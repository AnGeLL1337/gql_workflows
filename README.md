# GQL_WorkFlow
## Zadání
* Entity (AuthorizationGQLModel, AuthorizationUserGQLMode, AuthorizationGroupGQLModel, AuthorizationRoleTypeGQLModel)
* Modely v databázi pomocí SQLAlchemy, API endpoint typu GraphQL s pomocí knihovny Strawberry.
* Přístup k databázi řešte důsledně přes AioDataloder, resp. (https://github.com/hrbolek/uoishelpers/blob/main/uoishelpers/dataloaders.py).
* Zabezpečte kompletní CRUD operace nad entitami ExternalIdModel, ExternalIdTypeModel, ExternalIdCategoryModel
* CUD operace jako návratový typ nejméně se třemi prvky id, msg a „entityresult“ (pojmenujte adekvátně podle dotčené entity), vhodné přidat možnost nadřízené entity, speciálně pro operaci D.
* Řešte autorizaci operací (permission classes).
* Kompletní CRUD dotazy na GQL v souboru externalids_queries.json (dictionary), jméno klíče nechť vhodně identifikuje operaci, hodnota je dictionary s klíči query (obsahuje parametrický dotaz) nebo mutation (obsahuje parametrické mutation) a variables (obsahuje dictionary jako testovací hodnoty).
* Kompletní popisy API v kódu (description u GQLModelů) a popisy DB vrstvy (comment u DBModelů).
* Zabezpečte více jak 90% code test coverage (standard pytest).
## Plán postupu
* 16.10. - příprava na 1. projektový den, vytvořený GitHub repository, zprovozněný Docker
* 23.10. - 26.11. - bližší seznámení s projektem, porozuměmní technikám, příprava na 2. projektový den, příprava RU operací
* 27.11. - prezentace postupu na 2. projektovém dnu

```bash
pytest --cov-report term-missing --cov=DBDefinitions --cov=GraphTypeDefinitions --cov=utils --log-cli-level=INFO -x
```

```bash
uvicorn main:app --env-file environment.txt --reload
```

```bash
git push origin refs/heads/latest:refs/heads/latest
```

```
DEMO=True
DEMOUSER={"id": "2d9dc5ca-a4a2-11ed-b9df-0242ac120003", "name": "John", "surname": "Newbie"}
JWTPUBLICKEY=http://localhost:8000/oauth/publickey
JWTRESOLVEUSERPATH=http://localhost:8000/oauth/userinfo
GQLUG_ENDPOINT_URL=http://localhost:8000/gql
```

Pytest coverage report
```text
---------- coverage: platform win32, python 3.10.5-final-0 -----------
Name                                                    Stmts   Miss  Cover   Missing
-------------------------------------------------------------------------------------
DBDefinitions\AuthorizationGroupModel.py                   15      0   100%
DBDefinitions\AuthorizationModel.py                         8      0   100%
DBDefinitions\AuthorizationRoleTypeModel.py                16      0   100%
DBDefinitions\AuthorizationUserModel.py                    16      0   100%
DBDefinitions\WorkflowModel.py                             15      0   100%
DBDefinitions\WorkflowStateModel.py                        16      0   100%
DBDefinitions\WorkflowStateRoleTypeModel.py                16      0   100%
DBDefinitions\WorkflowStateUserModel.py                    17      0   100%
DBDefinitions\WorkflowTransitionModel.py                   18      0   100%
DBDefinitions\__init__.py                                  41      4    90%   35-38
DBDefinitions\base.py                                       3      0   100%
DBDefinitions\uuid.py                                       7      0   100%
GraphTypeDefinitions\BaseGQLModel.py                       16      2    88%   7, 12
GraphTypeDefinitions\_GraphPermissions.py                  94     52    45%   44, 191-205, 208, 270-273, 298-299, 304, 315, 321-389
GraphTypeDefinitions\_GraphResolvers.py                    61      0   100%
GraphTypeDefinitions\__init__.py                           40      0   100%
GraphTypeDefinitions\authorizationGQLModel.py              59      0   100%
GraphTypeDefinitions\authorizationGroupGQLModel.py        100      0   100%
GraphTypeDefinitions\authorizationRoleTypeGQLModel.py     105      0   100%
GraphTypeDefinitions\authorizationUserGQLModel.py          96      0   100%
GraphTypeDefinitions\externals.py                          19      0   100%
GraphTypeDefinitions\utils.py                               7      0   100%
utils\DBFeeder.py                                          36      1    97%   75
utils\Dataloaders.py                                       76      8    89%   165-168, 474-477
utils\__init__.py                                           2      0   100%
utils\gql_ug_proxy.py                                      38      8    79%   29-31, 39-42, 55
utils\sentinel.py                                           8      0   100%
-------------------------------------------------------------------------------------
TOTAL                                                     945     75    92%
```