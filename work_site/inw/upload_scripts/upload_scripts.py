import pandas as pd


def handle_uploaded(file):
    files = file

    if len(files['file[0]']) > len(files['file[1]']):
        return files['file[0]'], files['file[1]']
    else:
        return files['file[1]'], files['file[0]']


def excel_inf_to_list(excel,dict_sap):
    sap = dict_sap
    df_inw = excel
    list_inw = df_inw.iloc[:, 0].tolist()
    if 'START' in sap['Krótki tekst materiału'][0] or 'KARTA' in sap['Krótki tekst materiału'][0]:
        new_list = ['89480' + str(x) for x in list_inw]
        new_list_int = [int(x) for x in new_list]
        return new_list_int
    else:
        list_int = [int(x) for x in list_inw]
        return list_int


def excel_sap_to_dict(excel):
    df_sap = excel
    dict_sap = dict()
    accept_list = ['Krótki tekst materiału', 'Numer Seryjny', 'EAN', 'Zapas ogółem']
    for col in df_sap.columns:
        if col in accept_list:
            if col == 'EAN':
                dict_sap[col] = [None if pd.isna(value) else int(value) for value in df_sap[col].values]
            else:
                dict_sap[col] = df_sap[col].values.tolist()
                if col == 'Zapas ogółem':
                    licznik = -1
                    for value in dict_sap['Zapas ogółem']:
                        licznik += 1
                        dict_sap['Zapas ogółem'][licznik] = int(-1 * (value))
    return dict_sap

def process_excel_files(inw, sap):
    sap = sap
    inw = inw
    if 'START' in sap['Krótki tekst materiału'][0] or 'KARTA' in sap['Krótki tekst materiału'][0]:
        sap['EAN'] = sap.pop('Numer Seryjny')
        sap['Zapas ogółem'] = [-1 for x in sap['EAN']]
    for value in inw:
        if value in sap['EAN']:
            index = sap['EAN'].index(value)
            sap['Zapas ogółem'][index] += 1
        else:
            if 'START' in sap['Krótki tekst materiału'][0] or 'KARTA' in sap['Krótki tekst materiału'][0]:
                str_value = '89480' + str(value)
                int_value = int(str_value)
                sap['EAN'].append(int_value)
            else:
                sap['EAN'].append(value)
            sap['Krótki tekst materiału'].append(None)
            sap['Zapas ogółem'].append(1)
    return sap
