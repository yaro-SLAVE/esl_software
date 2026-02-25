from dataclasses import dataclass
from dataclasses_json import DataClassJsonMixin, config, Undefined
from aiohttp import ClientSession
from django.conf import settings

@dataclass
class ESLResponse(DataClassJsonMixin):
    dataclass_json_config = config(undefined=Undefined.EXCLUDE)["dataclasses_json"]
    status: str
    product_name: str
    message: str
    received_at: int


async def send_product(client: ClientSession, name: str, price: float, barcode: str, token: str, ip: str) -> ESLResponse:
    payload = {"name": name, "price": price, "barcode": barcode}

    headers = {"Authorization": 'Bearer ' + token}

    r = await client.post(f"http://{ip}/api/product/", json=payload, headers=headers)
    r.raise_for_status()
    return ESLResponse.schema().load(await r.json())