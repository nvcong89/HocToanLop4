# 🎓 Quy tắc Dự án - Học Toán Lớp 4

Tài liệu này định nghĩa các quy tắc lập trình, tiêu chuẩn thiết kế và cách tương tác để định hướng cho Agent hoạt động chính xác trong dự án **Học Toán Lớp 4**.

---

## 🛠️ Công Nghệ & Thư Viện Sử Dụng

*   **Ngôn ngữ chính**: Python 3.9+
*   **Framework Giao Diện**: Streamlit >= 1.32.0 (sử dụng các thành phần tương tác trực quan).
*   **Thư viện bổ trợ**:
    *   `streamlit-pdf-viewer` để hiển thị lý thuyết/tài liệu học tập dạng PDF.
    *   `groq` và `python-dotenv` để tích hợp AI Tutor hướng dẫn giải bài.
    *   Hạn chế tự ý cài đặt thêm thư viện ngoài nếu không có sự đồng ý của người dùng.
*   **Môi trường**: Luôn cập nhật [requirements.txt](file:///c:/Users/210608/Documents/GitHub/HocToanLop4/requirements.txt) khi có thư viện mới được bổ sung.

---

## 📂 Cấu Trúc Mã Nguồn Chuẩn

Mã nguồn được tổ chức rõ ràng theo mô hình module:
*   [app.py](file:///c:/Users/210608/Documents/GitHub/HocToanLop4/app.py): File chạy chính chứa giao diện điều hướng, sidebar, cấu hình trang và nhúng các module chủ đề.
*   [topics/](file:///c:/Users/210608/Documents/GitHub/HocToanLop4/topics/): Chứa logic và giao diện cho từng chủ đề toán học riêng biệt:
    *   Phép cộng/trừ: `addition_subtraction.py`
    *   Phép nhân/chia: `multiplication_division.py`
    *   Phân số: `fractions.py`
    *   Hình học: `geometry.py`
    *   Đo lường: `measurement.py`
    *   Toán đố: `word_problems.py`
*   [utils/](file:///c:/Users/210608/Documents/GitHub/HocToanLop4/utils/): Chứa các tiện ích dùng chung:
    *   `generator.py`: Bộ tạo bài tập ngẫu nhiên.
    *   `ai_tutor.py`: Logic tương tác với AI Tutor.
    *   `pdf_viewer.py`: Bộ hiển thị tài liệu PDF.

---

## 🎨 Tiêu Chuẩn Giao Diện & Trải Nghiệm Người Dùng (UX/UI)

Vì đối tượng sử dụng là học sinh Lớp 4, giao diện cần đảm bảo:
*   **Phong cách thiết kế**: Trực quan, tươi sáng, sử dụng màu sắc tươi tắn (tránh các tone màu xám xịt hoặc quá tối).
*   **Màu sắc thông báo**:
    *   Đúng: Nền xanh lá nhạt (`.correct-answer`)
    *   Sai: Nền đỏ nhạt (`.wrong-answer`)
    *   Gợi ý: Nền vàng nhạt (`.hint-box`)
*   **Kiểu chữ**: Sử dụng font chữ 'Nunito' (đã định cấu hình sẵn trong [app.py](file:///c:/Users/210608/Documents/GitHub/HocToanLop4/app.py)).
*   **Micro-interactions**: Sử dụng hover effect trên các thẻ bài học (`.topic-card`) để tăng tính tương tác.

---

## 📝 Quy Tắc Tạo Bài Tập & Sư Phạm

*   **Tính ngẫu nhiên**: Luôn sử dụng thư viện `random` của Python để sinh đề bài ngẫu nhiên. Không sử dụng các đề bài cố định để tránh học sinh học vẹt.
*   **Mức độ khó**: Hỗ trợ 3 mức độ (Dễ, Trung bình, Khó) tùy theo chủ đề.
*   **Logic toán học**:
    *   **Phép chia**: Kiểm tra mẫu số hoặc số chia khác 0. Đảm bảo phân biệt rõ ràng giữa chia hết và chia có dư.
    *   **Phân số**: Sử dụng `math.gcd` để tự động rút gọn kết quả về phân số tối giản trước khi so sánh hoặc hiển thị.
*   **Gợi ý từng bước (Hints)**: Mỗi bài tập khi làm sai hoặc khi học sinh yêu cầu đều phải đi kèm giải thích/gợi ý chi tiết từng bước bằng tiếng Việt thân thiện, dễ hiểu.
*   **Văn phong**: Sử dụng tiếng Việt chuẩn sư phạm tiểu học, khích lệ và động viên học sinh khi làm bài.

---

## 💾 Quản Lý Trạng Thái (Streamlit Session State)

*   Luôn lưu điểm số, câu hỏi hiện tại, trạng thái đã trả lời (đúng/sai) vào `st.session_state` để tránh mất dữ liệu của học sinh khi trang bị reload/rerun.
*   Đảm bảo có nút "Làm bài khác" hoặc "Đặt lại" để dọn dẹp state và sinh câu hỏi mới một cách mượt mà.
