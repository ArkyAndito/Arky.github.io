from flask import Flask, render_template
from flask import request, redirect, url_for
from mysql import connector

app = Flask(__name__)

db  = connector.connect(
    host        = 'localhost',
    user        = 'root',
    passwd      = '',
    database    = 'db_kuliah'
)

if db.is_connected():
    print('Berhasil Terhubung ke Databese')

@app.route('/')
def halaman_awal():
    cursor = db.cursor()
    cursor.execute("select * from tbl_mhs")
    result = cursor.fetchall()
    cursor.close()
    return render_template('index.html', hasil=result)

@app.route('/tambah/')
def tambah_data():
    return render_template('tambah.html')

@app.route('/proses_tambah/', methods=['POST'])
def proses_tambah():
    nim  = request.form['nim']
    nama = request.form['nama']
    asal = request.form['asal']
    cursor = db.cursor()
    cursor.execute('INSERT INTO tbl_mhs (nim, nama, asal) VALUES (%s, %s, %s)', (nim, nama, asal))
    db.commit()
    return redirect(url_for('halaman_awal'))


@app.route('/ubah/<nim>', methods=['GET'])
def ubah_data(nim):
    cursor = db.cursor()
    cursor.execute('SELECT * from tbl_mhs where nim=%s', (nim,))
    res = cursor.fetchall()
    cursor.close()
    return render_template('ubah.html', hasil=res)

@app.route('/proses_ubah/', methods=['POST'])
def proses_ubah():
    no_mhs = request.form['nim_ori']
    nim = request.form['nim']
    nama = request.form['nama']
    asal = request.form['asal']
    cursor = db.cursor
    sql = "UPDATE tbl_mhs SET nim=%s, nama=%s, asal=%s, WHERE nim=%s" 
    value = (nim, nama, asal, no_mhs)
    cursor.execute(sql, value)
    db.commit()
    return redirect(url_for('halaman_awal'))  

@app.route('/hapus/<nim>', methods=['GET'])
def hapus_data(nim):
    cursor = db.cursor()
    cursor.execute('DELETE tbl_mhs where nim=%', (nim,))
    db.commit()
    return redirect(url_for(halaman_awal))

 
if  __name__ == '__main__':
    app.run(debug=True)

 


