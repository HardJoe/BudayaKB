from budayaKB_model import BudayaItem, BudayaCollection
from flask import Flask, request, render_template, redirect, flash
from wtforms import Form, validators, TextField
import jinja2

app = Flask(__name__)
app.secret_key ="tp4"

#inisialisasi objek budayaData
databasefilename = ""
budayaData = BudayaCollection()

#membuat IDE untuk Flask
jinja_environment = jinja2.Environment(autoescape=True, loader=jinja2.FileSystemLoader('templates'))

#merender tampilan default(index.html)
@app.route('/')
def index():
	return render_template("index.html")

# Bagian ini adalah implementasi fitur Impor Budaya, yaitu:
# - merender tampilan saat menu Impor Budaya diklik
# - melakukan pemrosesan terhadap isian form setelah tombol "Import Data" diklik
# - menampilkan notifikasi bahwa data telah berhasil diimport
@app.route('/imporBudaya', methods=['GET', 'POST'])
def importData():
	if request.method == "GET":
		return render_template("imporBudaya.html")

	elif request.method == "POST":
		f = request.files['file']
		databasefilename=f.filename
		result_impor=budayaData.importFromCSV(f.filename)
		budayaData.exportToCSV(databasefilename) #setiap perubahan data langsung disimpan ke file
		return render_template("imporBudaya.html", result=result_impor, fname=f.filename)


# run main app
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=8080, debug=True)
