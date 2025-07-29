from typing import List, Optional
from pydantic import BaseModel, Field


class PasswordLoginRequest(BaseModel):
    email: str
    password: str
    long_lived: Optional[bool] = Field(serialization_alias="longLived", default=True)
    organization_id: str = Field(serialization_alias="organizationId")


class Jwt(BaseModel):
    access_token: str = Field(alias="accessToken")
    refresh_token: str = Field(alias="refreshToken")
    long_lived: bool = Field(alias="longLived")
    logout_url: Optional[str] = Field(alias="logoutUrl")


class Organization(BaseModel):
    id: str
    name: str
    firstname: str
    lastname: str
    email: str
    language: str


class AuthProvider(BaseModel):
    id: str
    name: str


class SingleOrg(BaseModel):
    organization: Organization
    auth_providers: List[AuthProvider] = Field(alias="authProviders")
    require_password: bool = Field(alias="requirePassword")
    backend_version: str = Field(alias="backendVersion")
    domain: str
