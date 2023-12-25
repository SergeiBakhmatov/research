Main Module Documentation Semi-Auto
=========================

   .. autoclass:: main.User

   .. autoclass:: main.Query

   .. autofunction:: main.Query.resolver_users

Пример запроса GraphQL
----------------------

Заголовок запроса
~~~~~~~~~~~~~~~~~
    {"Authorization": "Bearer TOKEN"}

    Где TOKEN - и тд и тп

Запрос с параметрами
~~~~~~~~~~~~~~~~~~~~
.. code-block:: graphql

    query {
      resolverUsers(ids: [12, 13, 14], names: ["Dima", "Volodya"]) {
        #Параметры, которые необходимы в ответе
        id
        name
      }
    }

Запрос без параметров
~~~~~~~~~~~~~~~~~~~~~
.. code-block:: graphql

    query {
      resolverUsers {
        id
        name
      }
    }

Пример ответа
~~~~~~~~~~~~~
.. code-block::
     
    "data": {
        "resolverUsers": [
          {
            "id": 12,
            "name": "Dima"
          },
          {
            "id": 13,
            "name": "Volodya"
          }
        ]
    }
     