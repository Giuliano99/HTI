#from networkx.algorithms.shortest_paths.weighted import johnson
#import numpy
from rdflib import Graph, Literal, RDF, URIRef
from rdflib.namespace import RDFS
from SPARQLWrapper import SPARQLWrapper, JSON, N3
import pandas as pd
#import rdflib
#import openpyxl

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

df = create_dataframe('IT Service Katalog.csv', 'uri.csv')
df = df.reset_index(inplace=False)
#print (df)

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


# Extraction of all data contained in dbpedia that can be used for our website in englisch for Softwares
# here the genre, abstract, and other important data should be added to the df
def append_DBpedia_data(df):
    for i in df.index:
        g = Graph()
        uri = df.iloc[i]['first_uri']
        try:
            g.parse(uri)
            for s, p, o in g:
                #print(s, p , o)
                if 'abstract' in p:
                    if g.objects(RDFS.label):
                        if o.language == 'en':
                            #print(s, p, o)
                            df.loc[df.index[i], 'Abstract_en'] = str(o)
            for s, p, o in g:
                if 'abstract' in p:
                    if g.objects(RDFS.label):
                        if o.language == 'de':
                            #print(s, p, o)
                            df.loc[df.index[i], 'Abstract_de'] = str(o) 
            for s, p, o in g:
                if 'abstract' in p:
                    if g.objects(RDFS.label):
                        if o.language == 'it':
                            #print(s, p, o)
                            df.loc[df.index[i], 'Abstract_it'] = str(o)
            for s, p, o in g:
                if 'abstract' in p:
                    if g.objects(RDFS.label):
                        if o.language == 'fr':
                            #print(s, p, o)
                            df.loc[df.index[i], 'Abstract_fr'] = str(o)                
            for s, p, o in g:
                if 'depiction' in p:
                    if g.objects(RDFS.label):
                        df.loc[df.index[i], 'Picture'] = str(o)
            for s, p, o in g:
                if 'genre' in p:
                    if g.objects(RDFS.label):
                        df.loc[df.index[i], 'Genre'] = str(o)
        except:
            df.loc[df.index[i], 'Abstract_en'] = str('NaN')
            df.loc[df.index[i], 'Abstract_de'] = str('NaN')
            df.loc[df.index[i], 'Abstract_it'] = str('NaN')
            df.loc[df.index[i], 'Abstract_fr'] = str('NaN')
            df.loc[df.index[i], 'Picture'] = str('NaN')
            df.loc[df.index[i], 'Genre'] = str('NaN')
            print('prase error for', df.iloc[i]['Name'])
    return df

#dbpdf = append_DBpedia_data(df)

#print(dbpdf)
#dbpdf.to_excel("output.xlsx")

data2 = pd.read_excel('output.xlsx', index_col=0)  
#print(data2)

#choose language for abstract
def choose_language(df, Name, label):
    df = df.loc[df['Name'] == Name]
    df = df.set_index('Name')
    comment = None
    if label == 'en':
        x =  df.loc[Name]['Abstract_en']
        if x == 'NaN' or x != str():
            comment ='Sorry, the English abstract is not available.'
            x =  df.loc[Name]['Description']
    if label == 'de':
        x =  df.loc[Name]['Abstract_de']
        if x == 'NaN'or x != str():
            comment = 'Die Deutsche Kurzfassung ist leider nicht verfügbar.'
            x =  df.loc[Name]['Abstract_en']
    if label == 'it':
        x = df.loc[Name]['Abstract_it']
        if x == 'NaN'or x != str():
            comment = 'Purtroppo, la versione abbreviata francese non è disponibile.'
            x =  df.loc[Name]['Abstract_en']
    if label == 'fr':
        x = df.loc[Name]['Abstract_fr']
        if x == 'NaN'or x != str():
            comment ="'La version courte en français n'est malheureusement pas disponible.'"
            x =  df.loc[Name]['Abstract_en']
    return x, comment

#print (choose_language(data2, "Zoom", 'it'))



#check if result from DBpedia is existing in the service catalog
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
