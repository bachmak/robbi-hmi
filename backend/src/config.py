import os


def _get_from_env(var_name):
    try:
        return os.environ[var_name]
    except KeyError:
        raise RuntimeError(f"Environment varialbe {var_name} not set.")


class db:
    def url(): return _get_from_env("DB_URL")
    def token(): return _get_from_env("DB_TOKEN")
    def org(): return _get_from_env("DB_ORG")
    def bucket_robot(): return _get_from_env("DB_BUCKET_ROBOT")


class opc_ua:
    def url(): return _get_from_env("OPC_UA_URL")
    def url_fallback(): return _get_from_env("OPC_UA_URL_FALLBACK")


class robot:
    def left_wheel_radius(): return 0.05
    def right_wheel_radius(): return 0.05
    def wheelbase(): return 0.15
