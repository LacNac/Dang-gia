from flask import render_template, session
import sqlite3

from . import list_sb_bp
studentdb = 'sinhvien.db'
@list_sb_bp.route('/')
def danh_sach():
    # khai báo con trỏ trỏ tới sinhvien.db
    conn = sqlite3.connect(studentdb)
    cursor = conn.cursor()
    # Lấy mã sinh viên từ user
    ma_sv = session.get('ma_sinh_vien')
    # Truy vấn câu lệnh SQL
    cursor.execute("""SELECT * FROM HocPhan WHERE ma_hoc_phan IN (SELECT ma_hoc_phan FROM DangKyHP WHERE ma_sinh_vien = ?)""", (ma_sv,))
    data = cursor.fetchall()
    # Đóng kết nối db
    conn.close()
    return render_template('liststudent.html', data=data)