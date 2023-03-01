import sentry_sdk
from {{cookiecutter.project_slug}}.config.env import Settings


def init_sentry(settings: Settings):
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        environment=settings.ENV,
        release=f"{settings.APP_NAME}@{settings.VERSION}",
        send_default_pii=True,
    )
