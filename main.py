
from flask import Flask, redirect, url_for, render_template, request

import dbpedia
import test

app = Flask(__name__)


#@app.route('/')
#def home():  # put application's code here
#    return 'Hello World!'

@app.route('/', methods=["POST", "GET"])
def home():  # put application's code here
    if request.method == "POST":
        search_string = request.form["nm"]
        print (search_string)
        search_result = dbpedia.search(search_string)

        return redirect(url_for("user", usr=search_result))
        return f"<h1>{search_result}</h1>"
    else:
        return render_template("searchbar.html")




@app.route("/<usr>")
def user(usr):
    return f"<h1>{usr}</h1>"


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080, debug=True)
