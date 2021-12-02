
from flask import Flask, redirect, url_for, render_template, request

import dbpedia
import test
import pandas as pd

app = Flask(__name__)

#
# path_serviceCatalog = "https://raw.githubusercontent.com/Giuliano99/HTI/test/IT%20Service%20Katalog.csv"
# path_uri = "https://raw.githubusercontent.com/Giuliano99/HTI/test/uri.csv"
#
# serviceCatalog = pd.read_csv(path_serviceCatalog)
# uri = pd.read_csv(path_uri)

#df = create_dataframe(serviceCatalog, uri)
#df = dbpedia.create_dataframe('IT Service Katalog.csv', 'uri.csv')
#df = df.reset_index(inplace=False)
data2 = pd.read_excel('output.xlsx', index_col=0) 
df = data2
#@app.route('/')
#def home():  # put application's code here
#    return 'Hello World!'

@app.route('/', methods=["POST", "GET"])
def home():  # put application's code here
    if request.method == "POST":
        search_string = request.form["nm"]
        #print (search_string)
        search_result = dbpedia.search([search_string], df)

        return render_template('results 2.0.html', column_names=search_result.columns.values,
                               row_data=list(search_result.values.tolist()), link_column="first_uri", zip=zip)

        return render_template('searchresults.html', tables=[search_result.to_html(classes='data')], titles=search_result.columns.values)

        #return redirect(url_for("user", usr = search_result.loc[0:5]['Name']))
        #return f"<h1>{search_result}</h1>"
    else:
        return render_template("index.html")




@app.route("/<usr>")
def user(usr):
    return f"<h1>{usr}</h1>"


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080, debug=True)
