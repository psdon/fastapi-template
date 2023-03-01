from sqlmodel import Session
from {{cookiecutter.project_slug}}.api.schema import CurrentUser

from ..model import User


def get_or_create(session: Session, current_user: CurrentUser) -> User:
    obj = session.query(User).filter_by(auth0_id=current_user.auth0_id).first()
    if obj:
        return obj

    obj = User(**current_user.dict())
    session.add(obj)
    session.commit()

    return obj
