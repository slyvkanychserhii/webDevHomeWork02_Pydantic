# Web development: домашние задание 2 (Python)

Разработать систему регистрации пользователя, используя Pydantic для валидации входных данных, обработки вложенных структур и сериализации. Система должна обрабатывать данные в формате JSON.

Задачи:
- Создать классы моделей данных с помощью Pydantic для пользователя и его адреса.
- Реализовать функцию, которая принимает JSON строку, десериализует её в объекты Pydantic, валидирует данные, и в случае успеха сериализует объект обратно в JSON и возвращает его.
- Добавить кастомный валидатор для проверки соответствия возраста и статуса занятости пользователя.
- Написать несколько примеров JSON строк для проверки различных сценариев валидации: успешные регистрации и случаи, когда валидация не проходит (например возраст не соответствует статусу занятости).

Модели:

- Address: Должен содержать следующие поля:
    - city: строка, минимум 2 символа.
    - street: строка, минимум 3 символа.
    - house_number: число, должно быть положительным.

- User: Должен содержать следующие поля:
  - name: строка, должна быть только из букв, минимум 2 символа. 
  - age: число, должно быть между 0 и 120.
  - email: строка, должна соответствовать формату email.
  - is_employed: булево значение, статус занятости пользователя. 
  - address: вложенная модель адреса.

```python

from typing import Self
from pydantic import (
    BaseModel,
    Field,
    PositiveInt,
    EmailStr,
    ValidationError,
    model_validator
)


class Address(BaseModel):
    city: str = Field(min_length=2)
    street: str = Field(min_length=3)
    house_number: PositiveInt


class User(BaseModel):
    name: str = Field(pattern="^[A-Za-z]{2,}$")
    age: int = Field(gt=0, lt=120)
    email: EmailStr
    is_employed: bool = False
    address: Address

    @model_validator(mode="after")
    def check_employment_age(self) -> Self:
        is_employed = self.is_employed
        age = self.age
        if is_employed and not (18 <= age <= 65):
            raise ValueError("Employed users must be between 18 and 65 years old")
        return self


def user_validate_json(user_json):
    try:
        user = User.model_validate_json(user_json)
        return user.model_dump_json()
    except ValidationError as e:
        print(e)


new_user_json_1 = """
{"name": "Serhii",
"age": 40,
"email": "serhii@example.com",
"is_employed": true,
"address": {
"city": "Mülheim an der Ruhr",
"street": "Aktienstraße",
"house_number": 123}}
"""
new_user_1 = user_validate_json(new_user_json_1)
print(new_user_1)

new_user_json_2 = """
{"name": "Alice",
"age": 16,
"email": "alice@example.com",
"address": {
"city": "Mülheim an der Ruhr",
"street": "Aktienstraße",
"house_number": 123}}
"""
new_user_2 = user_validate_json(new_user_json_2)
print(new_user_2)

new_user_json_invalid_name = """
{"name": "serhii_123",
"age": 40,
"email": "serhii@example.com",
"address": {
"city": "Mülheim an der Ruhr",
"street": "Aktienstraße",
"house_number": 123}}
"""
new_user_3 = user_validate_json(new_user_json_invalid_name)

new_user_json_invalid_age = """
{"name": "Serhii",
"age": 130,
"email": "serhii@example.com",
"address": {
"city": "Mülheim an der Ruhr",
"street": "Aktienstraße",
"house_number": 123}}
"""
new_user_4 = user_validate_json(new_user_json_invalid_age)

new_user_json_invalid_email = """
{"name": "Serhii",
"age": 40,
"email": "serhiiexample.com",
"address": {
"city": "Mülheim an der Ruhr",
"street": "Aktienstraße",
"house_number": 123
}}
"""
new_user_5 = user_validate_json(new_user_json_invalid_email)

new_user_json_invalid_employment_age = """
{"name": "Serhii",
"age": 16,
"email": "serhii@example.com",
"is_employed": true,
"address": {
"city": "Mülheim an der Ruhr",
"street": "Aktienstraße",
"house_number": 123}}
"""
new_user_6 = user_validate_json(new_user_json_invalid_employment_age)
```

