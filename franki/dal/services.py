from typing import Optional, List
from dataclasses import dataclass, field

from ..exceptions import FrankiInvalidFileFormat


ALLOWED_REPOSITORIES = ("github", "gitlab")

@dataclass
class Auth:
    user: str
    password: str


@dataclass
class Registry:
    auth: Optional[Auth]
    server: str
    name: str

    def __post_init__(self):
        if self.auth:
            self.auth = Auth(**self.auth)

@dataclass
class Repository:
    auth: Optional[Auth]
    server: str
    name: str

    def __post_init__(self):
        if self.auth:
            self.auth = Auth(**self.auth)

@dataclass
class ServiceDependency:
    name: str
    image: str
    command: str = None
    registry: str = "https://hub.docker.com"
    environment: Optional[List[str]] = field(default_factory=list)


@dataclass
class Service:
    version: str
    name: str
    port: int
    repository: str
    command: str = None
    entrypoint: str = None
    urls: Optional[List[str]] = field(default_factory=list)
    environment: Optional[List[str]] = field(default_factory=list)
    secrets: Optional[List[str]] = field(default_factory=list)
    dependencies: Optional[List[ServiceDependency]] = field(default_factory=list)

    def __post_init__(self):
        if self.repository not in ALLOWED_REPOSITORIES:
            raise FrankiInvalidFileFormat(
                f"Currently only supports these repositories: "
                f"{','.join(ALLOWED_REPOSITORIES)}"
            )

        if self.dependencies:
            self.dependencies = [
                ServiceDependency(**x) for x in self.dependencies
            ]


    @classmethod
    def from_dict(cls, content: dict):
        return cls()

@dataclass
class ServiceConfig:
    service: Service
    registries: List[Registry] = field(default_factory=list)
    repositories: List[Registry] = field(default_factory=list)
