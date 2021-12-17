# search in the dataframe
# need to be case insensitive
# should count every substring
# if it can't find something in the catalog it should search in dbpedia
import pandas as pd

data2 = pd.read_excel('output.xlsx', index_col=0)  
#print(data2)


def search(keyword, Dataframe):
    search = '|'.join(keyword)
    search = search.lower()
    for i in Dataframe.index:
        try:
            Dataframe.loc[Dataframe.index[i],'Description_search'] = Dataframe.loc[Dataframe.index[i],'Description'].lower()
            Dataframe.loc[Dataframe.index[i],'Abstract_en_search'] = Dataframe.loc[Dataframe.index[i],'Abstract_en'].lower()
            Dataframe.loc[Dataframe.index[i],'Abstract_de_search'] = Dataframe.loc[Dataframe.index[i],'Abstract_de'].lower()
        except:
            Dataframe.loc[Dataframe.index[i], 'Description_search'] = str('NaN')
            Dataframe.loc[Dataframe.index[i],'Abstract_en_search'] = str('NaN')
            Dataframe.loc[Dataframe.index[i],'Abstract_de_search'] = str('NaN')
    searched_Des = Dataframe.loc[Dataframe['Description_search'].str.contains(search, na=False)].copy()
    searched_Ab_en = Dataframe.loc[Dataframe['Abstract_en_search'].str.contains(search, na=False)].copy()
    searched_Ab_de = Dataframe.loc[Dataframe['Abstract_de_search'].str.contains(search, na=False)].copy()
    searched = pd.concat([searched_Des, searched_Ab_en, searched_Ab_de]).drop_duplicates().reset_index(drop=True)
    #searched = Dataframe
    for i in searched.index:
        try:
            searched.loc[searched.index[i],'Name_rank'] = searched.loc[searched.index[i],'Name'].lower()
            searched.loc[searched.index[i],'IT Category_rank'] = searched.loc[searched.index[i],'IT Category'].lower()
            searched.loc[searched.index[i],'ApplicationCategory_rank'] = searched.loc[searched.index[i],'ApplicationCategory'].lower()
        except:
            x = 1
    for i in searched.index:
        searched.loc[searched.index[i],'sum'] = searched.loc[searched.index[i],'Description_search'].count(search) + \
            searched.loc[searched.index[i],'Abstract_en_search'].count(search) + \
                searched.loc[searched.index[i],'Abstract_de_search'].count(search) +\
                    searched.loc[searched.index[i],'Name_rank'].count(search) +\
                        searched.loc[searched.index[i],'IT Category_rank'].count(search) +\
                            searched.loc[searched.index[i],'ApplicationCategory_rank'].count(search)
    try:
        ranked_search = searched.sort_values("sum", ascending=False)
    except:
        print('pleas try another search')
    ranked_search = ranked_search.reset_index(inplace=False)
    out = ranked_search[['Name', 'IT Category', 'Description',  'Abstract_de', 'sum']]
    #out.append (ranked_search['first_uri'])
    #print(out)
    return out

def filter_category (keyword, Dataframe):
    temp = Dataframe
    for index, row in temp.iterrows():
        if row['IT Category'] == keyword:
            temp.drop(index, inplace=True)
    #print(searched_Des)
    out = temp[['Name', 'IT Category']]
    return (out)
