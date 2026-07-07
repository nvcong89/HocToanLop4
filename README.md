# 🎓 Học Toán Lớp 4

<div align="center">

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge)

**Ứng dụng luyện tập Toán Lớp 4 với bài tập tự động, tương tác và chấm điểm trực tiếp.**

*Được xây dựng bởi **Nguyễn Văn Công** với ❤️ dành cho các em học sinh*

</div>

---

## 📸 Giao Diện

🏠 Trang Chủ     → Tổng quan các chủ đề + thông tin tác giả
➕ Cộng & Trừ    → Lý thuyết + luyện tập + kiểm tra nhanh
✖️ Nhân & Chia   → Lý thuyết + luyện tập + bảng nhân tương tác
🍕 Phân Số       → So sánh + cộng/trừ + rút gọn + minh họa
📐 Hình Học      → Chu vi + diện tích + công cụ tính nhanh
📏 Đo Lường      → Đổi đơn vị độ dài, khối lượng, thời gian
📝 Toán Đố       → 6 dạng bài + gợi ý từng bước + thi thử


---

## ✨ Tính Năng Nổi Bật

- 🎲 **Tạo bài tập ngẫu nhiên** — Không bao giờ lặp lại đề cũ
- 📊 **Chấm điểm tự động** — Hiển thị đúng/sai ngay lập tức
- 💡 **Gợi ý từng bước** — Hướng dẫn chi tiết khi làm sai
- 🎯 **3 mức độ khó** — Dễ / Trung bình / Khó
- 🏆 **Bảng điểm sidebar** — Theo dõi tiến độ theo thời gian thực
- 📱 **Giao diện thân thiện** — Màu sắc đẹp, dễ sử dụng cho học sinh

---

## 📚 Nội Dung Chương Trình

### ➕ Cộng & Trừ
- Phép cộng, trừ các số có đến 6 chữ số
- Tính chất giao hoán, kết hợp
- Dạng bài điền số còn thiếu

### ✖️ Nhân & Chia
- Nhân số nhiều chữ số với 1–2 chữ số
- Chia hết và chia có dư
- Bảng nhân tương tác (2–9)

### 🍕 Phân Số
- Khái niệm và minh họa trực quan
- So sánh phân số khác mẫu
- Cộng, trừ phân số cùng mẫu
- Rút gọn phân số

### 📐 Hình Học
- Chu vi và diện tích hình chữ nhật
- Chu vi và diện tích hình vuông
- Các loại góc (vuông, nhọn, tù, bẹt)
- Công cụ tính nhanh tương tác

### 📏 Đo Lường
- Đơn vị đo độ dài: mm, cm, dm, m, km
- Đơn vị đo khối lượng: g, kg, yến, tạ, tấn
- Đơn vị đo thời gian: giây, phút, giờ, ngày, tuần, tháng, năm

### 📝 Toán Đố
| Dạng | Mô tả |
|------|-------|
| 🛒 Mua Sắm | Tính tổng tiền, tiền thừa |
| 🚗 Quãng Đường | Vận tốc × Thời gian |
| 🌳 Vườn Cây | Đếm theo hàng và cột |
| 🍬 Chia Kẹo | Chia có dư và chia hết |
| 🏡 Diện Tích | Chu vi, diện tích thực tế |
| 👨‍👦 Tuổi Tác | Tính tuổi sau N năm |

---

## 🚀 Hướng Dẫn Cài Đặt & Chạy

### Yêu Cầu Hệ Thống
- Python **3.9** trở lên
- pip (trình quản lý gói Python)

Bước 3 — Cài đặt thư viện
pip install -r requirements.txt

Bước 4 — Chạy ứng dụng
streamlit run app.py

Bước 5 — Mở trình duyệt
http://localhost:8501

cấu trúc project
math_grade4/
│
├── app.py                          # File chính — điều hướng & giao diện
│
├── topics/                         # Các module chủ đề
│   ├── __init__.py
│   ├── addition_subtraction.py     # Cộng & Trừ
│   ├── multiplication_division.py  # Nhân & Chia
│   ├── fractions.py                # Phân Số
│   ├── geometry.py                 # Hình Học
│   ├── measurement.py              # Đo Lường
│   └── word_problems.py            # Toán Đố
│
├── utils/                          # Tiện ích dùng chung
│   ├── __init__.py
│   └── generator.py                # Bộ tạo bài tập ngẫu nhiên
│
├── requirements.txt                # Danh sách thư viện
└── README.md                       # Tài liệu này


🛠️ Công Nghệ Sử Dụng
Công nghệ	Phiên bản	Mục đích
Python	3.9+	Ngôn ngữ lập trình chính
Streamlit	1.32+	Framework giao diện web
random	built-in	Tạo bài tập ngẫu nhiên
math	built-in	Tính ƯCLN cho phân số

👨‍💻 Tác Giả
Nguyễn Văn Công
Tác Giả & Nhà Phát Triển

Ứng dụng được xây dựng với mong muốn giúp các em học sinh luyện tập
toán một cách vui vẻ, hiệu quả và tự tin hơn mỗi ngày.

📄 Giấy Phép
MIT License — Tự do sử dụng, chỉnh sửa và phân phối.
© 2026 Nguyễn Văn Công
