from pydantic import BaseModel
from typing import Dict


class UserDetails(BaseModel):
    name: str
    password: str


class Credentials(BaseModel):
    usernames: Dict[str, UserDetails]


class CredentialsCommitRequest(BaseModel):
    credentials: Credentials
