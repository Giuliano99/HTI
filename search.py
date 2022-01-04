# search in the dataframe
# need to be case insensitive
# should count every substring
# if it can't find something in the catalog it should search in dbpedia
from os import sep
import pandas as pd

data2 = pd.read_excel('output.xls', index_col=0)
print(data2)


def search(keyword, Dataframe):
    search = str(keyword)
    if ' ' in search:
        x = search.split(' ')
        search = '|'.join(x)
    search = search.lower()
    #print(search)
    for i in Dataframe.index:
        try:
            Dataframe.loc[Dataframe.index[i],'Name_search'] = Dataframe.loc[Dataframe.index[i],'Name'].lower()
            Dataframe.loc[Dataframe.index[i],'Description_search'] = Dataframe.loc[Dataframe.index[i],'Description'].lower()
            Dataframe.loc[Dataframe.index[i],'Abstract_en_search'] = Dataframe.loc[Dataframe.index[i],'Abstract_en'].lower()
            Dataframe.loc[Dataframe.index[i],'Abstract_de_search'] = Dataframe.loc[Dataframe.index[i],'Abstract_de'].lower()
            Dataframe.loc[Dataframe.index[i],'ApplicationCategory_search'] = Dataframe.loc[Dataframe.index[i],'ApplicationCategory'].lower()
            Dataframe.loc[Dataframe.index[i],'IT Category_search'] = Dataframe.loc[Dataframe.index[i],'IT Category'].lower()
        except:
            Dataframe.loc[Dataframe.index[i],'Name_search'] = str('NaN')
            Dataframe.loc[Dataframe.index[i],'Description_search'] = str('NaN')
            Dataframe.loc[Dataframe.index[i],'Abstract_en_search'] = str('NaN')
            Dataframe.loc[Dataframe.index[i],'Abstract_de_search'] = str('NaN')
            Dataframe.loc[Dataframe.index[i],'ApplicationCategory_search'] = str('NaN')
            Dataframe.loc[Dataframe.index[i],'IT Category_search'] = str('NaN')
    searched_Name = Dataframe.loc[Dataframe['Name_search'].str.contains(search, na=False)].copy()
    #print(searched_Name)
    searched_Des = Dataframe.loc[Dataframe['Description_search'].str.contains(search, na=False)].copy()
    #print(searched_Des)
    searched_Ab_en = Dataframe.loc[Dataframe['Abstract_en_search'].str.contains(search, na=False)].copy()
    #print(searched_Ab_en)
    searched_Ab_de = Dataframe.loc[Dataframe['Abstract_de_search'].str.contains(search, na=False)].copy()
    #print(searched_Ab_de)
    searched_AC = Dataframe.loc[Dataframe['ApplicationCategory_search'].str.contains(search, na=False)].copy()
    #print(searched_AC)
    searched_ITC = Dataframe.loc[Dataframe['IT Category_search'].str.contains(search, na=False)].copy()
    #print(searched_ITC)
    searched = pd.concat([searched_Name, searched_Des, searched_Ab_en, searched_Ab_de, searched_AC, searched_ITC]).drop_duplicates().reset_index(drop=True)
    if '|' not in search:
        for i in searched.index:
            searched.loc[searched.index[i],'sum'] = searched.loc[searched.index[i],'Description_search'].count(search) + \
                searched.loc[searched.index[i],'Abstract_en_search'].count(search) + \
                    searched.loc[searched.index[i],'Abstract_de_search'].count(search) +\
                        searched.loc[searched.index[i],'Name_search'].count(search) +\
                            searched.loc[searched.index[i],'IT Category_search'].count(search) +\
                                searched.loc[searched.index[i],'ApplicationCategory_search'].count(search)
    else:
        number_of_splits = search.count('|')
        x = search.split('|')
        search1 = x[number_of_splits]
        search2 = x[number_of_splits - number_of_splits]            
        for i in searched.index:
            searched.loc[searched.index[i],'sum1'] = searched.loc[searched.index[i],'Description_search'].count(search1) + \
                searched.loc[searched.index[i],'Abstract_en_search'].count(search1) + \
                    searched.loc[searched.index[i],'Abstract_de_search'].count(search1) +\
                        searched.loc[searched.index[i],'Name_search'].count(search1) +\
                            searched.loc[searched.index[i],'IT Category_search'].count(search1) +\
                                searched.loc[searched.index[i],'ApplicationCategory_search'].count(search1)
        for i in searched.index:
            searched.loc[searched.index[i],'sum2'] = searched.loc[searched.index[i],'Description_search'].count(search2) + \
                searched.loc[searched.index[i],'Abstract_en_search'].count(search2) + \
                    searched.loc[searched.index[i],'Abstract_de_search'].count(search2) +\
                        searched.loc[searched.index[i],'Name_search'].count(search2) +\
                            searched.loc[searched.index[i],'IT Category_search'].count(search2) +\
                                searched.loc[searched.index[i],'ApplicationCategory_search'].count(search2)
        for i in searched.index:
            searched.loc[searched.index[i],'sum'] = searched.loc[searched.index[i],'sum1'] + searched.loc[searched.index[i],'sum2']

    try:
        ranked_search = searched.sort_values("sum", ascending=False)
        ranked_search = ranked_search.reset_index(inplace=False)
        out = ranked_search[['Name', 'IT Category', 'Description',  'Abstract_de', 'sum']]
        #print (out)
        return out
    except:
        print('Please try another search!')
    

#def filter_category (keyword, Dataframe):
#    temp = Dataframe
#    for index, row in temp.iterrows():
#        if row['IT Category'] == keyword:
#            temp.drop(index, inplace=True)
#    #print(searched_Des)
#    out = temp[['Name', 'IT Category']]
#    return (out)

print(search('BIM', data2))


def filter (Dataframe, Colum, keyword):
    filtert = Dataframe.loc[Dataframe[Colum].str.contains(keyword, na=False)].copy()
    return filtert