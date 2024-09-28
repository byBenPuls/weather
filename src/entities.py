from dataclasses import dataclass


@dataclass
class IpEntity:
    ip: str
    hostname: str
    city: str
    region: str
    country: str
    loc: tuple
    org: str
    postal: str
    timezone: str


@dataclass(frozen=True)
class Weather:
    pass
