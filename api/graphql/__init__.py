import strawberry
from fastapi import FastAPI, Depends
from strawberry.fastapi import GraphQLRouter
from .queries import Query
from .mutations import Mutation

from ..config import config



def init_graphql(app: FastAPI):
    schema = strawberry.Schema(query=Query, mutation=Mutation)

    graphql_app = GraphQLRouter(schema, graphiql=config.app_debug)
    app.include_router(graphql_app, prefix=f"{config.base_url}api/graphql", tags=['GraphQL'])
