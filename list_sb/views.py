from flask import render_template
import sqlite3

from . import list_sb_bp
studentdb = 'database/sinhvien.db'
@list_sb_bp.route('/')
def danh_sach():
    # khai báo con trỏ trỏ tới sinhvien.db
    conn = sqlite3.connect(studentdb)
    cursor = conn.cursor()
    # Truy vấn câu lệnh SQL
    #  WHERE ma_hoc_phan IN (SELECT ma_hoc_phan FROM DangKyHP WHERE ma_sinh_vien = 'SV001');
    cursor.execute("SELECT * FROM HocPhan WHERE ma_hoc_phan IN (SELECT ma_hoc_phan FROM DangKyHP WHERE ma_sinh_vien = 'SV001');")
    data = cursor.fetchall()
    # Đóng kết nối db
    conn.close()
    return render_template('liststudent.html', data=data)