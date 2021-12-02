from rdflib import Graph
from SPARQLWrapper import SPARQLWrapper, JSON, N3
import pandas as pd
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

sparql = SPARQLWrapper('https://dbpedia.org/sparql')


# data = data.drop(columns = 'ID')


# extraction of names of Applications/Devices/Infrastrcture which are running or planned from the excel
# in liste "Name" dürfen nur softwares die runnning or planning no devises.
# import service catalog from github
# path = "https://raw.githubusercontent.com/Giuliano99/HTI/main/IT%20Service%20Katalog.xlsx"
# path = 'IT Service Katalog.csv'
# path1 = 'uri.csv'
def create_dataframe(path, path1):
    data = pd.read_csv(path, sep=';')
    df4 = data
    # clean dataset
    df4 = df4.rename(columns={'Service Status': 'ServiceStatus'})
    df4 = df4.rename(columns={'Service Type': 'ServiceType'})
    # print(df4)
    # drop all unnecesary columns
    df4 = df4[df4.ServiceStatus != 'Canceled']
    df4 = df4[df4.ServiceStatus != 'Retired']
    df4 = df4[df4.ServiceStatus != 'Retiring']
    df4 = df4[df4.ServiceType != 'Devices']
    df4 = df4[df4.ServiceType != 'Infrastructure']
    existing_solutions = df4['Name']
    df4 = df4.set_index('Name')

    # Combine with manually searched Uris
    uri = pd.read_csv(path1, sep=';')
    uri = uri.set_index('Name')
    df5 = pd.concat([df4, uri], axis=1, sort=False)
    return df5

#
# path_serviceCatalog = "https://raw.githubusercontent.com/Giuliano99/HTI/test/IT%20Service%20Katalog.csv"
# path_uri = "https://raw.githubusercontent.com/Giuliano99/HTI/test/uri.csv"
#
# serviceCatalog = pd.read_csv(path_serviceCatalog)
# uri = pd.read_csv(path_uri)

#df = create_dataframe(serviceCatalog, uri)
df = create_dataframe('IT Service Katalog.csv', 'uri.csv')
df = df.reset_index(inplace=False)


# print (df)

# extracting existing softwares
# solutions_software = []
# for name in existing_solutions:
#    solutions_software.append (name)

# print (solutions_software)


# Finding the URI and the real Name of the Application if it is on Wiki
def append_DBpedia_uri(Names):
    columns = ['name_after', 'uri']
    uris = pd.DataFrame(data=None, columns=columns)
    global data
    # software = '?s1 a <http://dbpedia.org/ontology/Software>. ?s1 a <http://dbpedia.org/ontology/Software>.'
    for Name in Names:
        sparql.setQuery(f'''
      define input:ifp "IFP_OFF"  select ?s1 as ?uri, (bif:search_excerpt (bif:vector ('{Name}'), ?o1)) as ?search, ?sc, ?rank, ?g 
      where {{{{ select ?s1, (?sc * 3e-1) as ?sc, ?o1, (sql:rnk_scale (<LONG::IRI_RANK> (?s1))) as ?rank, ?g where  
  {{ 
    quad map virtrdf:DefaultQuadMap 
    {{ 
      graph ?g 
      {{ 
        ?s1 ?s1textp ?o1 .
        ?o1 bif:contains  '"{Name}"'  option (score ?sc)  .

      }}
    }}
  }}
  order by desc (?sc * 3e-1 + sql:rnk_scale (<LONG::IRI_RANK> (?s1)))  limit 1  offset 0 }}}}''')
        sparql.setReturnFormat(JSON)
        try:
            qres1 = sparql.query().convert()
            # print(qres1)
            try:
                result = qres1['results']['bindings'][0]
                link = result['uri']['value']
            except:
                # print (Name, 'nothing found')
                link = ['NaN']
        except:
            print(Name, 'quiere wrong!')
            link = ['NaN']

        # print(link.count('/'))
        # x = link.split('/')
        # URI = x[4]
        df3 = pd.DataFrame({"name_after": [Name], "uri": [link]})
        #
        uris = uris.append(df3, ignore_index=True)
        # print(Name, link)
    return uris


# versuch für Zoom und SAP
# Name= ['Zoom', 'SAP ERP', 'Skype']
# solutions_software = ['SAP ERP', 'SEAL systems', 'OpenText ECM', 'Intranet', 'Business Intelligence', 'Microsoft Windows', 'Microsoft Office']
# print(df2)

# uris which had do be search manually
# print(df5)


# export excel for checking and improve names


# df5.to_excel("output3.xlsx")

# search in the dataframe
# need to be case insensitive
# should count every substring
# if it can't find something in the catalog it should search in dbpedia
def search(keyword, Dataframe):
    search = '|'.join(keyword)
    searched = Dataframe.loc[Dataframe['Description'].str.contains(search, na=False)].copy()
    searched['sum'] = searched['Description'].str.contains(search, regex=False).astype(int) + \
                      searched['Name'].str.contains(search, regex=False).astype(int) + \
                      searched['IT Category'].str.contains(search, regex=False).astype(int) + \
                      searched['ApplicationCategory'].str.contains(search, regex=False).astype(int)
    ranked_search = searched.sort_values("sum", ascending=False)
    ranked_search = ranked_search.reset_index(inplace=False)
    out = ranked_search[['Name', 'IT Category', 'first_uri',  'Second_uri']]
    #out.append (ranked_search['first_uri'])
    #print(out)
    return out


#print(search(['BIM'], df))

df6 = df
uri = df6.iloc[0]['first_uri']
#print(uri)
# Extraction of all data contained in dbpedia that can be used for our website in englisch for Softwares
# here the genre, abstract, and other important data should be added to the df
def append_DBpedia_data(df):
    for i in df.index:
        uri = df.iloc[i]['first_uri']
        sparql.setQuery(f'''
        SELECT *
        WHERE
        {{<{uri}> a ?class;
        dbo:genre ?genre ;
        dbo:abstract ?abstract ;
        rdfs:label ?label .
        FILTER (lang(?abstract) = 'en')
        FILTER (lang(?label) = 'en')
        }}''')
        sparql.setReturnFormat(JSON)
        print (uri)
        qres2 = sparql.query().convert()
        print(qres2)
        for result in qres2['results']['bindings']:
            # print(result['object'])
            genre, abstract, lable = result['genre']['value'], result['abstract']['value'], result['label']['value']
            #print(f'genre: {genre}\tAbstrect: {abstract}\tValue:{lable}')
            # if lang == 'en':
            # print(value)
#uris = ['http://dbpedia.org/resource/Zoom_(software)', 'http://dbpedia.org/resource/SAP_ERP']
test = df6.truncate(before=0, after=3)
print(test)
append_DBpedia_data(test)


# # check if result from DBpedia is existing in the service catalog
#
# test = 'SAP'
#
# sparql = SPARQLWrapper('https://dbpedia.org/sparql')
# sparql.setQuery('''
#   SELECT ?lable
#     WHERE { dbr:SAP rdfs:label ?lable .
#      FILTER (lang(?lable) = 'en')
# }''')
# sparql.setReturnFormat(JSON)
# qres = sparql.query().convert()
#
# # get company name from DBpedia query
# temp1 = qres.get('results')
# temp2 = temp1.get('bindings')
# temp3 = temp2[0]
# temp4 = temp3.get('lable')
# company_name = temp4.get('value')
# #print(f"Company Name: {company_name}")
#
# # check if solution exists in service catalog
# existing = False
# for index, value in existing_solutions.items():
#     if value == company_name:
#         existing = True
#
# #print(f"In service catalog: {existing}")
#
# sparql = SPARQLWrapper('https://dbpedia.org/sparql')
# sparql.setQuery('''
#     SELECT ?lable ?abstract ?genre ?image
#     WHERE { dbr:Microsoft_Teams rdfs:label ?lable .
#             dbr:Microsoft_Teams dbo:abstract ?abstract .
#             dbr:Microsoft_Teams dbo:genre ?genre .
#             dbr:Microsoft_Teams dbp:logo ?image.
#             FILTER (lang(?lable) = 'en')
#             FILTER (lang(?abstract) = 'en') }
# ''')
# sparql.setReturnFormat(JSON)
# qres = sparql.query().convert()
#
# #print(qres)
# for result in qres['results']['bindings']:
#     # print(result['object'])
#
#     lang, value, value2 = result['lable']['xml:lang'], result['abstract']['value'], result['genre']['value']
#     #print(f'Lang: {lang}\tValue: {value}\tValue:{value2}')
#     # if lang == 'en':
#     # print(value)
