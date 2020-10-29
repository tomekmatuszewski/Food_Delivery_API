from typing import Optional

from pydantic import BaseModel, StrictInt, StrictStr, StrictFloat


class OrderSchema(BaseModel):

    employee_id: StrictInt
    client_id: StrictInt
    contact_phone: StrictStr
    destination_address: StrictStr
    full_price: StrictFloat
    other_info: Optional[StrictStr] = None
