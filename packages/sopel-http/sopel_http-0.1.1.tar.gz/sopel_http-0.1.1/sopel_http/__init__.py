"""sopel-http

https://github.com/half-duplex/sopel-http
Released under the EUPL-1.2
"""

from __future__ import annotations

from threading import Thread
from typing import TYPE_CHECKING
from urllib.parse import urlparse

from flask import Flask
from gevent import monkey
from gevent.pywsgi import WSGIServer
from sopel.config.types import ListAttribute, StaticSection
from sopel.tools import get_logger

if TYPE_CHECKING:
    from typing import List

    from sopel.bot import Sopel

app = Flask(__name__)
LOGGER = get_logger(__name__)
servers: List[Thread] = []

monkey.patch_all()


class HTTPSection(StaticSection):
    bind = ListAttribute("bind", default=["127.0.0.1", "[::1]"])
    """List of address:port pairs to bind to.

    Use "::" to bind to all including public.
    """


def setup(bot: Sopel):
    bot.config.define_section("http", HTTPSection)

    for bind in bot.config.http.bind:
        parsed = urlparse("//" + bind)
        ip = parsed.hostname
        port = parsed.port or 8094

        server = WSGIServer((ip, port), app)
        try:
            server.start()
        except Exception as e:
            LOGGER.error("Couldn't start server: %s", e)
            if port < 1024:
                LOGGER.error(
                    "Ports <1024 can only be used by root. Try a higher port. "
                    "(Do not run Sopel as root!)"
                )
            continue
        LOGGER.info("Server started on %s port %s", ip, port)
        servers.append(server)
        Thread(target=server.serve_forever, name="sopel-http " + bind).start()
    if len(servers) < 1:
        raise Exception("No servers started")


def shutdown(bot: Sopel):
    """Attempt to clean up.

    .. note:: Reloading is not supported and will not function correctly.
    """

    for server in servers:
        server.stop()
