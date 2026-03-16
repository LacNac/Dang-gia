from flask import Blueprint, render_template, request
import sqlite3

from . import assess_bp
studentdb = 'database/sinhvien.db'
@assess_bp.route('/', methods=['GET','POST'])
def danh_gia():
    # Khai báo con trỏ trỏ tới db
    conn2 = sqlite3.connect(studentdb)
    cursor2 = conn2.cursor()
    # Kiểm tra đã đánh giá trước đó chưa
    if request.method == 'POST':
        ma_sinh_vien="SV001" # CHỜ LOGIN RỒI BỎ VÀO SESSION
        ma_hoc_phan = request.args.get('ma_hoc_phan')
        # Lấy kết quả từ html
        for i in range(1,6):
            diem = request.form.get(f'cau_{i}')
            # Lưu vào sql
            cursor2.execute("""INSERT INTO DanhGia (ma_sinh_vien, ma_hoc_phan, cau_hoi, diem") 
            VALUES (?,?,?,?)""", (ma_sinh_vien, ma_hoc_phan, i, diem, ))

        conn2.commit()

    # Câu truy vấn
    cursor2.execute('SELECT * FROM CauHoi')
    data2 = cursor2.fetchall()
    conn2.close()
    return render_template('danhgia.html', data2=data2)