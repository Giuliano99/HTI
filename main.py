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
# uri = pd.read_csv(path_uri)

# df = create_dataframe(serviceCatalog, uri)
# df = dbpedia.create_dataframe('IT Service Katalog.csv', 'uri.csv')
# df = df.reset_index(inplace=False)
data2 = pd.read_excel('output.xls', index_col=0)
df = data2
# @app.route('/')
# def home():  # put application's code here
#    return 'Hello World!'

categories = ['All', 'Basic Applications', 'ERP', 'PLM']
ApplicationCategory = ['Buisness Intelligence (BI);#20','Access Mgmt. Software', 'Analysation software', 'Animation software', 'ApplicationCategory',
                       'Asset Mgmt. Software', 'Audition software', 'Automatisation software',
                       'Bug and issue tracking software', 'Building information modeling (BIM)',
                       'Building Mgmt.', 'Buisness Intelligence (BI)', 'Business process Mgmt. (BPM)',
                       'Calculation software', 'Call management software', 'Collaborative software',
                       'Computer Aided design 2D (2D CAD)', 'Computer Aided design 3D (3D CAD)',
                       'Computer aided engineering (CAE)', 'Computer Aided Manufacturing (CAM)',
                       'Computer algebra system (CAS)', 'Computer graphic software 3D',
                       'Computer-assisted translation (CAT)', 'Computer-integrated manufacturing (CIM)',
                       'Content Mgmt. Software (CMS)', 'Conveyor system engeneering tool',
                       'Corporate Performance Mgmt (CPM)', 'Customer Portal', 'Customer Relationship Mgmt (CRM)',
                       'Customer Service Management (CSM)', 'Customs Declaration Programm (CDP)',
                       'Dangerous good Mgmt. software', 'Data Mgmt. software',
                       'DevOps', 'Digital Asset Mgmt. (DAM)', 'Digital Signage Software',
                       'Document management system (DMS)', 'E-Commerce Software', 'Electronic design automation (EDA)',
                       'Electronic Signature Software', 'Enterprise Asset Management (EAM)',
                       'Enterprise Legal Management (ELM)', 'Enterprise Output Management (EOM)',
                       'Enterprise Ressource Planning (ERP)', 'Export control Mgmt.', 'File Sharing System',
                       'Financial Consolidation Software', 'Fleet management software',
                       'FMEA Functional Safety Software',
                       'Geographic information system (GIS)', 'Graphics + Design apps',
                       'Human capital management (HCM)', 'Integrated development environment (IDE)',
                       'Lean Project Mgmt. Software', 'Learning Management System (LMS)',
                       'Machine Data Capturing (MDC)',
                       'Manufacturing execution systems (MES)', 'Marketing Automation', 'MindMapping', 'Office Suite',
                       'Operating system', 'Patent Mgmt. Software (PMS)', 'Payroll Software', 'PDF-Software',
                       'PLM Suite', 'Production Data Capturing (PDC)', 'Project Management Software',
                       'Recruiting Software', 'Remote administration software', 'Ropeway Design Office (RDO)',
                       'Sales Software', 'Screenshot software', 'Simulaton Software', 'Staff Planning',
                       'Statistical software', 'Structural engineering software',
                       'Supervisory Control and Data Acquisition (SCADA)',
                       'Supply Chain Mgmt. (SCM)', 'Survey data collection (SDO)', 'Tax Mgmt. software',
                       'Time Mgmt. Software', 'Transport Mgmt. System (TMS)', 'Travel & Expense Mgmt. Software',
                       'Treasury Mgmt. System (TMS)', 'Warehouse Management System', 'Workforce Mgmt. Software (WMS)']


@app.route('/', methods=["POST", "GET"])
def home():  # put application's code here

    if request.method == "POST":
        search_string = request.form["nm"]
        search_result = search.search(search_string, df)
        return msearch(df, search_result)
    else:
        return render_template("searchbar.html", categories=categories)


def msearch(dataframe, keyword):
    search_result = search.search(dataframe, keyword)
    return render_template('results 2.0.html', column_names=search_result.columns.values,
                           row_data=list(search_result.values.tolist()), link_column="Name", zip=zip,
                           categories=categories)
def mfilter(dataframe, cat ,keyword):

    search_result = search.filter(dataframe,cat, keyword)
    return render_template('results 2.0.html', column_names=search_result.columns.values,
                           row_data=list(search_result.values.tolist()), link_column="Name", zip=zip,
                           categories=categories)


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
    if request.method == "POST":
        category = request.form["categories"]
        #print(category)
        return mfilter(df,'IT Category' ,category)
    else:
        return render_template("searchbar.html", categories=categories)
    print("Hi")
    return


@app.route('/appcat', methods=["POST", "GET"])
def appcate():
    if request.method == "POST":
        category = request.form["appcategories"]
        #print(category)
        return mfilter(df,'ApplicationCategory' ,category)
    else:
        return render_template("searchbar.html", categories=categories)
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
        select = request.form["categories"]
        request.form["appcategories"]
        #result = search.filter(df, Colum, select)
        #print(result)
        return
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
