import os


def _get_from_env(var_name):
    try:
        return os.environ[var_name]
    except KeyError:
        raise RuntimeError(f"Environment varialbe {var_name} not set.")


def get_db_url(): return _get_from_env("DB_URL")


def get_db_token(): return _get_from_env("DB_TOKEN")


def get_db_org(): return _get_from_env("DB_ORG")
