from pydantic import BaseModel, StrictStr


class EmployeeSchema(BaseModel):
    first_name: StrictStr
    last_name: StrictStr
    gender: StrictStr
    date_of_birth: StrictStr
    address: StrictStr
    phone: StrictStr
    email: StrictStr
    id_number: StrictStr
    salary: float
