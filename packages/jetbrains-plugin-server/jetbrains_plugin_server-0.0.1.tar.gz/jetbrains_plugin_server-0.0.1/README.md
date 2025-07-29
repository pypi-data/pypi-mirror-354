<!--

THIS README FILE IS RENDERED ON '/' ENDPOINT WHEN NO "build" ARG IS GIVEN

-->

# jetbrains-plugin-server

Creates a jetbrains-compatible plugin server with a given list of plugins

## Tools

- `src/tools/dl_data.py` to fetch plugins specifications, versions and content from jetbrains to a local filesystem
- `src/tools/gen_json_cache.py` to build a JSON cache to answer faster, using either a filesystem storage or an
  artifactory
