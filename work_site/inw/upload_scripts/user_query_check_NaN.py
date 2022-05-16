
def check_NaN(query):
    user_query = query
    try:
        name = user_query.latest('name')
        name = 'Inwentaryzacja' + str(name.id + 1)
        return name
    except:
        return 'Inwentaryzacja'