"""
The reason this file exists is to serve as a flag for the offline version
When building a wheel, a `version_type_no_internet.py` file is copied as `version_type.py`
and the function `offline_version` returns `True`.
Based on this flag the `utils.py` file, handles licensing and telemetry.
"""


def offline_version():
    return False
