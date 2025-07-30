from __future__ import absolute_import, unicode_literals

# Standard Library
import atexit
import pickle
from typing import TypeVar
from urllib.parse import parse_qs

import environ
import msal
import seqslab
from msal.oauth2cli.authcode import (
    AuthCodeReceiver,
    _AuthCodeHandler,
    _AuthCodeHttpServer,
    _AuthCodeHttpServer6,
    _qs2kv,
)
from nubia import context
from pydantic import BaseModel

env = environ.Env()
environ.Env.read_env("/etc/seqslab/cli_apps.env")

PRIVATE_NAME = env.str("PRIVATE_NAME", "api")
API_HOSTNAME = f"{PRIVATE_NAME}.seqslab.net"
SOCIAL_AUTH_AZURE_KEY = env.str(
    "AZUREAD_OAUTH2_KEY", "b10403db-7700-42c2-996e-116578438579"
)
SOCIAL_AUTH_AZURE_TENANT_ID = env.str("AZUREAD_OAUTH2_TENANT", "organizations")
SOCIAL_AUTH_AZURE_SCOPE = env.json(
    "AZUREAD_OAUTH2_SCOPE",
    ["email offline_access " "https://management.azure.com/user_impersonation"],
)
SOCIAL_AUTH_AZURE_SCOPE_APP = env.json(
    "AZUREAD_OAUTH2_SCOPE_APP",
    {
        "management": ["https://management.azure.com/.default"],
        "storage": ["https://storage.azure.com/.default"],
    },
)

http_cache = f"/tmp/{seqslab.name}.{seqslab.__version__}.http_cache"
try:
    with open(http_cache, "rb") as f:
        persisted_http_cache = pickle.load(f)  # Take a snapshot
except (
    FileNotFoundError,
    pickle.UnpicklingError,  # A corrupted http cache file
):
    persisted_http_cache = {}  # Recover by starting afresh

atexit.register(
    lambda: pickle.dump(
        # When exit, flush it back to the file.
        # It may occasionally overwrite another process's concurrent write,
        # but that is fine. Subsequent runs will reach eventual consistency.
        persisted_http_cache,
        open(http_cache, "wb"),
    )
)

Client = TypeVar("Client", bound=msal.ClientApplication)


class AuthBaseModel(BaseModel):
    class Config:
        arbitrary_types_allowed = True


class ClientApp(AuthBaseModel):
    public_app: msal.ClientApplication = None
    confidential_app: msal.ClientApplication = None

    def load_client(self, credential: str = None, tenant: str = None) -> Client:
        proxies = context.get_context().args.proxy
        if credential:
            if not self.confidential_app:
                self.confidential_app = msal.ConfidentialClientApplication(
                    SOCIAL_AUTH_AZURE_KEY,
                    client_credential=credential,
                    authority=f"https://login.microsoftonline.com/{tenant}",
                    app_name=seqslab.name,
                    app_version=seqslab.__version__,
                    proxies=proxies,
                    http_cache=persisted_http_cache,
                )
            return self.confidential_app
        else:
            if not self.public_app:
                self.public_app = msal.PublicClientApplication(
                    SOCIAL_AUTH_AZURE_KEY,
                    authority=f"https://login.microsoftonline.com/{SOCIAL_AUTH_AZURE_TENANT_ID}",
                    app_name=seqslab.name,
                    app_version=seqslab.__version__,
                    proxies=proxies,
                    http_cache=persisted_http_cache,
                )
            return self.public_app


app = ClientApp()


class _AuthCodeHandlerEx(_AuthCodeHandler):
    def do_POST(self):
        clen = int(self.headers.get("Content-Length"))
        body = self.rfile.read(clen)
        qs = parse_qs(body.decode("utf-8"))
        if qs.get("code") or qs.get("error"):
            self.server.auth_response = _qs2kv(qs)
            template = (
                self.server.success_template
                if "code" in qs
                else self.server.error_template
            )
            self._send_full_response(
                template.safe_substitute(**self.server.auth_response)
            )
            # NOTE: Don't do self.server.shutdown() here. It'll halt the server.
        else:
            self._send_full_response(self.server.welcome_page)


class AuthCodeReceiverEx(AuthCodeReceiver):
    def __init__(self, port=None):
        """
        Create a Receiver waiting for incoming auth response.
        Note that this constructor is exactly the same as super class
        except we use own handler to do post with id_token auth response.
        """
        super(AuthCodeReceiverEx, self).__init__(port=port)
        address = "127.0.0.1"
        Server = _AuthCodeHttpServer6 if ":" in address else _AuthCodeHttpServer
        self._server = Server((address, port or 0), _AuthCodeHandlerEx)
