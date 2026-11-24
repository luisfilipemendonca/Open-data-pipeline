from typing import Literal

from pydantic import BaseModel


class NavigationAction(BaseModel):
    type: Literal["navigate"]
    destination: Literal["imports", "schemas", "create-schema"]


class AssistantResponse(BaseModel):
    action: NavigationAction | None
    message: str | None = None


class AssistantPayload(BaseModel):
    message: str
