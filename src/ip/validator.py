from dataclasses import dataclass

from src.entities import IpEntity
from src.exceptions import IpNotFromRussiaError


@dataclass
class IPValidator:
    ip_entity: IpEntity

    async def validate_ip_address(self) -> IpEntity:
        if self.ip_entity.country != "RU":
            raise IpNotFromRussiaError
        return self.ip_entity
