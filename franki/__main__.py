import glob
import yaml
import argparse

from franki import FrankiFileNotFound, FrankiException
from franki.dal import parse_service_file
from franki.docker import cli_docker_compose, build_docker_compose


def _main_(args: argparse.Namespace):

    action = args.action

    actions = {
        'docker-compose': build_docker_compose
    }

    # Get source files
    sources = []
    for p in args.PATH:
        sources.extend(glob.glob(p, recursive=True))

    # Load servile files content
    services = []
    for src in sources:

        if not src.endswith("service.yaml"):
            continue

        try:
            with open(src, "r") as f:
                content: dict = yaml.safe_load(f.read())

        except (FileNotFoundError, FileExistsError, IOError) as e:
            raise FrankiFileNotFound(e)

        # Parse file
        service_config = parse_service_file(content)

        services.append(service_config)

    try:
        f = actions[action]
    except KeyError as e:
        raise FrankiException(f"Action '{action}' not valid")

    content_dict = f(args, services)

    print(content_dict)


def main():
    parser = argparse.ArgumentParser(
        description='Franki'
    )

    sub_parser = parser.add_subparsers(help="sub-command help",
                                       dest="action")

    # Add subparsers
    cli_docker_compose(sub_parser)

    # Parse args
    parsed = parser.parse_args()

    if not parsed.action:
        parser.print_help()
        exit(1)

    _main_(parsed)


if __name__ == '__main__':
    main()
