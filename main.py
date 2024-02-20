from flask import Flask, render_template, request, redirect, url_for
import models.svr as svr
import models.plot as plot
from models.data import read_data
import models.data as data

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def dataset():
    if request.method == 'GET':
    
        if data.check_avalable_data() :
            status_data = True
            preview = data.read_data().iloc[:5]
            kolom = preview.columns.to_list()
            row = preview.values.tolist()
            del preview
            
        else:
            status_data = False
    
        return render_template(
            './pages/dataset.html',
            status_data = status_data,
            kolom = kolom,
            row = row
        )
    
    if request.method == 'POST':
        
        dataset = request.files['dataset']
        dataset.save('./static/data/dataset.csv')
        
        return redirect(url_for('dataset'))
    
@app.route("/analisis-data", methods=['GET','POST'])
def analisis_data():
    if request.method == 'GET':
        
        return render_template(
            './pages/analisis_data.html'
        )
        
    if request.method == 'POST':
        import models.analisis_data as asdat
        
        asdat.analisis_data()
        
        return render_template(
            './pages/analisis_data.html'
        )
    
# @app.route("/evaluasi", methods=['GET', 'POST'])
# def evaluasi():
#     if request.method == 'GET':
#         data = svm.svm()
#         mse = data['mse']
    
#         plot.show_visual()
        
#         return render_template(
#             './pages/evaluasi.html',
#             mse = mse,
#             data = data,
#         )
        
@app.route("/prediksi", methods=['GET', 'POST'])
def prediksi():
    if request.method == 'GET':
       
        return render_template(
            './pages/prediksi.html',
        )
        
    if request.method == 'POST':
        
        day = int(request.form['day'])
        data = read_data()

        prediksi = svr.predict_stock_and_signal(day, data)
        
        return render_template(
            './pages/hasil-prediksi.html',
            data = prediksi,
        )
    
        
@app.route("/data-uji", methods=['GET', 'POST'])
def data_uji():
    if request.method == 'GET':
        
        return render_template(
            './pages/data-uji.html'
        )
        
    if request.method == 'POST':
        
        return redirect(url_for('data_uji'))