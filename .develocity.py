import os

from develocity.config import from_properties_file, in_gradle_user_home


def develocity_configuration(config):
    # URL: from env if provided, else the local instance. `or` treats an
    # empty value (e.g. an undefined GitHub Actions var) as unset.
    url = os.environ.get("DEVELOCITY_URL") or "http://localhost:24200"
    config.develocity_url = url
    config.allow_insecure_protocol = url.startswith("http://")

    # Auth:
    #   - If DEVELOCITY_ACCESS_KEY (host=key) is set, the agent reads it automatically.
    #   - Otherwise, reuse the key in ~/.gradle/develocity/keys.properties.
    if not os.environ.get("DEVELOCITY_ACCESS_KEY"):
        config.access_key = from_properties_file(in_gradle_user_home())
    return config
