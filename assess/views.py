from flask import Blueprint, render_template, request
import sqlite3

from . import assess_bp
studentdb = 'database/sinhvien.db'
@assess_bp.route('/danhgia', methods=['GET','POST'])
def danh_gia():
    # Khai báo con trỏ trỏ tới db
    conn2 = sqlite3.connect(studentdb)
    cursor2 = conn2.cursor()
    # Câu truy vấn
    cursor2.execute('SELECT * FROM CauHoi')
    data2 = cursor2.fetchall()

    # Khi bấm lưu đánh giá
    if request.method == 'POST':
        ma_sv='SV001' # CHỜ LOGIN RỒI BỎ VÀO SESSION
        ma_hp = request.form.get('ma_hoc_phan')
        # Lấy kết quả từ html
        for q in data2:
            ma_cau_hoi = q[0]  # CH01, CH02...
            diem = request.form.get(f'cau_{ma_cau_hoi}')
            # Lưu vào sql
            cursor2.execute("""INSERT INTO DanhGia (ma_sinh_vien, ma_hoc_phan, ma_cau_hoi, diem) 
            VALUES (?,?,?,?)""", (ma_sv, ma_hp, ma_cau_hoi , diem))

        conn2.commit()
    # Khi bấm đánh giá
    ma_hp = request.args.get('ma_hoc_phan')

    conn2.close()
    return render_template('danhgia.html', data2=data2, ma_hp=ma_hp)