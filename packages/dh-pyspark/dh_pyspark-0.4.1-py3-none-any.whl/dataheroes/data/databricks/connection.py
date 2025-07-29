from ...configuration import DataHeroesConfiguration
from contextlib import contextmanager
from typing import Optional, Generator
from dataclasses import dataclass, field, fields
import logging
import dataclasses

@dataclass
class DatabricksConnection:
    """Create a Databricks connection based on credentials.
    If no credentials are provided, the connection will be created using the default configuration.
    No update of the credentials is possible after the connection is created.
    The configuration is not updated in the configuration file.

    Parameters
    ----------
    catalog : str, default=None
        The catalog to use for the query.

    schema : str, default=None
        The schema to use for the query.

    http_path : str, default=None
        The http path to use for the query.

    api_key : str, default=None
        The api key to use for the query.

    workspace_url : str, default=None
        The workspace url to use for the query.
    """
    catalog: Optional[str] = field(
        default_factory=lambda: DataHeroesConfiguration().get_param_str(
            "catalog", section="databricks"
        )
    )
    schema: Optional[str] = field(
        default_factory=lambda: DataHeroesConfiguration().get_param_str(
            "schema", section="databricks"
        )
    )
    http_path: Optional[str] = field(
        default_factory=lambda: DataHeroesConfiguration().get_param_str(
            "http_path", section="databricks"
        )
    )
    api_key: Optional[str] = field(
        default_factory=lambda: DataHeroesConfiguration().get_param_str(
            "api_key", section="databricks"
        )
    )
    workspace_url: Optional[str] = field(
        default_factory=lambda: DataHeroesConfiguration().get_param_str(
            "workspace_url", section="databricks"
        )
    )

    def __post_init__(self):
        self._dbsql = None
        self._logger = logging.getLogger(__name__)
        for f in fields(self):
            if getattr(self, f.name) is None:
                if not isinstance(f.default_factory, dataclasses._MISSING_TYPE):
                    # Use default_factory if it exists
                    setattr(self, f.name, f.default_factory())
                else:
                    raise ValueError(
                        f"No default value or default factory for field {f.name}"
                    )
        # If no workspace_url or api_key is provided, raise an error
        if self.workspace_url is None or self.api_key is None:
            raise ValueError(
                "Databricks connection requires workspace_url and api_key to be configured. "
                "Please run 'dataheroes-init' to set up your configuration file properly. "
                "For more information, use 'dataheroes-init --help'."
            )

    @property
    def dbsql(self):
        """Lazy loading of databricks.sql module"""
        if self._dbsql is None:
            try:
                import databricks.sql as dbsql
                from databricks.sql.exc import Error as DatabricksError

                self._dbsql = dbsql
                # Store the error class for use in get_connection
                self._dbsql_error = DatabricksError
            except ImportError:
                raise ImportError(
                    "databricks-sql-connector package is required. "
                    "Install it with: pip install databricks-sql-connector"
                )
        return self._dbsql

    @contextmanager
    def get_connection(self, http_path: Optional[str] = None) -> Generator:
        """
        Get a connection to Databricks SQL warehouse using context manager.

        Args:
            warehouse_id: Optional override for the warehouse_id from config

        Yields:
            databricks.sql.Connection: Active connection to Databricks

        Raises:
            DatabricksError: If there's an issue with the Databricks connection
            Other exceptions are allowed to propagate normally

        Example:
            with connection.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT * FROM my_table")
        """
        # Only import databricks when actually making a connection
        connection = None
        try:
            connector_url = http_path if http_path is not None else self.http_path

            try:
                connection = self.dbsql.connect(
                    server_hostname=self.workspace_url,
                    http_path=connector_url,
                    access_token=self.api_key,
                    catalog=self.catalog,
                    schema=self.schema,
                )
            except self._dbsql_error as e:
                self._logger.error(f"Error connecting to Databricks: {str(e)}")
                raise

            yield connection

        finally:
            if connection:
                try:
                    connection.close()
                except self._dbsql_error as e:
                    self._logger.warning(
                        f"Error closing Databricks connection: {str(e)}"
                    )
