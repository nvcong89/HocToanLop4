import streamlit as st
import random
from utils.generator import gen_perimeter_rectangle, gen_perimeter_square

def show():
    st.markdown("## 📐 Hình Học")

    tab1, tab2, tab3 = st.tabs(["📖 Lý Thuyết", "✏️ Luyện Tập", "🎨 Vẽ Hình"])

    with tab1:
        st.markdown("""
        ### 📌 Hình Chữ Nhật
        - **Chu vi** = (chiều dài + chiều rộng) × 2
        - **Diện tích** = chiều dài × chiều rộng

        ### 📌 Hình Vuông
        - **Chu vi** = cạnh × 4
        - **Diện tích** = cạnh × cạnh

        ### 📌 Đơn Vị Đo Diện Tích
        | Đơn vị | Ký hiệu | Quy đổi |
        |--------|---------|---------|
        | cm vuông | cm² | 1 cm² = 100 mm² |
        | dm vuông | dm² | 1 dm² = 100 cm² |
        | m vuông  | m²  | 1 m² = 100 dm² |

        ### 📌 Góc
        - **Góc vuông**: 90°
        - **Góc nhọn**: < 90°
        - **Góc tù**: > 90° và < 180°
        - **Góc bẹt**: 180°
        """)

    with tab2:
        st.markdown("### ✏️ Tính Chu Vi & Diện Tích")
        shape = st.radio("Chọn hình:", ["Hình Chữ Nhật", "Hình Vuông", "Hỗn hợp"], horizontal=True)
        num_q = st.slider("Số câu:", 3, 8, 4, key="geo_num")

        if st.button("🎲 Tạo Bài Hình Học", key="gen_geo"):
            problems = []
            for _ in range(num_q):
                if shape == "Hình Chữ Nhật" or (shape == "Hỗn hợp" and random.random() > 0.5):
                    a, b, p, area = gen_perimeter_rectangle()
                    ask = random.choice(["perimeter", "area", "find_side"])
                    problems.append({"shape": "rect", "a": a, "b": b, "p": p, "area": area, "ask": ask})
                else:
                    a, p, area = gen_perimeter_square()
                    ask = random.choice(["perimeter", "area"])
                    problems.append({"shape": "square", "a": a, "p": p, "area": area, "ask": ask})
            st.session_state["geo_problems"] = problems
            st.session_state["geo_user"] = {}

        if "geo_problems" in st.session_state:
            problems = st.session_state["geo_problems"]
            user = st.session_state.get("geo_user", {})

            for i, p in enumerate(problems):
                if p["shape"] == "rect":
                    if p["ask"] == "perimeter":
                        st.markdown(f"**Câu {i+1}:** Hình chữ nhật có chiều dài **{p['a']} cm**, chiều rộng **{p['b']} cm**. Tính chu vi (cm).")
                        user[i] = (st.number_input("Chu vi:", key=f"geo_{i}", value=0, step=1), p["p"])
                    elif p["ask"] == "area":
                        st.markdown(f"**Câu {i+1}:** Hình chữ nhật có chiều dài **{p['a']} cm**, chiều rộng **{p['b']} cm**. Tính diện tích (cm²).")
                        user[i] = (st.number_input("Diện tích:", key=f"geo_{i}", value=0, step=1), p["area"])
                    else:
                        st.markdown(f"**Câu {i+1}:** Hình chữ nhật có chu vi **{p['p']} cm**, chiều dài **{p['a']} cm**. Tính chiều rộng (cm).")
                        user[i] = (st.number_input("Chiều rộng:", key=f"geo_{i}", value=0, step=1), p["b"])
                else:
                    if p["ask"] == "perimeter":
                        st.markdown(f"**Câu {i+1}:** Hình vuông có cạnh **{p['a']} cm**. Tính chu vi (cm).")
                        user[i] = (st.number_input("Chu vi:", key=f"geo_{i}", value=0, step=1), p["p"])
                    else:
                        st.markdown(f"**Câu {i+1}:** Hình vuông có cạnh **{p['a']} cm**. Tính diện tích (cm²).")
                        user[i] = (st.number_input("Diện tích:", key=f"geo_{i}", value=0, step=1), p["area"])

            st.session_state["geo_user"] = user

            if st.button("✅ Kiểm Tra Hình Học", key="check_geo"):
                correct = sum(1 for v, ans in user.values() if v == ans)
                for i, (v, ans) in user.items():
                    if v == ans:
                        st.markdown(f'<div class="correct-answer">✅ Câu {i+1}: {ans} — Đúng!</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="wrong-answer">❌ Câu {i+1}: Đáp án đúng là {ans}</div>', unsafe_allow_html=True)
                st.session_state.score += correct
                st.session_state.total += len(problems)
                st.success(f"🎉 Đúng {correct}/{len(problems)} câu!")

    with tab3:
        st.markdown("### 🎨 Công Cụ Tính Nhanh")
        shape_calc = st.radio("Chọn hình:", ["Hình Chữ Nhật", "Hình Vuông"], horizontal=True, key="calc_shape")

        if shape_calc == "Hình Chữ Nhật":
            c1, c2 = st.columns(2)
            with c1:
                length = st.number_input("Chiều dài (cm):", min_value=1, value=5, key="calc_l")
            with c2:
                width = st.number_input("Chiều rộng (cm):", min_value=1, value=3, key="calc_w")
            st.markdown(f"""
            **Kết quả:**
            - 📏 Chu vi = (chiều dài + chiều rộng) × 2 = ({length} + {width}) × 2 = **{2*(length+width)} cm**
            - 📐 Diện tích = chiều dài × chiều rộng = {length} × {width} = **{length*width} cm²**
            """)
        else:
            side = st.number_input("Độ dài cạnh (cm):", min_value=1, value=5, key="calc_s")
            st.markdown(f"""
            **Kết quả:**
            - 📏 Chu vi = cạnh × 4 = {side} × 4 = **{4*side} cm**
            - 📐 Diện tích = cạnh × cạnh = {side} × {side} = **{side*side} cm²**
            """)
