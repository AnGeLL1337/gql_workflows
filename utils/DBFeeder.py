import uuid

from DBDefinitions import (
    AuthorizationModel,
    AuthorizationGroupModel,
    AuthorizationRoleTypeModel,
    AuthorizationUserModel
)


def get_demodata():
    def datetime_parser(json_dict):
        for (key, value) in json_dict.items():
            if key in ["startdate", "enddate", "lastchange", "created"]:
                if value is None:
                    dateValueWOtzinfo = None
                else:
                    try:
                        dateValue = datetime.datetime.fromisoformat(value)
                        dateValueWOtzinfo = dateValue.replace(tzinfo=None)
                    except:
                        print("jsonconvert Error", key, value, flush=True)
                        dateValueWOtzinfo = None

                json_dict[key] = dateValueWOtzinfo

            if (key in ["id", "changedby", "createdby"]) or ("_id" in key):

                if value not in ["", None]:
                    json_dict[key] = uuid.UUID(value)
                else:
                    print(key, value)

        return json_dict

    with open("./systemdata.json", "r", encoding="utf-8") as f:
        jsonData = json.load(f, object_hook=datetime_parser)

    return jsonData


import os
import json
from uoishelpers.feeders import ImportModels
import datetime
'''
def get_demodata():
    def datetime_parser(json_dict):
        for (key, value) in json_dict.items():
            if key in ["startdate", "enddate", "lastchange", "created"]:
                if value is None:
                    dateValueWOtzinfo = None
                else:
                    try:
                        dateValue = datetime.datetime.fromisoformat(value)
                        dateValueWOtzinfo = dateValue.replace(tzinfo=None)
                    except:
                        print("jsonconvert Error", key, value, flush=True)
                        dateValueWOtzinfo = None
                
                json_dict[key] = dateValueWOtzinfo
        return json_dict


    with open("./systemdata.json", "r",encoding="UTF-8") as f:
        jsonData = json.load(f, object_hook=datetime_parser)

    return jsonData
    '''

async def initDB(asyncSessionMaker):

    defaultNoDemo = "False"
    if defaultNoDemo == os.environ.get("DEMO", "True"):
        dbModels = [
            AuthorizationModel,
            AuthorizationGroupModel,
            AuthorizationRoleTypeModel,
            AuthorizationUserModel
        ]
    else:
        dbModels = [
            AuthorizationModel,
            AuthorizationGroupModel,
            AuthorizationRoleTypeModel,
            AuthorizationUserModel
        ]

    jsonData = get_demodata()
    await ImportModels(asyncSessionMaker, dbModels, jsonData)
    pass