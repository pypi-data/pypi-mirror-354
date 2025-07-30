import logging
import re
from importlib.metadata import metadata, PackageNotFoundError
from typing import Annotated

import markdown

from jetbrains_plugin_server.config import FAST_API_OFFLINE
from jetbrains_plugin_server.schemas import PluginSchema

if FAST_API_OFFLINE:
    from fastapi_offline import FastAPIOffline as FastAPI
else:
    from fastapi import FastAPI  # type: ignore

from fastapi.responses import HTMLResponse, Response

from jetbrains_plugin_server.plugin_catalog import get_plugin_catalog
from jetbrains_plugin_server.plugin_model import get_plugins
from jetbrains_plugin_server.to_xml import to_xml

LOG = logging.getLogger(__name__)


def create_app():
    app = FastAPI()

    @app.get("/")
    def get_plugins_route(build: Annotated[
        str, "IDE build number to filter the available plugins and return only the compatible ones"] = ""):
        if not build:
            md = "# Jetbrains plugin server\n\n"
            try:
                md += metadata("jetbrains-plugin-server")["description"]
                md = re.sub(r"- `(/[^`]*)`", r"- [`\1`](\1)", md)
            except PackageNotFoundError:
                pass
            return HTMLResponse(content=markdown.markdown(md))

        LOG.debug("Request with build=%s", build)
        result = get_plugins(build)
        return Response(content=to_xml(result), media_type="application/xml")

    @app.get("/cache")
    def get_cache_route():
        return get_plugin_catalog()

    @app.get("/packages")
    def get_packages_route():
        catalog = get_plugin_catalog()
        md = "# Packages\n"
        md += "\n".join(f"- [{p.name}](/packages/{p.versions[0].plugin_id})" for p in catalog.plugins)
        md += "\n\n [Previous page](/)"
        return HTMLResponse(content=markdown.markdown(md))

    @app.get("/packages/{plugin_id}")
    def get_package_route(plugin_id: str):
        catalog = get_plugin_catalog()
        plugin: PluginSchema = next(p for p in catalog.plugins if p.versions[0].plugin_id == plugin_id)
        md = f"# Package {plugin.name}\n"
        md += "\n".join(
            f"- [{v.version}](/packages/{plugin_id}/{v.version}) "
            f"compatible with IDE version in `[{v.specs.since_build} ; {v.specs.until_build}]`"
            for v in plugin.versions
        )
        md += "\n\n [Previous page](/packages)"
        return HTMLResponse(content=markdown.markdown(md))

    return app
