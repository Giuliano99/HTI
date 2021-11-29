
from flask import Flask, redirect, url_for, render_template, request

import dbpedia
import test

app = Flask(__name__)

#
# path_serviceCatalog = "https://raw.githubusercontent.com/Giuliano99/HTI/test/IT%20Service%20Katalog.csv"
# path_uri = "https://raw.githubusercontent.com/Giuliano99/HTI/test/uri.csv"
#
# serviceCatalog = pd.read_csv(path_serviceCatalog)
# uri = pd.read_csv(path_uri)

#df = create_dataframe(serviceCatalog, uri)
df = dbpedia.create_dataframe('IT Service Katalog.csv', 'uri.csv')
df = df.reset_index(inplace=False)


#@app.route('/')
#def home():  # put application's code here
#    return 'Hello World!'

@app.route('/', methods=["POST", "GET"])
def home():  # put application's code here
    if request.method == "POST":
        search_string = request.form["nm"]
        #print (search_string)
        search_result = dbpedia.search([search_string], df)
        search_result = search_result


        return redirect(url_for("user", usr = search_result.loc[0:5]['Name']))
        return f"<h1>{search_result}</h1>"
    else:
        return render_template("searchbar.html")




@app.route("/<usr>")
def user(usr):
    return f"<h1>{usr}</h1>"


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080, debug=True)
