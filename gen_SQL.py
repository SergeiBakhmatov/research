def generates_sql_query(table, **kwargs):
    sql_query = list()
    sql_query.append("SELECT * FROM %s " % table)
    if kwargs:
        sql_query.append("WHERE " + " AND ".join("%s IN %s" % (k, tuple(v)) for k, v in kwargs.items()))
    sql_query.append(";")
    full_sql_query = "".join(sql_query)
    clear_sql_query = full_sql_query.replace(',)', ')')
    return clear_sql_query

print(generates_sql_query(table="table_user", id=[12,22], name=["qsd", "qwe"], height=[120]))