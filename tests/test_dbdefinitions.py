import os
from unittest.mock import patch
from DBDefinitions import ComposeConnectionString


def test_compose_connection_string_default_values():
    with patch.dict(os.environ, {}, clear=True):
        conn_string = ComposeConnectionString()
        assert conn_string == "postgresql+asyncpg://postgres:example@localhost:5432/data"


def test_compose_connection_string_custom_values():
    custom_env = {
        "POSTGRES_USER": "custom_user",
        "POSTGRES_PASSWORD": "custom_password",
        "POSTGRES_DB": "custom_db",
        "POSTGRES_HOST": "custom_host:1234"
    }
    with patch.dict(os.environ, custom_env, clear=True):
        conn_string = ComposeConnectionString()
        assert conn_string == "postgresql+asyncpg://custom_user:custom_password@custom_host:1234/custom_db"
