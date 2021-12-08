# search in the dataframe
# need to be case insensitive
# should count every substring
# if it can't find something in the catalog it should search in dbpedia

def search(keyword, Dataframe):
    search = '|'.join(keyword)
    searched_Des = Dataframe.loc[Dataframe['Description'].str.contains(search, na=False)].copy()
    searched_Ab_en = Dataframe.loc[Dataframe['Abstract_en'].str.contains(search, na=False)].copy()
    searched = searched_Des.append(searched_Ab_en)
    #searched = Dataframe
    searched['sum'] = searched['Description'].str.contains(search, regex=False).astype(float) + \
                      searched['Name'].str.contains(search, regex=False).astype(float) + \
                      searched['IT Category'].str.contains(search, regex=False).astype(float) + \
                      searched['ApplicationCategory'].str.contains(search, regex=False).astype(float)+ \
                      searched['Abstract_en'].str.contains(search, regex=False).astype(float)+ \
                      searched['Abstract_de'].str.contains(search, regex=False).astype(float)
    ranked_search = searched.sort_values("sum", ascending=False)
    ranked_search = ranked_search.reset_index(inplace=False)
    out = ranked_search[['Name', 'IT Category', 'Description',  'Abstract_de', 'sum']]
    #out.append (ranked_search['first_uri'])
    #print(out)
    return out