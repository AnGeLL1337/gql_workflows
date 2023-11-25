import sys

# setting path
sys.path.append("../gql_workflow")

# from ..uoishelpers.uuid import UUIDColumn

from DBDefinitions import BaseModel
from DBDefinitions import AuthorizationModel, AuthorizationGroupModel, AuthorizationUserModel, AuthorizationRoleTypeModel
from DBDefinitions import WorkflowModel, WorkflowStateModel, WorkflowStateRoleTypeModel, WorkflowStateUserModel


async def prepare_in_memory_sqllite():
    from sqlalchemy.ext.asyncio import create_async_engine
    from sqlalchemy.ext.asyncio import AsyncSession
    from sqlalchemy.orm import sessionmaker

    asyncEngine = create_async_engine("sqlite+aiosqlite:///:memory:")
    # asyncEngine = create_async_engine("sqlite+aiosqlite:///data.sqlite")
    async with asyncEngine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)

    async_session_maker = sessionmaker(
        asyncEngine, expire_on_commit=False, class_=AsyncSession
    )

    return async_session_maker

from utils.DBFeeder import get_demodata

async def prepare_demodata(async_session_maker):
    data = get_demodata()

    from uoishelpers.feeders import ImportModels

    await ImportModels(
        async_session_maker,
        [           
            AuthorizationModel, 
            AuthorizationGroupModel, 
            AuthorizationUserModel, 
            AuthorizationRoleTypeModel,

            WorkflowModel, 
            WorkflowStateModel, 
            WorkflowStateRoleTypeModel, 
            WorkflowStateUserModel
        ],
        data,
    )


from utils.Dataloaders import createLoaders


async def createContext(asyncSessionMaker):
    return {
        "asyncSessionMaker": asyncSessionMaker,
        "all": await createLoaders(asyncSessionMaker),
    }
