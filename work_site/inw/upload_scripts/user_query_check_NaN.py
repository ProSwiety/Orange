
def check_NaN(query):
    user_query = query
    try:
        name = user_query.latest('name')
        name = 'Akcesoria ' + str(name.id + 1)
        return name
    except:
        return 'Akcesoria'