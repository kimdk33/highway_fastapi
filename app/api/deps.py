from fastapi import Depends
from sqlmodel import Session

from app.core.session import get_session

SessionDep = Depends(get_session)
