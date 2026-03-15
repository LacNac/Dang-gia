from flask import Blueprint, render_template
import sqlite3

from . import assess_bp
studentdb = 'database/sinhvien.db'
@assess_bp.route('/')
def danh_gia():
    # Khai báo con trỏ trỏ tới db
    conn2 = sqlite3.connect(studentdb)
    cursor2 = conn2.cursor()
    # Câu truy vấn
    cursor2.execute('SELECT * FROM CauHoi')
    data2 = cursor2.fetchall()

    conn2.close()
    return render_template('danhgia.html', data2=data2)