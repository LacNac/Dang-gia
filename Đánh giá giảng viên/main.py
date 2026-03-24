from flask import (Flask, render_template,
                   request, redirect,
                   session, url_for, current_app, jsonify)
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
@app.route('/loginsv', methods=['GET', 'POST'])
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

        return render_template("loginsv.html", hu="Sai tên đăng nhập hoặc mật khẩu")

    return render_template("loginsv.html")


@app.route('/logingv', methods=['GET', 'POST'])
def logingv():
    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']
        if username != "gv" and password != "1":
            return render_template('logingv.html', hu="Sai tên đăng nhập hoặc mật khẩu")
        return redirect(url_for('gv.giang_vien'))

    return render_template('logingv.html')


# API
# {
#   "username": "svnhu",
#   "password": "123"
# }
@app.route('/api/loginsv', methods=['POST'])
def api_loginsv():
    data_json = request.get_json()

    username = data_json.get('username')
    password = data_json.get('password')

    conn = sqlite3.connect(data)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM SinhVien WHERE username = ? AND password = ?",
        (username, password)
    )

    sv = cur.fetchone()
    conn.close()

    if sv:
        return jsonify({
            "message": "Login success",
            "ma_sinh_vien": sv[0],
            "username": username
        })

    return jsonify({"error": "Sai tài khoản"}), 401


# lấy danh sách sinh viên
# http://127.0.0.1:5000/api/sinhvien
@app.route('/api/sinhvien', methods=['GET'])
def api_get_sinhvien():
    conn = sqlite3.connect(data)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("SELECT * FROM SinhVien")
    rows = cur.fetchall()
    conn.close()

    return jsonify([dict(row) for row in rows])


# thêm sinh viên
@app.route('/api/sinhvien', methods=['POST'])
def api_add_sv():
    data_json = request.get_json()

    username = data_json.get('username')
    password = data_json.get('password')

    conn = sqlite3.connect(data)
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO SinhVien (username, password) VALUES (?, ?)",
        (username, password)
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "Thêm thành công"})


# update sinh viên
@app.route('/api/sinhvien/<int:id>', methods=['PUT'])
def api_update_sv(id):
    data_json = request.get_json()

    username = data_json.get('username')
    password = data_json.get('password')

    conn = sqlite3.connect(data)
    cur = conn.cursor()

    cur.execute(
        "UPDATE SinhVien SET username=?, password=? WHERE ma_sinh_vien=?",
        (username, password, id)
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "Cập nhật thành công"})

# lấy danh sách học phần của 1 sinh viên
# test api: http://127.0.0.1:5000/api/sinhvien/hocphan?ma_sinh_vien=SV001
@app.route('/api/sinhvien/hocphan', methods=['GET'])
def api_liststudent():
    conn = sqlite3.connect(data)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    ma_sv = request.args.get('ma_sinh_vien')  # lấy từ URL

    cursor.execute("""
        SELECT * FROM HocPhan 
        WHERE ma_hoc_phan IN (
            SELECT ma_hoc_phan 
            FROM DangKyHP 
            WHERE ma_sinh_vien = ?
        )
    """, (ma_sv,))

    rows = cursor.fetchall()
    conn.close()

    return jsonify([dict(row) for row in rows])

# xóa sinh viên
@app.route('/api/sinhvien/<int:id>', methods=['DELETE'])
def api_delete_sv(id):
    conn = sqlite3.connect(data)
    cur = conn.cursor()

    cur.execute("DELETE FROM SinhVien WHERE ma_sinh_vien=?", (id,))
    conn.commit()
    conn.close()

    return jsonify({"message": "Xóa thành công"})


if __name__ == '__main__':
    app.run(debug=True)
