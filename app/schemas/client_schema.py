from pydantic import BaseModel, StrictStr


class ClientSchema(BaseModel):

    company_name: StrictStr
    address: StrictStr
