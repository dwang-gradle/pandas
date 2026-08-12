import os

from develocity.config import from_properties_file, in_gradle_user_home


def develocity_configuration(config):
    # URL: from env if provided, else the unstable-release instance. `or` treats
    # an empty value (e.g. an undefined GitHub Actions var) as unset.
    url = os.environ.get("DEVELOCITY_URL") or "https://dv-helm-cluster-unstable-release.grdev.net"
    config.develocity_url = url
    config.allow_insecure_protocol = url.startswith("http://")

    # Auth:
    #   - If DEVELOCITY_ACCESS_KEY (host=key) is set, the agent reads it automatically.
    #   - Otherwise, reuse the key in ~/.gradle/develocity/keys.properties.
    if not os.environ.get("DEVELOCITY_ACCESS_KEY"):
        config.access_key = from_properties_file(in_gradle_user_home())

    # --- Artifact Cache experiment (step 2) ---
    # Identify these builds for future discovery.
    config.tags.add("ac-step-2")
    # Attach Artifact Cache restore metrics to the build for later analysis.
    capture_artifact_cache_metrics(config)
    return config


def capture_artifact_cache_metrics(config):
    pip_cache_dir = os.environ.get("PIP_CACHE_DIR")
    if not pip_cache_dir:
        return

    metrics_file = os.path.join(
        pip_cache_dir,
        ".develocity",
        "artifact-cache",
        "restore",
        "metrics.properties",
    )
    if not os.path.isfile(metrics_file):
        return

    from develocity.properties import parse_properties

    with open(metrics_file, encoding="utf-8") as f:
        metrics = parse_properties(f.read())

        for key, value in metrics.items():
            if value == "":
                config.tags.add(key)
            else:
                config.custom_values[key] = value
