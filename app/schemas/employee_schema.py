from pydantic import BaseModel, StrictStr


class EmployeeSchema(BaseModel):

    first_name: StrictStr
    last_name: StrictStr
