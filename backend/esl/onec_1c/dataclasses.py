from dataclasses import dataclass
from dataclasses_json import DataClassJsonMixin, config, Undefined

@dataclass
class ProductsListItemResponse(DataClassJsonMixin):
    dataclass_json_config = config(undefined=Undefined.EXCLUDE)["dataclasses_json"]
    id: str
    short_name: str

@dataclass
class ProductInfoResponse(DataClassJsonMixin):
    dataclass_json_config = config(undefined=Undefined.EXCLUDE)["dataclasses_json"]
    id: str
    short_name: str
    description: str
    price: float
    have_promotion: bool
    promotion: int

@dataclass
class CompanyOrFilial(DataClassJsonMixin):
    dataclass_json_config = config(undefined=Undefined.EXCLUDE)["dataclasses_json"]
    id: str
    name: str

@dataclass
class CompanyInfoResponse(DataClassJsonMixin):
    dataclass_json_config = config(undefined=Undefined.EXCLUDE)["dataclasses_json"]
    company: CompanyOrFilial
    filials: list[CompanyOrFilial]

@dataclass
class Update(DataClassJsonMixin):
    dataclass_json_config = config(undefined=Undefined.EXCLUDE)["dataclasses_json"]
    id: str
    short_name: str
    price: float
    have_promotion: bool | None
    promotion: int | None
