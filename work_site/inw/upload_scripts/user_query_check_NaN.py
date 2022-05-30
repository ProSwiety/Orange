def check_NaN(query, name):
    user_query = query
    check_name = name
    if 'START' in check_name['Krótki tekst materiału'][0]:
        try:
            name = user_query.latest('name')
            name = 'Startery' + '#' + str(name.id + 1)
            return name
        except:
            return 'Startery'
    elif 'KARTA' in check_name['Krótki tekst materiału'][0]:
        try:
            name = user_query.latest('name')
            name = 'SIM' + '#' + str(name.id + 1)
            return name
        except:
            return 'SIM'
    else:
        try:
            name = user_query.latest('name')
            name = 'Akcesoria' + '#' + str(name.id + 1)
            return name
        except:
            return 'Akcesoria'