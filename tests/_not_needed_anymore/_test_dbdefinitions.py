import pytest
import sqlalchemy
import sys
import asyncio
import os

from DBDefinitions import startEngine


from DBDefinitions import (
    BaseModel,
    AuthorizationModel,
    AuthorizationUserModel,
    AuthorizationRoleTypeModel,
    AuthorizationGroupModel,
    WorkflowModel,
    WorkflowStateModel,
    WorkflowTransitionModel,
    WorkflowStateUserModel,
    WorkflowStateRoleTypeModel,
)

from shared import prepare_demodata, prepare_in_memory_sqllite, get_demodata


@pytest.mark.asyncio
async def test_load_demo_data():
    async_session_maker = await prepare_in_memory_sqllite()
    await prepare_demodata(async_session_maker)
    # data = get_demodata()


def test_connection_string():
    from DBDefinitions import ComposeConnectionString
    connection_string = ComposeConnectionString()

    assert "://" in connection_string


@pytest.mark.asyncio
async def test_table_start_engine():
    connection_string = "sqlite+aiosqlite:///:memory:"
    async_session_maker = await startEngine(
        connection_string, makeDrop=True, makeUp=True
    )

    assert async_session_maker is not None


from utils.DBFeeder import initDB


@pytest.mark.asyncio
async def test_initDB():
    connection_string = "sqlite+aiosqlite:///:memory:"
    async_session_maker = await startEngine(
        connection_string, makeDrop=True, makeUp=True
    )

    assert async_session_maker is not None
    await initDB(async_session_maker)