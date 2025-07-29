from pydantic import BaseModel, Field

class Personal(BaseModel):
    fistname: str = Field(description = "The first name", default = "Adama")
    lastname: str = Field(description = "The last name", default = "COULIBALY")

class Competence:

    personal: Personal = Personal()

    def __init__(self):
        pass

    def get(self):
        return self.personal

    def __str__(self):
        return f"class {personal.firstname}_{personal.lastname}_{id(self)}"
