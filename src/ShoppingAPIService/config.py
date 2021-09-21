
from dynaconf import Dynaconf

Settings = Dynaconf

# `envvar_prefix` = export envvars with `export DYNACONF_FOO=bar`.
# `settings_files` = Load this files in the order.
settings = Dynaconf(
    envvar_prefix="ShoppingAPIService",
    settings_files=['settings.toml', '.secrets.toml'],
)


def get_settings() -> Settings:
    return settings
