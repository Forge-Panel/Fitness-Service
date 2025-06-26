import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

from .queries import Query
from .mutations import Mutation

from ..config import config


# class Context(BaseContext):
#     @cached_property
#     def user(self) -> User | None:
#         if not self.request:
#             return None
#
#         authorization = self.request.headers.get("Authorization", None)
#         return authorization_service.authorize(authorization)


def init_graphql(app: FastAPI):
    schema = strawberry.Schema(query=Query, mutation=Mutation)

    graphql_app = GraphQLRouter(schema, graphiql=config.app_debug)
    app.include_router(graphql_app, prefix=f"{config.base_url}api/app/graphql", tags=['GraphQL'])
