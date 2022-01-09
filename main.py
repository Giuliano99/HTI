import os

from flask import Flask, redirect, url_for, render_template, request
import search
import pandas as pd
from flask_mail import Mail, Message

app = Flask(__name__)
mail = Mail(app)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'htigroup04@gmail.com'
app.config['MAIL_PASSWORD'] = 'Bestgroup#'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

#
# path_serviceCatalog = "https://raw.githubusercontent.com/Giuliano99/HTI/test/IT%20Service%20Katalog.csv"
# path_uri = "https://raw.githubusercontent.com/Giuliano99/HTI/test/uri.csv"
#
# serviceCatalog = pd.read_csv(path_serviceCatalog)
# uri = pd.read_csv(path_uri)a

# df = create_dataframe(serviceCatalog, uri)
# df = dbpedia.create_dataframe('IT Service Katalog.csv', 'uri.csv')
# df = df.reset_index(inplace=False)
data2 = pd.read_excel('output.xls', index_col=0)
df = data2


categories = ['All', 'Basic Applications', 'ERP', 'PLM']
ApplicationCategory = [ 'All', 'Access Mgmt. Software', 'Analysation software', 'Animation software', 'ApplicationCategory',
                       'Asset Mgmt. Software', 'Audition software', 'Automatisation software',
                       'Bug and issue tracking software', 'BIM',
                       'Building Mgmt.', 'BI', 'BPM',
                       'Calculation software', 'Call management software', 'Collaborative software',
                       '2D CAD', '3D CAD',
                       'CAE', 'CAM',
                       'CAS', 'Computer graphic software 3D',
                       'CAT', 'CIM',
                       'CMS', 'Conveyor system engeneering tool',
                       'CPM', 'Customer Portal', 'CRM',
                       'CSM', 'CDP',
                       'Dangerous good Mgmt. software', 'Data Mgmt. software',
                       'DevOps', 'DAM', 'Digital Signage Software',
                       'DMS', 'E-Commerce Software', 'EDA',
                       'Electronic Signature Software', 'EAM',
                       'ELM', 'EOM',
                       'ERP', 'Export control Mgmt.', 'File Sharing System',
                       'Financial Consolidation Software', 'Fleet management software',
                       'FMEA Functional Safety Software',
                       'GIS', 'Graphics + Design apps',
                       'HCM', 'IDE',
                       'Lean Project Mgmt. Software', 'LMS',
                       'MDC',
                       'MES', 'Marketing Automation', 'MindMapping', 'Office Suite',
                       'Operating system', 'PMS', 'Payroll Software', 'PDF-Software',
                       'PLM Suite', 'PDC', 'Project Management Software',
                       'Recruiting Software', 'Remote administration software', 'RDO',
                       'Sales Software', 'Screenshot software', 'Simulaton Software', 'Staff Planning',
                       'Statistical software', 'Structural engineering software',
                       'SCADA',
                       'SCM', 'SDO', 'Tax Mgmt. software',
                       'Time Mgmt. Software', 'TMS', 'Travel & Expense Mgmt. Software',
                       'TMS', 'Warehouse Management System', 'WMS']


@app.route('/', methods=["POST", "GET"])
def home():  # put application's code here

    if request.method == "POST":
        category = request.form.get('categories')
        appcategory = request.form.get('appcategories')
        search_string = request.form.get('search')
        print(search_string)
        search_result = search.search(search_string, df)
        search_result = search_result.drop(columns=['index', "Name_search", "Description_search", "Abstract_en_search", "Abstract_de_search", "ApplicationCategory_search", "IT Category_search", "sum"])
        print(search_result)
        return render_template('results 2.0.html', categories=categories,ApplicationCategory=ApplicationCategory,column_names=df.columns.values,
        row_data=list(search_result.values.tolist()), picture_column="Picture",description_column="Description",name_column="Name", zip=zip)
    else:
        print(df)
        return render_template("searchbar.html",categories=categories,ApplicationCategory=ApplicationCategory,column_names=df.columns.values,
        row_data=list(df.values.tolist()), picture_column="Picture",description_column="Description",name_column="Name", zip=zip)


def msearch(keyword, dataframe):
    search_result = search.search(keyword, dataframe)
    return search_result


def mfilter(dataframe, cat ,keyword):
    search_result = search.filter(dataframe, cat, keyword)
    return search_result


@app.route('/redirect', methods=["POST", "GET"])
def umleiten():  # put application's code here
    if request.method == "POST":
        return redirect(url_for('home'))
    else:
        return redirect(url_for('home'))


@app.route('/mail', methods=["POST", "GET"])
def select_software():  # put application's code here
    if request.method == "POST":
        software = request.form["software_name"]
        out = (f"You oredered {software}, congratulation")
        msg = Message('Ticket request', sender='htigroup04@gmail.com', recipients=['htigroup04@gmail.com'])
        msg.body = out
        mail.send(msg)
        return render_template("request_confirmation.html", out=out)
    else:
        return render_template("searchbar.html", categories=categories)


@app.route('/cat', methods=["POST", "GET"])
def cate():
    data = df
    if request.method == "POST":
        category = request.form.get('categories')
        appcategory = request.form.get('appcategories')
        search_string = request.form.get('search')

        print(category)
        print(appcategory)
        print(search_string)
        #print(data)
        data = mfilter(data,'IT Category', category)
        data = data.reset_index()
        print(data)
        data = mfilter(data,'ApplicationCategory', appcategory)
        data = data.reset_index()
        print(data)
        data = msearch(search_string, data)
        print(data)

        return render_template("searchbar.html", categories=categories, ApplicationCategory=ApplicationCategory)
    else:
        return render_template("searchbar.html", categories=categories, ApplicationCategory=ApplicationCategory)
    print("Hi")
    return



@app.route('/dropdown', methods=["POST", "GET"])
def dropdown():
    Colum = ['IT Category', 'ApplicationCategory']
    # if select_colum == "IT Category":
    #     select = request.form.get('IT Category')
    #     categories = IT_Category
    # else:
    #     select = request.form.get(' ApplicationCategory')
    #     categories = ApplicationCategory
    # result = search.filter(select_colum, select, df)
    if request.method == "POST":
        Colum = 'IT Category'
        category = request.form.get('categories')
        appcategory = request.form.get('appcategories')
        search_string = request.form.get('search')
        search_result = search.search(search_string, df)
        print(search_result)
        return render_template('test.html', categories=categories, Colum=Colum,
                               ApplicationCategory=ApplicationCategory)
    else:
        return render_template('test.html', categories=categories, Colum=Colum,
                               ApplicationCategory=ApplicationCategory)


@app.route('/testdropdown', methods=["POST", "GET"])
def testdropdown():
    Colum = ['IT Category', 'ApplicationCategory']
    # if select_colum == "IT Category":
    #     select = request.form.get('IT Category')
    #     categories = IT_Category
    # else:
    #     select = request.form.get(' ApplicationCategory')
    #     categories = ApplicationCategory
    # result = search.filter(select_colum, select, df)
    if request.method == "POST":
        Colum = 'IT Category'
        select = request.form["categories"]
        result = search.filter(df, Colum, select)
        print(result)
        return render_template('test.html', categories=categories, Colum=Colum,
                               ApplicationCategory=ApplicationCategory)
    else:
        return render_template('test.html', categories=categories, Colum=Colum,
                               ApplicationCategory=ApplicationCategory)


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080, debug=True)
