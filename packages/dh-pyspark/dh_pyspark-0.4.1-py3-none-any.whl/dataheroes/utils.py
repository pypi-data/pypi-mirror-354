import random
import subprocess
import time
import platform
import typing
from logging import FileHandler
from pathlib import Path
from datetime import datetime
from typing import Optional
import psutil
import inspect
import sys
import os
import grpc
import warnings
import tempfile
import logging
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter as OTLPSpanExporterHttp
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace.export import BatchSpanProcessor, SpanExporter, SpanExportResult, ReadableSpan

import opentelemetry.sdk.trace.export
from opentelemetry.sdk.trace import TracerProvider, SpanLimits
from uuid import getnode as get_mac
from licensing.methods import Helpers
import json
import requests
from opentelemetry.sdk.util import BoundedList
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from decorator import decorate

from .configuration import get_config_license_key, DataHeroesConfiguration, get_library_code, Singleton
from .version import get_version
from .version_type import offline_version
import threading

_ctx = threading.local()

def _allow():
    _ctx.allow = True

def _deny():
    _ctx.allow = False

def _is_allowed():
    return getattr(_ctx, "allow", False)

TELEMETRY_CONFIG_URL = "https://telemetry.skcoreset.com/" if not offline_version() else ''
LICENSING_URL = "https://license.skcoreset.com/check_feature_v2/" if not offline_version() else ''
LICENSING_ACTIVATION_URL = "https://license.skcoreset.com/check_license_v2/" if not offline_version() else ''
NO_CONNECTION_MESSAGE = "HTTPS connectivity could not be established with" \
                        " our server to verify your account." \
                        " Please verify that you have Internet connectivity" \
                        " and that your firewall is not blocking external" \
                        " connections. If you need to continue using" \
                        " the library behind a firewall, " \
                        "please contact support@dataheroes.ai"
NO_FEATURE_MESSAGE_DEFAULT = 'License key {license_key} does not allow using the {feature_name} function. ' \
                             'If you need access to this function please contact support@dataheroes.ai.'
# suppress warnings when telemetry failed to send data for some reason (bad connection or our server is down)
opentelemetry.exporter.otlp.proto.grpc.exporter.logger.setLevel(logging.CRITICAL)
opentelemetry.sdk.trace.export.logger.setLevel(logging.CRITICAL)

# own https adapter with few retries (trying to keep work on bad connection)
# with these parameters should repeat after 1, 2, 4, 8 seconds
retries = Retry(total=4, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
https = requests.Session()
https.mount("https://", HTTPAdapter(max_retries=retries))

# Alternatively, we can use https://github.com/termcolor/termcolor/tree/main
def colored(text: str, color: Optional[str] = None) -> str:
    # If output is not a terminal and not a notebook, don't colour
    if not sys.stdout.isatty() and "ipykernel" not in sys.modules:
        return text
    if color is None:
        return text
    if color not in colored.COLORS:
        raise ValueError(f"Invalid color: {color}")
    return f"{colored.COLORS[color]}{text}{colored.COLORS['end']}"


colored.COLORS = {
    "black": "\033[30m",  # basic colors
    "red": "\033[31m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "blue": "\033[34m",
    "magenta": "\033[35m",
    "cyan": "\033[36m",
    "white": "\033[37m",
    "bright_black": "\033[90m",  # bright colors
    "bright_red": "\033[91m",
    "bright_green": "\033[92m",
    "bright_yellow": "\033[93m",
    "bright_blue": "\033[94m",
    "bright_magenta": "\033[95m",
    "bright_cyan": "\033[96m",
    "bright_white": "\033[97m",
    "end": "\033[0m",  # misc
    "bold": "\033[1m",
    "underline": "\033[4m",
}


def localtime(format="%Y-%m-%d %H:%M:%S") -> str:
    """Print localtime in the provided format using time.strftime"""
    return time.strftime(format, time.localtime())

def localtime_ms() -> str:
    """Print localtime in the provided format using datetime.now()"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]


def user_warning(message):
    """
    that's replacement for warnings.warn() fo messages that we would like to see in telemetry data
    """
    warnings.warn(message)
    current_span = trace.get_current_span()
    if type(current_span).__name__ != 'NonRecordingSpan':
        max_title_length = 50
        title = message[0:max_title_length]
        if len(message) > max_title_length:
            title += '...'
        current_span.add_event(title, {"text": message})


def telemetry(func):
    func.cache = {}
    return decorate(func, telemetry_inner)


def telemetry_inner(func, *args, **kwargs):
    current_span_name = func.__module__.split('.', 1)[-1] + '.' + func.__name__
    save_warning_filters = warnings.filters.copy()
    with TraceManager().tracer.start_as_current_span(current_span_name) as span:
        # opentelemetry get_tracer() reset all filters!
        warnings.filters = save_warning_filters
        if span.parent is None:
            # top level span, additional info
            span.set_attribute("OS", platform.platform())
            span.set_attribute("MAC address", ':'.join(("%012X" % get_mac())[i:i + 2] for i in range(0, 12, 2)))
            span.set_attribute("Total memory, GB", psutil.virtual_memory().total / 2 ** 30)
            span.set_attribute("CPU number", psutil.cpu_count())
            span.set_attribute("installed packages", TraceManager().pkg_list)
            span.set_attribute("Python version", sys.version)
        span.set_attribute("License key", get_config_license_key() or '')
        span.set_attribute("Library version", get_version())
        before_current_memory = psutil.Process().memory_full_info().uss
        start_cpu_time = time.process_time()
        result = func(*args, **kwargs)
        cpu_time_total = time.process_time() - start_cpu_time
        span.set_attribute("CPU time, ms", round(cpu_time_total*1000, 2))
        current_memory = psutil.Process().memory_full_info().uss
        span.set_attribute("CPU time, ms", round(cpu_time_total * 1000, 2))
        span.set_attribute("before memory usage, MB", f'{before_current_memory / 2 ** 20:.2f}')
        span.set_attribute("after memory usage, MB", f'{current_memory / 2 ** 20:.2f}')
        arg_names = func.__code__.co_varnames

        def process_value(param_value):
            delimiter = ", "
            if type(param_value).__name__ in ["ndarray", "DataFrame"] :
                return f'{type(param_value).__name__}(shape={param_value.shape}, size={param_value.size})'
            elif type(param_value).__name__ == "list":
                return f'{type(param_value).__name__}(len={len(param_value)})'
            elif type(param_value).__name__ == "tuple" or type(param_value).__name__ == "dict":
                is_dict = type(param_value).__name__ == "dict"
                # can be used for any iterable type, but hardly for lists due to performance issues
                values_representation = ""
                for iter_element in param_value:
                    if is_dict:
                        values_representation += str(iter_element)+'=' + \
                                                 process_value(param_value[iter_element]) + \
                                                 delimiter
                    else:
                        values_representation += process_value(iter_element) + delimiter
                values_representation = f'{type(param_value).__name__}({values_representation.rstrip(delimiter)})'
                return values_representation
            else:
                return str(param_value)

        def add_param_attribute(param_name, param_value):
            if "update_features" in current_span_name and (param_name == 'X'):
                # no real data in telemetry
                span.set_attribute(f"Params[{param_name}]", f"len({param_name})={len(param_value)}")
            elif 'grid_search' in current_span_name and (param_name == 'param_grid'):
                span.set_attribute(f"Params[{param_name}]", str(param_value))
            elif param_name == "data_tuning_params":
                span.set_attribute(f"Params[{param_name}]", str(param_value))
            else:
                span.set_attribute(f"Params[{param_name}]", process_value(param_value))

        params_written = []
        for arg_index, arg in enumerate(args):
            add_param_attribute(arg_names[arg_index], arg)
            params_written.append(arg_names[arg_index])
        for kwarg in kwargs:
            add_param_attribute(kwarg, kwargs[kwarg])
            params_written.append(kwarg)
        for default_param in [{"name": p, "value": inspect.signature(func).parameters[p].default}
                              for p in inspect.signature(func).parameters if p not in params_written]:
            add_param_attribute(default_param['name'], default_param['value'])
        add_param_attribute("result", result)
        return result


class LicenseFeatures(metaclass=Singleton):
    no_feature_message = NO_FEATURE_MESSAGE_DEFAULT
    fl = []


class LicenseManager(metaclass=Singleton):
    def __init__(self):
        activate_account()

    @classmethod
    def clear_instance(cls):
        if cls in cls._instances:
            del cls._instances[cls]


class FileSpanExporter(SpanExporter):
    """
    Implementation of :class:`SpanExporter` that write spans to a logger file.
    The reason for logger file is to utilize the file rotating capabilities,
    logging level are irrelevant since it only used a "rotating file writer".
    Only relevant parameters are how many backups to keep and directory to store.
    The telemetry data is written as a json encoded object to the file.
    To disable writing telemetry data to file set the parameter `enable_logger` in `dataheroes.config` to - 0
    """

    def __init__(
        self,
        service_name: Optional[str] = None,
        formatter: typing.Callable[
            [ReadableSpan], str
        ] = lambda span: span.to_json()
        + os.linesep,
    ):
        self.formatter = formatter
        self.service_name = service_name
        self._logger = self._init_logger()

    @classmethod
    def _init_logger(cls):
        logger = logging.getLogger(get_library_code() + '.telemetry')
        # disable propagation to root logger to avoid telemetry data printed to stout if root logger set.
        logger.propagate = False
        if not logger.handlers:
            # get telemetry logger params
            if int(DataHeroesConfiguration().get_param('enable_logger', default_value=1)):
                handler = cls._get_rotating_file_handler()
            else:
                # add empty handler that does nothing
                handler = logging.NullHandler()
            logger.setLevel(logging.DEBUG)
            logger.addHandler(handler)
        return logger

    @classmethod
    def _delete_old_log_files(cls, log_dir: str, max_backups):
        # get all files of the log name template dataheroes*.log
        log_files = list(str(f) for f in Path(log_dir).glob('dataheroes*.log'))

        # if we have more backups than allowed, delete old files
        if len(log_files) > 0 and len(log_files) >= max_backups:
            # sort new to old
            log_files.sort(reverse=True)
            # files for deletion
            old_logs = log_files[-(len(log_files) - max_backups):]
            for old_log in old_logs:
                if os.path.exists(old_log):
                    os.remove(old_log)

    @classmethod
    def _get_log_filename(cls):
        return f"dataheroes_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

    @classmethod
    def _get_rotating_file_handler(cls):
        backup_count = int(DataHeroesConfiguration().get_param('logger_backup_count',
                                                               default_value=100))
        log_directory = DataHeroesConfiguration().get_param('logger_path')

        if log_directory is None:
            # create $HOME/dataheroes_logs folder if file path is not set
            log_directory = os.path.join(str(Path.home()), f'{get_library_code()}_logs')

        cls._create_log_dir(log_directory)

        logger_file_path = os.path.join(log_directory, cls._get_log_filename())

        # get all log files and if list exceeds the allowed backup count delete
        cls._delete_old_log_files(log_directory, backup_count)

        handler = FileHandler(logger_file_path)

        formatter = logging.Formatter(fmt='%(name)s: %(message)s')
        handler.setFormatter(formatter)
        # setting handler level just not to leave empty
        handler.setLevel(logging.DEBUG)
        return handler

    @classmethod
    def _create_log_dir(cls, log_dir):
        # make sure the folder for file exists, or it's not a directory (a file exists with the same name)
        if not os.path.exists(log_dir) or not os.path.isdir(log_dir):
            os.mkdir(log_dir)

    def export(self, spans: typing.Sequence[ReadableSpan]) -> SpanExportResult:
        for span in spans:
            self._logger.info(self.formatter(span))
        return SpanExportResult.SUCCESS

    def force_flush(self, timeout_millis: int = 30000) -> bool:
        return True


class OTLPHandler(logging.Handler):

    def emit(self, record):
        event = {"level": record.levelname, "msg": self.format(record)}
        span = trace.get_current_span()
        # in the common case, this will be called within an open span like build, grid_search and
        # any other @telemetry wrapped function etc.
        # Otherwise, when a logger was initialized outside telemetry wrapped function, a new child span is opened
        if span.is_recording():
            # check we don't overflow events limit and add to the current open span
            if len(span.events) < int(DataHeroesConfiguration().get_param(name="max_span_events", default_value=2048)):
                span.add_event("log_entry", event)
            else:
                warnings.warn(f"span events over limit: {len(span.events)}")
        else:
            # this will open (and close) a new child span of a previous span
            with TraceManager().tracer.start_as_current_span(record.name) as span:
                span.add_event("log_entry", event)


def get_logger(name: str) -> logging.Logger:
    """
    Returns an initiated python logger object.
    The logger has an otlp handler attached that writes the telemetry data to a file
    The log entries are added to the "events" array in the telemetry.
    The logging level can be configured by the `log_level` parameter in the `dataheroes.config` file.
    Default level is `INFO`.
    Setting log lvl to `DEBUG` in the `dataheroes.config` will automatically attach a console handler to the logger
    for printing log entries to the screen.
    """
    logger = logging.getLogger(name)

    log_level = _get_logger_level(logger_param='logger_level', max_level=logging.DEBUG)

    logger.setLevel(log_level)

    if not logger.handlers:
        # add handlers
        formatter = logging.Formatter(fmt='%(asctime)s %(levelname)-4s %(name)s: %(message)s',
                                      datefmt='%Y-%m-%d %H:%M:%S')
        otlp_handler = OTLPHandler()
        otlp_handler.setLevel(log_level)
        otlp_handler.setFormatter(formatter)
        logger.addHandler(otlp_handler)

        # auto console logger for debug
        if 'StreamHandler' in DataHeroesConfiguration().get_param(section='logger', name="handlers", default_value=""):
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logger.level)
            stream_handler.setFormatter(formatter)
            logger.addHandler(stream_handler)
    return logger


def _get_logger_level(logger_param, max_level=logging.INFO) -> int:
    """
    Get logger level from configuration
    limit severity to INFO and print warning if exceeds
    """
    log_level = DataHeroesConfiguration().get_param(logger_param,
                                                    default_value=max_level)
    # translate str to int value, debug->10, info->20...
    if isinstance(log_level, str):
        try:
            log_level = int(logging.getLevelName(log_level.upper()))
        except ValueError as e:
            warnings.warn(f'{str(e)}, setting {logger_param} to: {logging.getLevelName(max_level)}')
            log_level = max_level

    if log_level > max_level:
        warnings.warn(
            f"{logger_param} value: {logging.getLevelName(log_level)} exceeds {logging.getLevelName(max_level)}, setting to: {logging.getLevelName(max_level)}")
        log_level = max_level
    return log_level


class TraceManager(metaclass=Singleton):

    def __init__(self):
        resource = Resource(attributes={"service.name": get_library_code()})
        # we need to increase the max span events value because the default value is only 128
        max_span_events = int(DataHeroesConfiguration().get_param(name="max_span_events",
                                                                  default_value=2048))
        trace.set_tracer_provider(TracerProvider(resource=resource,
                                                 span_limits=SpanLimits(max_events=max_span_events)))
        self.pkg_list = subprocess.check_output(["pip", "freeze"])

        # add file exporter
        file_processor = BatchSpanProcessor(FileSpanExporter())
        trace.get_tracer_provider().add_span_processor(file_processor)
        self.span_processors = [file_processor]

        if not offline_version():
            # add online telemetry exporter for an online version
            # that will work only when our AWS-hosted service is online (and return certificate)
            otlp_exporter = self.get_otlp_exporter()
            span_processor = BatchSpanProcessor(otlp_exporter)
            trace.get_tracer_provider().add_span_processor(span_processor)
            self.span_processors.append(span_processor)

        self.tracer = trace.get_tracer("none")
        self.current_function_name = None
        self.enabled = True

    def get_otlp_exporter(self):
        try:
            response = https.get(TELEMETRY_CONFIG_URL)
            if response.status_code != 200:
                raise RuntimeError(NO_CONNECTION_MESSAGE)
            telemetry_config = json.loads(response.content)
            if telemetry_config.get('errorMessage', '') != '':
                raise RuntimeError(telemetry_config.get('errorMessage'))
            if telemetry_config.get('cert', '') == '':
                raise RuntimeError(NO_CONNECTION_MESSAGE)
        except requests.exceptions.ConnectionError:
            raise RuntimeError(NO_CONNECTION_MESSAGE)
        use_https_protocol = telemetry_config.get('use_http', '0') == '1'
        if DataHeroesConfiguration().get_param("use_http") is not None \
                and DataHeroesConfiguration().get_param_str("use_http") != "":
            use_https_protocol = DataHeroesConfiguration().get_param_bool("use_http")
        if use_https_protocol:
            temp_dir = tempfile.mkdtemp()
            cert_file_path = os.path.join(temp_dir, 'cert.pem')
            with open(cert_file_path, 'wb') as f:
                f.write(str.encode(telemetry_config.get('cert')))
            otlp_exporter = OTLPSpanExporterHttp(endpoint=telemetry_config.get('url_http'),
                                                 certificate_file=cert_file_path)

            # all this for tmp-file deletion
            original_shutdown = opentelemetry.sdk.trace.export.BatchSpanProcessor.shutdown

            def own_shutdown(self) -> None:
                original_shutdown(self)
                if os.path.exists(cert_file_path):
                    os.remove(cert_file_path)

            opentelemetry.sdk.trace.export.BatchSpanProcessor.shutdown = own_shutdown
        else:
            credentials = grpc.ssl_channel_credentials(str.encode(telemetry_config.get('cert')))
            otlp_exporter = OTLPSpanExporter(endpoint=telemetry_config.get('url_grcp'), credentials=credentials)
            # instead of original [1, 2, 4, 8, 16, 32], set shorter set of delays
            opentelemetry.exporter.otlp.proto.grpc.exporter._expo = lambda *args, **kwargs: [1, 2, 4]

        # adjust custom events translate to enforce events filter:
        self._set_custom_events_filter(otlp_exporter)
        return otlp_exporter

    @classmethod
    def _set_custom_events_filter(cls, otlp_exporter):
        """
        This method wraps the original `export` method of the OTLPSpanExporter,OTLPSpanExporterHttp
        For each span passed to the exporter we will check the events array and filter log_entry items based on
        log level.
        """
        telemetry_logger_level = _get_logger_level(logger_param='telemetry_log_level')

        original_export = otlp_exporter.export

        def own_export(spans: typing.Sequence[ReadableSpan]) -> SpanExportResult:
            for sdk_span in spans:
                if sdk_span.events:
                    filtered_events = []
                    for span_event in sdk_span.events:
                        # we are only interested in the log events
                        if span_event.name == 'log_entry':
                            level = span_event.attributes.get('level')
                            # check that the message log level is equal or over the set logger level.
                            # for unknown message level we will assume debug as level
                            try:
                                log_level = int(logging.getLevelName(level))
                            except ValueError:
                                log_level = logging.INFO
                            if log_level >= telemetry_logger_level:
                                filtered_events.append(span_event)
                        else:
                            filtered_events.append(span_event)
                    # create the bounded list object based on the filtered events
                    bounded_event_list = BoundedList(len(filtered_events))
                    for event in filtered_events:
                        bounded_event_list.append(event)
                    sdk_span._events = bounded_event_list
            return original_export(spans)

        otlp_exporter.export = own_export

    @classmethod
    def clear_instance(cls):
        if cls in cls._instances:
            del cls._instances[cls]


def add_telemetry_attribute(name, value):
    trace.get_current_span().set_attribute(name, value)


def activate_account(email=''):
    return
    """
    if email =='' and config has not license key,
    we are trying to activate temporary license
    """
    if not offline_version():
        try:
            machine_code = Helpers.GetMachineCode(v=2)
            license_key = get_config_license_key()
            request_data = dict(machine_code=machine_code or '',
                                email=email or '',
                                license_key=license_key or '')
            wait_response = True
            repeat_count = 1
            while wait_response:
                response = https.post(url=LICENSING_ACTIVATION_URL, json=request_data)
                if not json.loads(response.content).get('message', '') == 'Endpoint request timed out':
                    wait_response = False
                elif repeat_count > 5:
                    raise RuntimeError('Endpoint request timed out')
                else:
                    # if there are lot requests at once, we have a problem on the server side
                    # this parameters let to distribute ~20 requests in time
                    time_to_sleep = random.randint(1, 5) * 40
                    time.sleep(time_to_sleep)
                    repeat_count += 1
            if response.status_code != 200:
                raise RuntimeError(f'{NO_CONNECTION_MESSAGE} {response.status_code=}')
            result = json.loads(response.content)
            LicenseFeatures().no_feature_message = result.get('no_feature_message', NO_FEATURE_MESSAGE_DEFAULT)
            LicenseFeatures().fl = json.loads((result.get('features', '[]')))
            if result.get('errorMessage', '') != '':
                raise RuntimeError(result.get('errorMessage', ''))
            if result.get('message', '') != '':
                raise RuntimeError(result.get('message'))
            if license_key != result.get('key'):
                DataHeroesConfiguration(licensing__license_key=result.get("key"))
                DataHeroesConfiguration().update_create_config_file(
                    section_name='licensing',
                    param_name='license_key',
                    param_value=result.get("key")
                )
        except requests.exceptions.ConnectionError:
            raise RuntimeError(NO_CONNECTION_MESSAGE)


def check_feature_for_license(feature_name):
    return
    no_license_message = LicenseFeatures().no_feature_message.format_map(
                {"feature_name": feature_name, "license_key": get_config_license_key()})

    date_limit_license = datetime.strptime('01-01-9999', '%d-%m-%Y')
    if datetime.now() > date_limit_license:
        raise RuntimeError(no_license_message)
    # that is only to call activate_account only once per session (but user can activate_account manually)
    if not offline_version():
        LicenseManager()
        if feature_name not in LicenseFeatures().fl:
            raise RuntimeError(no_license_message)


def unsupported_method_in(service_name: str):
    def decorator(func):
        def wrapper(*args, **kwargs):
            raise AttributeError(f"{func.__name__} is not supported for {service_name}.")
        return wrapper
    return decorator
