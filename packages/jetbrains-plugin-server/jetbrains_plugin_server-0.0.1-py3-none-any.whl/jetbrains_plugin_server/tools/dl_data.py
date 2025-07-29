from requests import get, Session
from requests.adapters import HTTPAdapter, Retry

from jetbrains_plugin_server.config import PLUGINS_DIR, PLUGIN_VERSIONS_DIR, PLUGIN_SPECS_DIR, LOCAL, \
    JETBRAINS_PLUGINS_HOST

PLUGINS: list[str] = [
    "https://plugins.jetbrains.com/plugin/631-python",
    "https://plugins.jetbrains.com/plugin/10080-rainbow-brackets",
    "https://plugins.jetbrains.com/plugin/11938-one-dark-theme",
    "https://plugins.jetbrains.com/plugin/9525--env-files",
    "https://plugins.jetbrains.com/plugin/11938-one-dark-theme",
    "https://plugins.jetbrains.com/plugin/15075-jpa-buddy",
    "https://plugins.jetbrains.com/plugin/9525--env-files-support/",
    "https://plugins.jetbrains.com/plugin/10044-atom-material-icons/",
    "https://plugins.jetbrains.com/plugin/164-ideavim",
    "https://plugins.jetbrains.com/plugin/9792-key-promoter-x",
    "https://plugins.jetbrains.com/plugin/14708-mario-progress-bar",
    "https://plugins.jetbrains.com/plugin/7086-acejump"
]

if __name__ == '__main__':
    s = Session()
    retries = Retry(total=5, backoff_factor=0.1)
    s.mount('https://', HTTPAdapter(max_retries=retries))

    for plugin in PLUGINS:
        print("PLUGIN", plugin)
        plugin = plugin.replace(f"{JETBRAINS_PLUGINS_HOST}/plugin/", "").strip("/")
        plugin_id_int = plugin.split("-", maxsplit=1)[0]

        versions_rep = get(f"{JETBRAINS_PLUGINS_HOST}/plugins/list?pluginId={plugin}")
        LOCAL.joinpath(PLUGIN_SPECS_DIR, f"{plugin_id_int}.xml").write_bytes(
            versions_rep.content
        )

        versions_id_rep = get(f"{JETBRAINS_PLUGINS_HOST}/api/plugins/{plugin_id_int}/updateVersions")
        LOCAL.joinpath(PLUGIN_VERSIONS_DIR, f"{plugin_id_int}.json").write_bytes(
            versions_id_rep.content
        )

        for row in versions_id_rep.json()[:-4:-1]:
            print("   VERSION", row["version"])
            plugin_version_id = row["id"]
            dl = s.get(
                f"{JETBRAINS_PLUGINS_HOST}/plugin/download",
                params={"updateId": plugin_version_id},
                stream=True
            )

            print("   Done in ", dl.elapsed)

            LOCAL.joinpath(PLUGINS_DIR, f"{plugin_version_id}.zip").write_bytes(
                dl.content
            )
