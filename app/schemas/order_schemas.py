from typing import Optional

from pydantic import BaseModel, StrictInt, StrictStr


class OrderSchema(BaseModel):

    employee_id: StrictInt
    source_address: StrictStr
    destination_address: StrictStr
    other_info: Optional[StrictStr] = None
