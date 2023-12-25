"""Пример использования GraphQL с fastAPI"""

import strawberry
from fastapi import FastAPI, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordBearer
from strawberry.fastapi import GraphQLRouter
import psycopg2
from psycopg2 import Error
from typing import List, Tuple, Any, Optional

@strawberry.type
class User:
    """Объект схемы GraphQL User.

    :param id: integer | None - Айди объекта
    :param name: string | None - Имя объекта
    """

    id: int | None
    name: str | None

@strawberry.type
class Item(User):
    """Объект схемы GraphQL Item.

    :param id: integer | None - Айди объекта
    :param name: string | None - Имя объекта
    :param height: integer | None - Высота объекта
    :param width: integer | None - Ширина объекта
    """

    height: int | None
    width: int | None

@strawberry.type
class NewItem(Item):
    price: int | None

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def fake_decode_token(token: str):
     if token == "1234":
        return {"username": "user1"} 
     return None

def get_current_user(token: str = Depends(oauth2_scheme)):
     
     user = fake_decode_token(token)

     if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
     
     return user

def generates_sql_query(table, **kwargs):
    sql_query = list()
    sql_query.append("SELECT * FROM %s " % table)
    if kwargs:
        sql_query.append("WHERE " + " AND ".join("%s IN %s" % (k, tuple(v)) for k, v in kwargs.items()))
    sql_query.append(";")
    full_sql_query = "".join(sql_query)
    clear_sql_query = full_sql_query.replace(',)', ')')
    return clear_sql_query

async def ex_from_db_table_users(
          table_name: str, 
          id_in_db: List[int] = None, 
          name_in_db: List[str] = None
          ) -> List[Tuple[Any,]]:
    try:
            connection = psycopg2.connect(
                user="admin", 
                password="root", 
                host="127.0.0.1", 
                port="5432", 
                database="db_postgres"
                )
            cursor = connection.cursor()

            if id_in_db and name_in_db:
                postgreSQL_select_query = generates_sql_query(table=table_name, id=id_in_db, name=name_in_db)
            elif id_in_db:
                postgreSQL_select_query = generates_sql_query(table=table_name, id=id_in_db)
            elif name_in_db:
                postgreSQL_select_query = generates_sql_query(table=table_name, name=name_in_db)
            else:
                postgreSQL_select_query = generates_sql_query(table=table_name)

            cursor.execute(postgreSQL_select_query)

            return cursor.fetchall()
    
    except (Exception, Error) as error:
            print("Ошибка при работе с PostgreSQL", error)
    finally:
            if connection:
                cursor.close()
                connection.close()

async def ex_from_db_table_items( 
          ids: List[int] = None, 
          names: List[str] = None,
          heights: List[int] = None,
          widths: List[int] = None
          ) -> List[Tuple[Any,]]:
    try:
            connection = psycopg2.connect(
                user="admin", 
                password="root", 
                host="127.0.0.1", 
                port="5432", 
                database="db_postgres"
                )
            cursor = connection.cursor()

            if ids and names and heights and widths:
                postgreSQL_select_Query = "SELECT * FROM table_items WHERE id IN %s AND name IN %s AND height IN %s AND widths IN %s;"
                cursor.execute(postgreSQL_select_Query, (tuple(ids), tuple(names), tuple(heights), tuple(widths)))
            elif ids and names and heights:
                postgreSQL_select_Query = "SELECT * FROM table_items WHERE id IN %s AND name IN %s AND height IN %s;"
                cursor.execute(postgreSQL_select_Query, (tuple(ids), tuple(names), tuple(heights)))
            elif ids and names:
                postgreSQL_select_Query = "SELECT * FROM table_items WHERE id IN %s AND name IN %s;"
                cursor.execute(postgreSQL_select_Query, (tuple(ids), tuple(names)))
            elif ids:
                postgreSQL_select_Query = "SELECT * FROM table_items WHERE id IN %s;"
                cursor.execute(postgreSQL_select_Query, (tuple(ids),))
            elif names:
                postgreSQL_select_Query = "SELECT * FROM table_items WHERE name IN %s;"
                cursor.execute(postgreSQL_select_Query, (tuple(names),))
            elif heights:
                postgreSQL_select_Query = "SELECT * FROM table_items WHERE height IN %s;"
                cursor.execute(postgreSQL_select_Query, (tuple(heights),))
            elif widths:
                postgreSQL_select_Query = "SELECT * FROM table_items WHERE width IN %s;"
                cursor.execute(postgreSQL_select_Query, (tuple(widths),))
            else:
                postgreSQL_select_Query = "SELECT * FROM table_items"
                cursor.execute(postgreSQL_select_Query)

            return cursor.fetchall()
    
    except (Exception, Error) as error:
            print("Ошибка при работе с PostgreSQL", error)
    finally:
            if connection:
                cursor.close()
                connection.close()

@strawberry.type
class Query:
    """Схема запроса GraphQL. \n
        Пример запроса:
            query{
                resolverUsers(ids:[12]){ \n
                    id \n
                    name \n
                }
             }
        Пример ответа:
            {
                "data": {
                    "resolverUsers": [
                        {
                            "id": 12,\n
                            "name": "Dima"
                        }
                    ]
                }
            }
     """
    @strawberry.field(description="Return Users")
    async def resolver_users(
         self, 
         ids: Optional[List[int]] = None,
         names: Optional[List[str]] = None
         ) -> List[User]:
         
         """Запрос на получение объектов User.

         Arguments:
            ids {Optional[List[integer]]} -- Айди требуемых пользователей. \n
            names {Optional[List[string]]} -- Имена требуемых пользователей. \n

         Returns:
            users {List[User]} -- Список пользователей, соответствующий аргументам, иначе полный список пользователей.
         """

         db_data = await ex_from_db_table_users(table_name="table_users", id_in_db=ids, name_in_db=names)

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
    async def resolver_items(
         self, 
         ids: Optional[List[int]] = None,
         names: Optional[List[str]] = None,
         heights: Optional[List[int]] = None,
         widths: Optional[List[int]] = None
         ) -> List[Item]:

         if ids and names and heights and widths:
            db_data = await ex_from_db_table_items(ids=ids, names=names, heights=heights, widths=widths)
         elif ids and names and heights:
            db_data = await ex_from_db_table_items(ids=ids, names=names, heights=heights)
         elif ids and names:
            db_data = await ex_from_db_table_items(ids=ids, names=names)
         elif ids:
            db_data = await ex_from_db_table_items(ids=ids)
         elif names:
            db_data = await ex_from_db_table_items(names=names)
         elif heights:
            db_data = await ex_from_db_table_items(heights=heights)
         elif widths:
            db_data = await ex_from_db_table_items(widths=widths)
         else:
            db_data = await ex_from_db_table_items()

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
         db_data = await ex_from_db_table_items()

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

schema_a = strawberry.Schema(query=Query)
graphql_app = GraphQLRouter(schema=schema_a)

app = FastAPI()
app.include_router(
    graphql_app, 
    prefix="/graphql/a",
    include_in_schema=True, 
    dependencies=[Depends(get_current_user)]
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)




