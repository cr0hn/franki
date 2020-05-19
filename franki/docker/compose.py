import argparse

from typing import List

import yaml

from ..dal.services import ServiceConfig

TAB = " " * 2


def cli_docker_compose(parser: argparse._SubParsersAction):
    sub_parser = parser.add_parser("docker-compose",
                                   help="build a docker-compose")
    sub_parser.add_argument("-v", "--compose-version",
                            default="3.7",
                            help="minimum docker-compose format")
    sub_parser.add_argument("PATH", nargs="+")


def build_docker_compose(parsed: argparse.Namespace,
                         services_config: List[ServiceConfig]) -> str:

    #
    # NOT USE YAML LIBRARY BECAUSE IT DOESN'T GUARANTEES ORDER ON KEYS
    #
    data_service = [
        f"version: {parsed.compose_version}",
        f"services:\n",
    ]
    for serv in services_config:
        service = serv.service

        # -------------------------------------------------------------------------
        # Service config
        # -------------------------------------------------------------------------
        data_service.extend([
            f"{TAB}#{'-' * 40}",
            f"{TAB}# Service: '{service.name}'",
            f"{TAB}#{'-' * 40}",
            f"{TAB}{service.name.lower()}:",
            f"{TAB}{TAB}image: {service.name.lower()}:{service.version}"
        ])

        if service.environment:
            data_service.append(f"{TAB}{TAB}environment:")
            for e in service.environment:
                data_service.append(f"{TAB}{TAB}{TAB}- {e}={e}")

        if service.port:
            data_service.append(f"{TAB}{TAB}ports:")
            data_service.append(f"{TAB}{TAB}{TAB}- {service.port}:{service.port}")

        if service.command:
            data_service.append(f"{TAB}{TAB}command: {service.command}")

        if service.entrypoint:
            data_service.append(f"{TAB}{TAB}command: {service.entrypoint}")

        data_service.append("")

        # -------------------------------------------------------------------------
        # Dependencies
        # -------------------------------------------------------------------------
        for dep in service.dependencies:
            data_service.append(f"{TAB}{dep.name}:")
            data_service.append(f"{TAB}{TAB}image: {dep.image}")
            data_service.append(f"{TAB}{TAB}environment:")

            for e in dep.environment:
                data_service.append(f"{TAB}{TAB}{TAB} - {e}={e}")

            # TODO: importar de catálogo
            if dep.command:
                data_service.append(f"{TAB}{TAB}command: {dep.command}")
            # if dep.ports:
            #     data_service.append(f"{TAB}{TAB}ports: {dep.environment}")

            data_service.append("")

        data_service.extend([
            f"{TAB}#{'-' * 40}",
            f"{TAB}# END '{service.name}'",
            f"{TAB}#{'-' * 40}"
        ])

    return "\n".join(data_service)


__all__ = ("cli_docker_compose", "build_docker_compose")
