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
        return f"class {self.personal.firstname}_{self.personal.lastname}_{id(self)}"
