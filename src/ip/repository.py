from src.container import get_container
from src.entities import IpEntity
from src.exceptions import CannotGetIpDataError
from src.http.client import HttpClient
from src.settings import settings


class IpRepository:
    def __init__(self):
        self.http_session: HttpClient = get_container().resolve(HttpClient)

    async def __get_ip_data(self, ip: str) -> dict:
        return await self.http_session.get(
            f"https://ipinfo.io/{ip}?token={settings.IP_API_KEY}"
        )

    def serialize_coordinates(self, location: str) -> tuple:
        return tuple(location.split(","))

    async def get_entity(self, ip: str) -> IpEntity:
        ip_data = await self.__get_ip_data(ip)
        try:
            return IpEntity(
                ip=ip_data.get("ip"),
                hostname=ip_data.get("hostname"),
                city=ip_data.get("city"),
                region=ip_data.get("region"),
                country=ip_data.get("country"),
                loc=self.serialize_coordinates(ip_data.get("loc"))
                if ip_data.get("loc") is not None
                else None,
                org=ip_data.get("org"),
                postal=ip_data.get("postal"),
                timezone=ip_data.get("timezone"),
            )
        except Exception as e:
            print(e)
            raise CannotGetIpDataError(e.args)
