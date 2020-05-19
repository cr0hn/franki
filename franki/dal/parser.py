"""
This file has the parser of files:
- *.service.yaml
"""

from .services import *
from ..exceptions import *


def parse_service_file(file_content: dict) -> ServiceConfig:

    # Checking basic values
    try:
        service_dict = file_content["service"]

        for b in ("version", "name", "port", "repository"):
            _ = service_dict[b]

        service = Service(**service_dict)

    except KeyError as e:
        raise FrankiInvalidFileFormat(
            f"Invalid service file format. Missing '{e}'"
        )

    try:
        registries = [Registry(**x) for x in file_content["registries"]]
    except KeyError as e:
        registries = []

    try:
        repositories = [Repository(**x) for x in file_content["repositories"]]
    except KeyError as e:
        repositories = []

    service_config = ServiceConfig(
        service=service,
        registries=registries,
        repositories=repositories
    )

    return service_config
