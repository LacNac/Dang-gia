from flask import (Flask, render_template,
                   request, redirect,
                   session, url_for, current_app)
import sqlite3
import os
from giangvien1 import gv_bp
from assess import assess_bp
from list_sb import list_sb_bp

app = Flask(__name__)
data = 'sinhvien.db'

# Đăng ký Blueprint
app.register_blueprint(list_sb_bp)
app.register_blueprint(assess_bp)
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
            "SELECT * FROM SinhVien WHERE username = ? AND password = ?",
            (username, password)
        )

        sv = cur.fetchone()

        if sv:
            session['ss_user'] = username
            session['role'] = 'sinhvien'
            session['ma_sinh_vien'] = sv[0]
            return redirect(url_for('list_sb.danh_sach'))

        return render_template("loginsv.html", hu = "Sai tên đăng nhập hoặc mật khẩu")

    return render_template("loginsv.html", hu = None)

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

