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
ApplicationCategory = ['All', 'Access Mgmt. Software', 'Analysation software', 
                       'Asset Mgmt. Software', 'Audition software', 'Automatisation software',
                       'Bug and issue tracking software', 'Buisness Intelligence',
                       'Building Mgmt.', 
                       'Calculation software', 'Call management software', 'Collaborative software',
                       'Computer graphic software 3D', 'Conveyor system engeneering tool', 'Customer Portal', 
                       'Dangerous good Mgmt. software', 
                       'DevOps', 'Digital Signage Software','E-Commerce Software', 
                       'Electronic Signature Software', 'Export control Mgmt.', 
                       'Financial Consolidation Software', 'Fleet management software',
                       'FMEA Functional Safety Software', 'Marketing Automation', 'MindMapping', 'Office Suite',
                       'Operating system', 'Payroll Software', 'PDF-Software',
                       'PLM Suite', 'Project Management Software',
                       'Recruiting Software', 'Remote administration software', 
                       'Sales Software', 'Screenshot software', 'Simulaton Software', 'Staff Planning',
                       'Statistical software', 'Structural engineering software', 'Tax Mgmt. software',
                       'Time Mgmt. Software', 'Travel & Expense Mgmt. Software', 'Warehouse Management System']
# not used but maby needed sometimes: 'Animation software','ApplicationCategory', 'BIM', 'BI', 'BPM',
#  '2D CAD', '3D CAD', 'CAE', 'CAM', 'CAS', 'CAT', 'CIM','CMS','CPM', 'CRM',  'CSM', 'CDP', 'Data Mgmt. software', 'DAM', 'EAM', 'Lean Project Mgmt. Software',                   
#                       'DMS','ELM', 'EOM','ERP','EDA','File Sharing System','GIS', 'Graphics + Design apps', 'WMS','SCADA', 'PMS', 'PDC', SCM', 'SDO', 'LMS','MDC','MES','HCM', 'IDE','RDO','TMS','TMS',
                       
                       
                       
                       
                       
                      
                       
                        
                       
                       
                        

@app.route('/', methods=["POST", "GET"])
def home():  # put application's code here
    try:
        if request.method == "POST":
            data = df
            category = request.form.get('categories')
            appcategory = request.form.get('appcategories')
            search_string = request.form.get('search')


            data = mfilter(data, 'IT Category', category)
            data = data.reset_index(drop=True)
            if data.empty:
                return render_template('searchfail.html', categories=categories, ApplicationCategory=ApplicationCategory)

            data = mfilter(data, 'ApplicationCategory', appcategory)
            data = data.reset_index(drop=True)
            if data.empty:
                return render_template('searchfail.html', categories=categories, ApplicationCategory=ApplicationCategory)

            data = msearch(search_string, data)
            data = data.reset_index(drop=True)
            if data.empty:
                return render_template('searchfail.html', categories=categories, ApplicationCategory=ApplicationCategory)

            search_result = data

            #print(search_result)
            return render_template('results2.0.html', categories=categories, ApplicationCategory=ApplicationCategory,
                                column_names=df.columns.values,
                                row_data=list(search_result.values.tolist()), picture_column="Picture",
                                description_column="Description",name_column="Name", zip=zip)
        else:
            #print(df)
            return render_template("searchbar.html", categories=categories, ApplicationCategory=ApplicationCategory,
                                column_names=df.columns.values,
                                row_data=list(df.values.tolist()), picture_column="Picture",
                                description_column="Description", name_column="Name", zip=zip)
    except:
        return render_template("searchbar.html", categories=categories, ApplicationCategory=ApplicationCategory,
                                column_names=df.columns.values,
                                row_data=list(df.values.tolist()), picture_column="Picture",
                                description_column="Description", name_column="Name", zip=zip)

def msearch(keyword, dataframe):
    search_result = search.search(keyword, dataframe)
    return search_result


def mfilter(dataframe, cat, keyword):
    search_result = search.filter(dataframe, cat, keyword)
    return search_result

@app.route('/ReadMore', methods=["POST", "GET"])
def readMore():
    if request.method == "POST":
        data = df
        softwaer_name = request.form.get('readmore')
        #print(softwaer_name)
        search_result = search.filter(data, 'Name', softwaer_name)
        return render_template('resultsAll.html', categories=categories, ApplicationCategory=ApplicationCategory,
                                column_names=df.columns.values, row_data=list(search_result.values.tolist()), picture_column="Picture",
                                description_column="Description",name_column="Name", Domain_coulum="Business Domain", ApplicationCategory_column="ApplicationCategory",
                                Re_invoicing_column="Re-invoicing", Abstract_en_column="Abstract_en", Abstract_de_column="Abstract_de", Abstract_it_column="Abstract_it", Abstract_fr_column="Abstract_fr", zip=zip)
    else:
        return render_template("searchbar.html", categories=categories, ApplicationCategory=ApplicationCategory,
                                column_names=df.columns.values,
                                row_data=list(df.values.tolist()), picture_column="Picture",
                                description_column="Description", name_column="Name", zip=zip)


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
        return render_template("request_confirmation.html", out=out, categories=categories, ApplicationCategory=ApplicationCategory,
                                column_names=df.columns.values,
                                picture_column="Picture",
                                description_column="Description",name_column="Name", zip=zip)
    else:
        return render_template("searchbar.html", categories=categories)

@app.route('/confirmation', methods=["POST", "GET"])
def confirm_software():  # put application's code here
    if request.method == "POST":
        software = request.form["software_name"]
        out = (f"Do you really want to order: {software}")
        return render_template("order_confirmation.html", out=out, categories=categories, ApplicationCategory=ApplicationCategory,
                                column_names=df.columns.values,
                                picture_column="Picture", software=software,
                                description_column="Description",name_column="Name", zip=zip)
    else:
        return render_template("searchbar.html", categories=categories)





if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080, debug=True)



