from flask import Flask, redirect, url_for, render_template, request
import search
import pandas as pd
from flask_mail import Mail, Message


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
data2 = pd.read_excel('output.xls', index_col=0)
df = data2
#@app.route('/')
#def home():  # put application's code here
#    return 'Hello World!'



@app.route('/', methods=["POST", "GET"])
def home():  # put application's code here
    categories = ['Basic Applications', 'ERP', 'Network', 'Personal Computing', 'PLM', 'Plotting',
                  'Security']
    if request.method == "POST":
        search_string = request.form["nm"]
        search_result = search.search([search_string], df)

        return render_template('results 2.0.html', column_names=search_result.columns.values,
                               row_data=list(search_result.values.tolist()), link_column="first_uri", zip=zip,
                               categories=categories)
    else:
        return render_template("searchbar.html",  categories=categories)


@app.route('/dropdown', methods=["POST", "GET"])
def dropdown():
    Colum = ['IT Category', 'ApplicationCategory']
    IT_Category = ['Basic Applications', 'ERP', 'Network', 'Personal Computing', 'PLM', 'Plotting', 'Security']
    ApplicationCategory = ['Access Mgmt. Software', 'Analysation software', 'Animation software', 'ApplicationCategory', 'Asset Mgmt. Software', 'Audition software', 'Automatisation software', 'Bug and issue tracking software', 'Building information modeling (BIM)',
        'Building Mgmt.', 'Buisness Intelligence (BI)', 'Business process Mgmt. (BPM)', 'Calculation software', 'Call management software', 'Collaborative software', 'Computer Aided design 2D (2D CAD)', 'Computer Aided design 3D (3D CAD)',
        'Computer aided engineering (CAE)', 'Computer Aided Manufacturing (CAM)', 'Computer algebra system (CAS)', 'Computer graphic software 3D', 'Computer-assisted translation (CAT)', 'Computer-integrated manufacturing (CIM)', 'Content Mgmt. Software (CMS)', 'Conveyor system engeneering tool',
        'Corporate Performance Mgmt (CPM)', 'Customer Portal', 'Customer Relationship Mgmt (CRM)', 'Customer Service Management (CSM)', 'Customs Declaration Programm (CDP)', 'Dangerous good Mgmt. software', 'Data Mgmt. software',
        'DevOps', 'Digital Asset Mgmt. (DAM)', 'Digital Signage Software', 'Document management system (DMS)', 'E-Commerce Software', 'Electronic design automation (EDA)', 'Electronic Signature Software', 'Enterprise Asset Management (EAM)',
        'Enterprise Legal Management (ELM)', 'Enterprise Output Management (EOM)',  'Enterprise Ressource Planning (ERP)', 'Export control Mgmt.', 'File Sharing System', 'Financial Consolidation Software', 'Fleet management software', 'FMEA Functional Safety Software',
        'Geographic information system (GIS)', 'Graphics + Design apps', 'Human capital management (HCM)', 'Integrated development environment (IDE)', 'Lean Project Mgmt. Software', 'Learning Management System (LMS)', 'Machine Data Capturing (MDC)',
        'Manufacturing execution systems (MES)', 'Marketing Automation', 'MindMapping', 'Office Suite', 'Operating system', 'Patent Mgmt. Software (PMS)', 'Payroll Software', 'PDF-Software', 'PLM Suite', 'Production Data Capturing (PDC)', 'Project Management Software',
        'Recruiting Software', 'Remote administration software', 'Ropeway Design Office (RDO)', 'Sales Software', 'Screenshot software', 'Simulaton Software', 'Staff Planning', 'Statistical software', 'Structural engineering software', 'Supervisory Control and Data Acquisition (SCADA)',
        'Supply Chain Mgmt. (SCM)', 'Survey data collection (SDO)', 'Tax Mgmt. software', 'Time Mgmt. Software', 'Transport Mgmt. System (TMS)', 'Travel & Expense Mgmt. Software', 'Treasury Mgmt. System (TMS)', 'Warehouse Management System', 'Workforce Mgmt. Software (WMS)']
    select_colum = request.form.get('Colum')
    if select_colum == "IT Category":
        select = request.form.get('IT Category')
        categories = IT_Category
    else:
        select = request.form.get(' ApplicationCategory')
        categories = ApplicationCategory
    result = search.filter(select_colum, select, df)
    print(result)
    return render_template('test.html', categories=categories, Colum=Colum)


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080, debug=True)
