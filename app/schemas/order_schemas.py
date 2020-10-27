from typing import Optional
from pydantic import BaseModel, StrictStr, StrictFloat


class OrderSchema(BaseModel):
    full_name: StrictStr
    source_address: StrictStr
    destination_address: StrictStr
    other_info: Optional[StrictStr] = None

