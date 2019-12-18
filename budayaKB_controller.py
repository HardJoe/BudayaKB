from budayaKB_model import BudayaItem, BudayaCollection
from flask import Flask, request, render_template, redirect, flash
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
		try:
			budayaData.koleksi = {}
			f = request.files['file']
			global databasefilename
			databasefilename = f.filename
			result_impor = budayaData.importFromCSV(f.filename)
			budayaData.exportToCSV(databasefilename) #setiap perubahan data langsung disimpan ke file
			return render_template("imporBudaya.html", result=result_impor, fname=f.filename)
		except FileNotFoundError:  #jika file dalam format yang salah
			f_error = 1
			return render_template("imporBudaya.html", f_error=f_error)
		except PermissionError:    #jika file sedang dibuka di program lain
			p_error = 1
			return render_template("imporBudaya.html", p_error=p_error)

#menambah budaya baru ke dalam database
@app.route('/tambahBudaya', methods=['GET', 'POST'])
def addData():
    if request.method == "GET":
        return render_template("tambahBudaya.html")
    elif request.method == 'POST':
        result_tambah = budayaData.tambah(request.form['name'], request.form['tipe'], request.form['prov'], request.form['url'])
        try:
            budayaData.exportToCSV(databasefilename)
        except FileNotFoundError:
            f_error = 1
            return render_template("tambahBudaya.html", f_error=f_error)
        return render_template("tambahBudaya.html", result=result_tambah, name=request.form['name'], filename=databasefilename)

#mengubah data budaya yang sudah ada dalam database
@app.route('/ubahBudaya', methods=['GET', 'POST'])
def updateData():
    if request.method == "GET":
        return render_template("ubahBudaya.html")
    elif request.method == 'POST':
        result_ubah = budayaData.ubah(request.form['name'], request.form['tipe'], request.form['prov'], request.form['url'])
        try:
            budayaData.exportToCSV(databasefilename)
        except FileNotFoundError:
            f_error = 1
            return render_template("ubahBudaya.html", f_error=f_error)
        return render_template("ubahBudaya.html", result=result_ubah, name=request.form['name'])

#menghapus budaya yang ada dalam database
@app.route('/hapusBudaya', methods=['GET', 'POST'])
def removeData():
    if request.method == "GET":
        return render_template("hapusBudaya.html")
    elif request.method == 'POST':
        result_hapus = budayaData.hapus(request.form['name'])
        try:
            budayaData.exportToCSV(databasefilename)
        except FileNotFoundError:
            f_error = 1
            return render_template("hapusBudaya.html", f_error=f_error)
        return render_template("hapusBudaya.html", result=result_hapus, name=request.form['name'])

#mencari budaya, tipe, atau asal provinsi dalam database
@app.route('/cariBudaya', methods=['GET', 'POST'])
def findData():
    if request.method == "GET":
        return render_template("cariBudaya.html")
    if request.method == "POST":
        if request.form['entry'] == '*':  #untuk mencari seluruh budaya
            all_list = budayaData.cariAll()
            qty_all = len(all_list)
            return render_template("cariBudaya.html", all_list=all_list, qty_all=qty_all)
        elif request.form['pilih'] == 'name':
            name_list = budayaData.cariByNama(request.form['entry'])
            qty_name = len(name_list)
            return render_template("cariBudaya.html", name_list=name_list, name=request.form['entry'], qty_name=qty_name)
        elif request.form['pilih'] == 'tipe':
            tipe_list = budayaData.cariByTipe(request.form['entry'])
            qty_tipe = len(tipe_list)
            return render_template("cariBudaya.html", tipe_list=tipe_list, tipe=request.form['entry'], qty_tipe=qty_tipe)
        else:
            prov_list = budayaData.cariByProv(request.form['entry'])
            qty_prov = len(prov_list)
            return render_template("cariBudaya.html", prov_list=prov_list, prov=request.form['entry'], qty_prov=qty_prov)

#memunculkan statistik jumlah budaya, tipe, atau asal provinsi di database
@app.route('/statsBudaya', methods=['GET', 'POST'])
def viewStats():
    if request.method == "GET":
        return render_template("statsBudaya.html")
    if request.method == "POST":
        if request.form['pilih'] == 'all':
            result_all = budayaData.stat()
            return render_template("statsBudaya.html", result_all=result_all)
        elif request.form['pilih'] == 'tipe':
            tipe_dict = budayaData.statByTipe()
            return render_template("statsBudaya.html", tipe_dict=tipe_dict)
        else:
            prov_dict = budayaData.statByProv()
            return render_template("statsBudaya.html", prov_dict=prov_dict)

#menjalankan main app
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=5000, debug=True)
