from dataclasses import dataclass
from dataclasses_json import DataClassJsonMixin, config, Undefined
from aiohttp import ClientSession
from django.conf import settings

@dataclass
class ESLResponse(DataClassJsonMixin):
    dataclass_json_config = config(undefined=Undefined.EXCLUDE)["dataclasses_json"]
    status: str
    code: int
    message: str


def send_product(client: ClientSession, name: str, price: float, barcode: str, token: str) -> ESLResponse:
    payload = {"name": name, "price": price, barcode: barcode}

    headers = {"Authorization": 'Bearer ' + token}

    r = client.post(f"http://10.108.129.180/api/product/", json=payload, headers=headers)
    r.raise_for_status()
    return ESLResponse.schema().load(r.json())