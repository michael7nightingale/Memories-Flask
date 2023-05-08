from typing import IO

from pydantic import BaseModel, constr, ValidationError, validator
from pydantic.dataclasses import dataclass
import re


class User(BaseModel):
    username: str
    password: str
    email: str
    #
    # @validator('username')
    # @classmethod
    # def validate_username(cls, v: str):
    #     min_length = 5
    #     max_length = 20
    #     if not(min_length <= len(v.strip()) <= max_length):
    #         raise ValidationError
    #     return v
    #
    # @validator('email')
    # @classmethod
    # def validate_email(cls, v: str):
    #     if not re.match(r'\S+@\S+.\S+', v).group()[0] == v:
    #         raise ValidationError
    #     return v
    #
    # @validator('password')
    # @classmethod
    # def validate_password(cls, v: str):
    #     min_length = 5
    #     max_length = 30
    #     if not (min_length <= len(v.strip()) <= max_length):
    #         raise ValidationError
    #     return v


class Theme(BaseModel):
    title: str
    isPublic: bool
    key: None | str = None
    user_id: int


class Card(BaseModel):
    theme_id: int
    ask_side: str
    answer_side: str


class Request:
    form: dict






