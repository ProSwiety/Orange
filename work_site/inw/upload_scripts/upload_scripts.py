import pandas as pd
def excel_inf_to_list(excel):
    df_inw = excel
    list_inw = df_inw.iloc[:, 0].tolist()
    return list_inw

def excel_sap_to_dict(excel):
    df_sap = excel
    dict_sap = dict()
    accept_list = ['Krótki tekst materiału','EAN','Zapas ogółem']
    for col in df_sap.columns:
        if col in accept_list:
            if col == 'EAN':
                dict_sap[col] = [None if pd.isna(value) else int(value) for value in df_sap[col].values]
            else:
                dict_sap[col] = df_sap[col].values.tolist()
    licznik = -1
    for value in dict_sap['Zapas ogółem']:
        licznik += 1
        dict_sap['Zapas ogółem'][licznik] = int(-1*(value))
    return dict_sap

def process_excel_files(inw,sap):
    inw = inw
    sap = sap
    for value in inw:
        if value in sap['EAN']:
            index = sap['EAN'].index(value)
            sap['Zapas ogółem'][index] += 1
        else:
            sap['EAN'].append(value)
            sap['Krótki tekst materiału'].append(None)
            sap['Zapas ogółem'].append(1)
    for value in sap['Zapas ogółem']:
        if value == 0:
            index = sap['Zapas ogółem'].index(value)
            sap['EAN'].pop(index)
            sap['Krótki tekst materiału'].pop(index)
            sap['Zapas ogółem'].pop(index)
    sap['Nazwa'] = sap['Krótki tekst materiału']
    sap['Ilosc'] = sap['Zapas ogółem']
    del sap['Krótki tekst materiału']
    del sap['Zapas ogółem']
    return sap