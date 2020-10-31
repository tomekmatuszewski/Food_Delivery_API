from pydantic import BaseModel, StrictStr


class ClientSchema(BaseModel):
    company_name: StrictStr
    address: StrictStr
    contact_person: StrictStr
    phone: StrictStr
    email: StrictStr
    tax_identification_number: StrictStr
    company_id: StrictStr

