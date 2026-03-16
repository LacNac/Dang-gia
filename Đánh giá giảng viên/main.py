from flask import (Flask, render_template,
                   request, redirect,
                   session, url_for, current_app)
import sqlite3
from giangvien1 import gv_bp
import os


app = Flask(__name__)

data = 'sinhvien.db'
app.register_blueprint(gv_bp, url_prefix='/giang_vien')
app.secret_key = 'felix_pham'

@app.route('/', methods=['GET', 'POST'])
@app.route('/loginsv', methods=['GET','POST'])
def loginsv():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect(data)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        cur.execute(
            "SELECT * FROM SinhVien WHERE user = ? AND password = ?",
            (username, password)
        )

        sv = cur.fetchone()

        if sv:
            session['ss_user'] = username
            session['role'] = 'sinhvien'
            return redirect(url_for('sinhvien_home'))

        return "Sai tài khoản hoặc mật khẩu"

    return render_template("loginsv.html")

@app.route('/logingv', methods=['GET','POST'])
def logingv():
    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']
        session['ss_user'] = username
        name = session['ss_user']
        return redirect(url_for('gv.giang_vien'))

    return render_template('logingv.html')

if __name__ == '__main__':
    app.run(debug=True)