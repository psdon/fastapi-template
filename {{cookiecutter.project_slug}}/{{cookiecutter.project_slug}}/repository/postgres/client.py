from sqlmodel import Session, create_engine
from sqlmodel.pool import StaticPool
from {{cookiecutter.project_slug}}.config.env import settings

# Set echo=True, if you want to print SQL Queries being executed. (i.e. Performance Debugging)
# future=False is required to use pandas.read_sql
# issue: https://github.com/pandas-dev/pandas/issues/44823#issuecomment-993828292
db_engine = (
    create_engine(settings.POSTGRES_URL, echo=False, future=False)
    if not settings.ENV == "unittest"
    else create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool, future=False)
)


def get_session():
    return Session(db_engine)
