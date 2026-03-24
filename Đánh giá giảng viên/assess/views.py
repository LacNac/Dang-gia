from flask import Blueprint, render_template, request, redirect
import sqlite3

from . import assess_bp

studentdb = 'sinhvien.db'


@assess_bp.route('/danhgia', methods=['GET', 'POST'])
def danh_gia():
    # Khai báo con trỏ trỏ tới db
    conn2 = sqlite3.connect(studentdb)
    cursor2 = conn2.cursor()
    # Câu truy vấn
    cursor2.execute('SELECT * FROM CauHoi')
    data2 = cursor2.fetchall()

    # Khi bấm lưu đánh giá
    if request.method == 'POST':
        diem1 = float(request.form.get("cau_CH01"))
        diem2 = float(request.form.get("cau_CH02"))
        diem3 = float(request.form.get("cau_CH03"))
        diem4 = float(request.form.get("cau_CH04"))
        diem5 = float(request.form.get("cau_CH05"))

        diem_tb = (diem1 + diem2 + diem3 + diem4 + diem5) / 5

        ma_hp = request.form.get("ma_hoc_phan")

        cursor2.execute("""
            UPDATE DiemTrungBinh
            SET diem_cau_1 = (? + diem_cau_1)/2,
                diem_cau_2 = (? + diem_cau_2)/2,
                diem_cau_3 = (? + diem_cau_3)/2,
                diem_cau_4 = (? + diem_cau_4)/2,
                diem_cau_5 = (? + diem_cau_5)/2,
                diem_trung_binh = (? + diem_trung_binh)/2
            WHERE ma_hoc_phan = ?
        """, (diem1, diem2, diem3, diem4, diem5, diem_tb, ma_hp))

        conn2.commit()
        return redirect("/list_sb")

    # Khi bấm đánh giá
    ma_hp = request.args.get('ma_hoc_phan')

    conn2.close()
    return render_template('danhgia.html', data2=data2, ma_hp=ma_hp)
