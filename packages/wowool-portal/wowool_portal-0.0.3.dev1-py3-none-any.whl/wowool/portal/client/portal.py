from logging import getLogger
import os
from json import loads as json_loads

from wowool.portal.client.defines import (
    WOWOOL_PORTAL_API_KEY_ENV_NAME,
    WOWOOL_PORTAL_HOST_DEFAULT,
    WOWOOL_PORTAL_HOST_ENV_NAME,
    WOWOOL_PORTAL_HEADERS_ENV_NAME,
)
from wowool.portal.client.httpcode import HttpCode
from wowool.portal.client.service import Service, API_PREFIX
from wowool.portal.client.environment import get_caller_var

5
logger = getLogger(__name__)

_portal = None


def current_portal():
    global _portal
    return _portal


def set_current_portal(portal):
    global _portal
    assert portal is not None
    _portal = portal


# Used by Portal objects, e.g. Pipeline etc
class _PortalMixin:
    def __init__(self, portal=None):
        self.portal = portal if portal is not None else current_portal()


class Portal:
    """
    :class:`Portal` is a class that holds the information required to connect to the Portal server. An instance of this class is passed to each :class:`Pipeline <wowool.portal.client.pipeline.Pipeline>` or :class:`Compiler <wowool.portal.client.compiler.Compiler>` instance so that the latter is able to send the required request:

    .. literalinclude:: init_pipeline.py
        :language: python

    Alternatively, instances of this class can also be used as a context manager avoiding the need to pass it to each pipeline or compiler explicitly:

    .. literalinclude:: init_pipeline_context.py
        :language: python
    """

    def __init__(
        self,
        host: str | None = None,
        api_key: str | None = None,
        headers: dict | None = None,
        auth: tuple[str, str] | None = None,
    ):
        """
        Initialize a Portal instance

        :param host: URL to the Portal. Defaults to http://api.wowool.com
        :type host: ``str``
        :param api_key: API key used to connect to the Portal
        :type api_key: ``str``

        :return: An initialized portal connection
        :rtype: :class:`Portal`

        .. tip::
            The API key can also be set using the ``WOWOOL_PORTAL_API_KEY`` environment variable.
            We recommend using this option over hard coding the key

        .. environment variables:
            WOWOOL_PORTAL_HOST (str)
            WOWOOL_PORTAL_API_KEY (str)
            WOWOOL_PORTAL_HEADERS (str, representing a JSON object )

        """
        self.host = host
        if self.host is None:
            self.host = get_caller_var(WOWOOL_PORTAL_HOST_ENV_NAME)

        if self.host is None:
            self.host = os.environ[WOWOOL_PORTAL_HOST_ENV_NAME] if WOWOOL_PORTAL_HOST_ENV_NAME in os.environ else WOWOOL_PORTAL_HOST_DEFAULT

        self.headers = headers
        if self.headers is None:
            self.headers = json_loads(os.environ[WOWOOL_PORTAL_HEADERS_ENV_NAME]) if WOWOOL_PORTAL_HEADERS_ENV_NAME in os.environ else None

        assert len(self.host) != 0, "Cannot pass empty url"
        if api_key is None:
            self.api_key = os.environ.get(WOWOOL_PORTAL_API_KEY_ENV_NAME, None)
        else:
            self.api_key = api_key

        assert self.api_key, "Cannot pass empty api_key"
        self.host = self.host[-1] if self.host.endswith("/") else self.host
        # self.host = f"https://{self.host}" if not self.host.startswith("https://") else self.host
        logger.debug(f"Using Portal {self.host}")
        if auth:
            auth_ = auth
        else:
            username = os.environ.get("WOWOOL_PORTAL_USERNAME", None)
            password = os.environ.get("WOWOOL_PORTAL_PASSWORD", None)
            if username and password:
                auth_ = (username, password)
            else:
                auth_ = None

        self._service = Service(self.host, self.headers, auth=auth_)

    def __enter__(self):
        set_current_portal(self)
        return self

    def __exit__(self, *_, **__):
        pass

    def __repr__(self):
        assert self.api_key
        return f"""wowool.portal.Portal(host="{self.host}", api_key ="******{self.api_key[-4:]}")"""
