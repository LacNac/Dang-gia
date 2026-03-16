from flask import Blueprint, render_template, request
import sqlite3

from . import assess_bp

studentdb = "sinhvien.db"

@assess_bp.route('/danhgia', methods=['GET','POST'])
def danh_gia():

    conn = sqlite3.connect(studentdb)
    cursor = conn.cursor()

    # lấy danh sách câu hỏi
    cursor.execute("SELECT * FROM CauHoi")
    data2 = cursor.fetchall()

    if request.method == "POST":

        ma_sv = "SV001"   # sau này lấy từ session
        ma_hp = request.form.get("ma_hoc_phan")

        tong = 0
        dem = 0

        # đọc điểm từng câu
        for q in data2:

            ma_cau = q[0]   # ví dụ CH01
            diem = request.form.get(f"cau_{ma_cau}")

            if diem is not None:
                diem = float(diem)

                tong += diem
                dem += 1

                # lưu từng câu vào bảng diem
                cursor.execute("""
                    INSERT INTO diem(ma_sinh_vien, ma_hoc_phan, ma_cau_hoi, diem)
                    VALUES(?,?,?,?)
                """, (ma_sv, ma_hp, ma_cau, diem))

        # tính trung bình
        diem_tb = tong / dem if dem > 0 else 0

        # cập nhật bảng tổng
        cursor.execute("""
            UPDATE DiemTrungBinh
            SET diem_trung_binh = ?
            WHERE ma_hoc_phan = ?
        """, (diem_tb, ma_hp))

        conn.commit()

    # khi mở trang đánh giá
    ma_hp = request.args.get("ma_hoc_phan")

    conn.close()

    return render_template(
        "danhgia.html",
        data2=data2,
        ma_hp=ma_hp
    )