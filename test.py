import strawberry
from fastapi import FastAPI
from strawberry.asgi import GraphQL
import psycopg2
from psycopg2 import Error
from typing import List, Tuple, Any

@strawberry.type
class User:
    id: int | None
    name: str | None

@strawberry.type
class Item:
    id: int | None
    name: str | None
    height: int | None
    width: int | None

@strawberry.type
class NewItem:
    id: int | None
    name: str | None
    height: int | None
    width: int | None
    price: int | None

async def ex_from_db(table_name: str) -> List[Tuple[Any,]]:
    try:
            connection = psycopg2.connect(
                user="admin", 
                password="root", 
                host="127.0.0.1", 
                port="5432", 
                database="db_postgres"
                )
            cursor = connection.cursor()
            postgreSQL_select_Query = "SELECT * FROM " + table_name

            cursor.execute(postgreSQL_select_Query)

            return cursor.fetchall()
    
    except (Exception, Error) as error:
            print("Ошибка при работе с PostgreSQL", error)
    finally:
            if connection:
                cursor.close()
                connection.close()

@strawberry.type
class QueryA:
    @strawberry.field(description="Return Users")
    async def resolver_users(self) -> List[User]:
         db_data = await ex_from_db(table_name="table_users")

         users = []
         for user in db_data:
              users.append(
                   User(
                        id=user[0], 
                        name=user[1]
                        )
                    )

         return users
    
    @strawberry.field(description="Return Items")
    async def resolver_items(self) -> List[Item]:
         db_data = await ex_from_db(table_name="table_items")

         items = []
         for item in db_data:
              items.append(
                   Item(
                        id=item[0], 
                        name=item[1], 
                        height=item[2], 
                        width=item[3]
                        )
                    )

         return items
    
    @strawberry.field(description="Return New items")
    async def resolver_new_items(self) -> List[NewItem]:
         db_data = await ex_from_db(table_name="table_new_items")

         new_items = []
         for new_item in db_data:
              new_items.append(
                   NewItem(
                        id=new_item[0], 
                        name=new_item[1], 
                        height=new_item[2], 
                        width=new_item[3], 
                        price=new_item[4]
                        )
                    )

         return new_items

schema_a = strawberry.Schema(query=QueryA)

app = FastAPI()

app.add_route("/graphql/a", GraphQL(schema=schema_a))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)




