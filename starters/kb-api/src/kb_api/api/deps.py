from typing import Annotated

from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from kb_api.config import Settings, get_settings
from kb_api.db import get_session

SessionDep = Annotated[AsyncSession, Depends(get_session)]
SettingsDep = Annotated[Settings, Depends(get_settings)]


def require_api_key(settings: SettingsDep, x_api_key: Annotated[str | None, Header()] = None) -> None:
    """Like a before_action: write endpoints need a valid X-API-Key header."""
    if x_api_key != settings.api_key.get_secret_value():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key")
