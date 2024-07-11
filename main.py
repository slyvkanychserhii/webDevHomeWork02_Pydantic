# pip install pydantic
# pip install email-validator  # pip install 'pydantic[email]'

from pydantic import BaseModel, Field, EmailStr, field_validator, ValidationError


class Address(BaseModel):
    city: str = Field(..., min_length=2)
    street: str = Field(..., min_length=3)
    house_number: int = Field(..., gt=0)


class User(BaseModel):
    name: str = Field(..., min_length=2)
    age: int = Field(..., gt=0, lt=120)
    email: EmailStr
    is_employed: bool = False
    address: Address

    @field_validator('name')
    def check_name(cls, value):
        if not value.isalpha():
            raise ValueError('Name must contain only alphabetic characters')
        return value

    @field_validator('is_employed')
    def check_employment_age(cls, value, values):
        age = values.data.get('age')
        if value and age is not None and age < 18:
            raise ValueError('User must be at least 18 years old to be employed')
        return value

    @classmethod
    def ich_model_validate_json(cls, json_string):
        try:
            user = cls.model_validate_json(json_string)
            return user.json()
        except ValidationError as e:
            return e.json()


valid_json_1 = """{
    "name": "Serhii",
    "age": 40,
    "email": "serhii@example.com",
    "is_employed": true,
    "address": {
        "city": "Mülheim an der Ruhr",
        "street": "Aktienstraße",
        "house_number": 123
    }
}"""

valid_json_2 = """{
    "name": "Alice",
    "age": 16,
    "email": "alice@example.com",
    "address": {
        "city": "Mülheim an der Ruhr",
        "street": "Aktienstraße",
        "house_number": 123
    }
}"""

invalid_name_json = """{
    "name": "serhii_123",
    "age": 40,
    "email": "serhii@example.com",
    "address": {
        "city": "Mülheim an der Ruhr",
        "street": "Aktienstraße",
        "house_number": 123
    }
}"""

invalid_age_json = """{
    "name": "Serhii",
    "age": 130,
    "email": "serhii@example.com",
    "address": {
        "city": "Mülheim an der Ruhr",
        "street": "Aktienstraße",
        "house_number": 123
    }
}"""

invalid_email_json = """{
    "name": "Serhii",
    "age": 40,
    "email": "serhiiexample.com",
    "address": {
        "city": "Mülheim an der Ruhr",
        "street": "Aktienstraße",
        "house_number": 123
    }
}"""

invalid_employment_age_json = """{
    "name": "Serhii",
    "age": 16,
    "email": "serhii@example.com",
    "is_employed": true,
    "address": {
        "city": "Mülheim an der Ruhr",
        "street": "Aktienstraße",
        "house_number": 123
    }
}"""

print(User.ich_model_validate_json(valid_json_1))
print(User.ich_model_validate_json(valid_json_2))
print(User.ich_model_validate_json(invalid_name_json))
print(User.ich_model_validate_json(invalid_age_json))
print(User.ich_model_validate_json(invalid_email_json))
print(User.ich_model_validate_json(invalid_employment_age_json))
