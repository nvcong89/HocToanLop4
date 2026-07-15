import streamlit as st
import random
from math import gcd
from utils.generator import gen_fraction_compare, gen_fraction_add_sub
from utils.ai_tutor import explain_wrong_answer, generate_hint


def simplify(n, d):
    g = gcd(abs(n), abs(d))
    return n // g, d // g


def show():
    st.markdown("## 🍕 Phân Số")

    # ── Liên kết SGK ──────────────────────────────────────────
    from utils.pdf_viewer import render_page_links
    with st.expander("📖 Xem trang SGK liên quan", expanded=False):
        render_page_links("🍕 Phân Số")

    tab1, tab2, tab3, tab4 = st.tabs([
        "📖 Lý Thuyết", "⚖️ So Sánh", "➕ Cộng/Trừ", "🔢 Rút Gọn"
    ])

    # ══════════════════════════════════════════════════════════
    with tab1:
        st.markdown("""
        ### 📌 Phân Số Là Gì?
        Phân số có dạng **a/b** (b ≠ 0), trong đó:
        - **a** là **tử số** (phần được lấy)
        - **b** là **mẫu số** (chia thành bao nhiêu phần bằng nhau)

        **Ví dụ:** 3/4 nghĩa là chia 1 cái bánh thành 4 phần bằng nhau, lấy 3 phần.

        ### 📌 So Sánh Phân Số
        - Cùng mẫu số: so sánh tử số
        - Khác mẫu số: quy đồng mẫu số rồi so sánh

        ### 📌 Rút Gọn Phân Số
        Chia cả tử và mẫu cho **ƯCLN** của chúng.

        **Ví dụ:** 6/8 → ƯCLN(6,8) = 2 → 6÷2 / 8÷2 = **3/4**

        ### 📌 Phân Số Bằng Nhau
        a/b = c/d khi a × d = b × c
        """)

        st.markdown("### 🎨 Minh Họa Phân Số")
        col1, col2 = st.columns(2)
        with col1:
            demo_n = st.number_input("Tử số:", 1, 10, 3, key="demo_n")
        with col2:
            demo_d = st.number_input("Mẫu số:", 1, 10, 4, key="demo_d")

        if demo_d > 0 and demo_n <= demo_d:
            filled = "🟦" * demo_n + "⬜" * (demo_d - demo_n)
            st.markdown(f"**{demo_n}/{demo_d}** = {filled}")
            st.markdown(f"Phần được tô màu: **{demo_n}** trong **{demo_d}** phần bằng nhau")
        elif demo_n > demo_d:
            st.warning("Đây là phân số lớn hơn 1 (phân số giả)!")

    # ══════════════════════════════════════════════════════════
    with tab2:
        st.markdown("### ⚖️ So Sánh Phân Số")

        if st.button("🎲 Tạo Bài So Sánh", key="gen_compare"):
            st.session_state["frac_compare"] = [gen_fraction_compare() for _ in range(5)]
            st.session_state["frac_compare_ans"] = {}
            # Reset AI state
            st.session_state.pop("cmp_wrong_list",   None)
            st.session_state.pop("cmp_hint_text",    None)
            st.session_state.pop("cmp_explain_text", None)

        if "frac_compare" in st.session_state:
            problems = st.session_state["frac_compare"]
            user_signs = {}

            for i, (n1, d1, n2, d2, correct_sign) in enumerate(problems):
                st.markdown(f"**Câu {i+1}:** {n1}/{d1} ☐ {n2}/{d2}")
                user_signs[i] = st.selectbox(
                    f"Chọn dấu câu {i+1}:",
                    [">", "<", "="],
                    key=f"cmp_{i}",
                    label_visibility="collapsed"
                )

            if st.button("✅ Kiểm Tra So Sánh", key="check_compare"):
                correct   = 0
                wrong_list = []
                details = []

                for i, (n1, d1, n2, d2, correct_sign) in enumerate(problems):
                    is_ok = user_signs[i] == correct_sign
                    details.append({
                        "question": f"{n1}/{d1} ☐ {n2}/{d2}",
                        "correct_answer": correct_sign,
                        "student_answer": user_signs[i],
                        "is_correct": is_ok
                    })
                    if is_ok:
                        correct += 1
                        st.markdown(
                            f'<div class="correct-answer">✅ Câu {i+1}: '
                            f'{n1}/{d1} {correct_sign} {n2}/{d2} — Đúng!</div>',
                            unsafe_allow_html=True
                        )
                    else:
                        st.markdown(
                            f'<div class="wrong-answer">❌ Câu {i+1}: '
                            f'{n1}/{d1} <b>{correct_sign}</b> {n2}/{d2} '
                            f'(bạn chọn: {user_signs[i]})</div>',
                            unsafe_allow_html=True
                        )
                        wrong_list.append({
                            "question": f"{n1}/{d1} ☐ {n2}/{d2}",
                            "correct":  correct_sign,
                            "student":  user_signs[i],
                        })

                st.session_state.score += correct
                st.session_state.total += len(problems)
                st.success(f"🎉 Đúng {correct}/{len(problems)} câu!")
                st.session_state["cmp_wrong_list"] = wrong_list
                
                # Lưu lịch sử
                from utils.history import save_attempt
                save_attempt("🍕 Phân Số", "So Sánh", details, correct, len(problems))
                # Reset nội dung AI cũ khi kiểm tra lại
                st.session_state.pop("cmp_hint_text",    None)
                st.session_state.pop("cmp_explain_text", None)

            # ── AI hỗ trợ ─────────────────────────────────────
            wrong_list = st.session_state.get("cmp_wrong_list", [])
            if wrong_list:
                st.markdown("---")
                st.markdown("#### 🤖 Hỗ Trợ AI")

                wrong_labels = [
                    f"Câu: {w['question']} (bạn chọn '{w['student']}')"
                    for w in wrong_list
                ]
                selected_idx = 0
                if len(wrong_list) > 1:
                    selected = st.selectbox(
                        "Chọn câu muốn hỏi AI:",
                        wrong_labels,
                        key="cmp_select_wrong"
                    )
                    selected_idx = wrong_labels.index(selected)
                chosen = wrong_list[selected_idx]

                col_hint, col_explain = st.columns(2)

                with col_hint:
                    if st.button("💡 Gợi ý", key="cmp_hint"):
                        with st.spinner("AI đang nghĩ..."):
                            st.session_state["cmp_hint_text"] = generate_hint(
                                chosen["question"], "So Sánh Phân Số"
                            )
                    if "cmp_hint_text" in st.session_state:
                        st.info(f"💡 {st.session_state['cmp_hint_text']}")

                with col_explain:
                    if st.button("🤖 Giải thích", key="cmp_explain"):
                        with st.spinner("AI đang giải thích..."):
                            st.session_state["cmp_explain_text"] = explain_wrong_answer(
                                question       = chosen["question"],
                                correct_answer = chosen["correct"],
                                student_answer = chosen["student"],
                                topic          = "So Sánh Phân Số"
                            )
                    if "cmp_explain_text" in st.session_state:
                        st.warning(f"🤖 {st.session_state['cmp_explain_text']}")

    # ══════════════════════════════════════════════════════════
    with tab3:
        st.markdown("### ➕ Cộng & Trừ Phân Số Cùng Mẫu")
        op_frac = st.radio("Phép tính:", ["Cộng ➕", "Trừ ➖"], horizontal=True)

        if st.button("🎲 Tạo Bài Cộng/Trừ", key="gen_frac_add"):
            op = "add" if op_frac == "Cộng ➕" else "sub"
            st.session_state["frac_add_problems"] = [gen_fraction_add_sub(op) for _ in range(5)]
            st.session_state["frac_add_op"] = op
            # Reset AI state
            st.session_state.pop("add_wrong_list",   None)
            st.session_state.pop("add_hint_text",    None)
            st.session_state.pop("add_explain_text", None)

        if "frac_add_problems" in st.session_state:
            problems = st.session_state["frac_add_problems"]
            op       = st.session_state.get("frac_add_op", "add")
            user_ans = {}

            for i, (n1, d1, n2, d2, rn, rd, sym) in enumerate(problems):
                st.markdown(f"**Câu {i+1}:** {n1}/{d1} {sym} {n2}/{d2} = ?/? (rút gọn nếu được)")
                c1, c2 = st.columns(2)
                with c1:
                    user_ans[f"{i}_n"] = st.number_input("Tử số:", key=f"fan_{i}", value=0, step=1)
                with c2:
                    user_ans[f"{i}_d"] = st.number_input("Mẫu số:", key=f"fad_{i}", value=1, step=1)

            if st.button("✅ Kiểm Tra", key="check_frac_add"):
                correct    = 0
                wrong_list = []
                details = []

                for i, (n1, d1, n2, d2, rn, rd, sym) in enumerate(problems):
                    un = user_ans.get(f"{i}_n", 0)
                    ud = user_ans.get(f"{i}_d", 1)
                    ok = (un == rn and ud == rd) or (ud != 0 and rn * ud == rd * un)
                    details.append({
                        "question": f"{n1}/{d1} {sym} {n2}/{d2}",
                        "correct_answer": f"{rn}/{rd}",
                        "student_answer": f"{un}/{ud}",
                        "is_correct": ok
                    })
                    if ok:
                        correct += 1
                        st.markdown(
                            f'<div class="correct-answer">✅ Câu {i+1}: '
                            f'{n1}/{d1} {sym} {n2}/{d2} = {rn}/{rd} — Đúng!</div>',
                            unsafe_allow_html=True
                        )
                    else:
                        st.markdown(
                            f'<div class="wrong-answer">❌ Câu {i+1}: '
                            f'Đáp án đúng = {rn}/{rd}</div>',
                            unsafe_allow_html=True
                        )
                        wrong_list.append({
                            "question": f"{n1}/{d1} {sym} {n2}/{d2}",
                            "correct":  f"{rn}/{rd}",
                            "student":  f"{un}/{ud}",
                        })

                st.session_state.score += correct
                st.session_state.total += len(problems)
                st.success(f"🎉 Đúng {correct}/{len(problems)} câu!")
                st.session_state["add_wrong_list"] = wrong_list
                
                # Lưu lịch sử
                from utils.history import save_attempt
                save_attempt("🍕 Phân Số", "Cộng/Trừ", details, correct, len(problems))
                # Reset nội dung AI cũ khi kiểm tra lại
                st.session_state.pop("add_hint_text",    None)
                st.session_state.pop("add_explain_text", None)

            # ── AI hỗ trợ ─────────────────────────────────────
            wrong_list = st.session_state.get("add_wrong_list", [])
            if wrong_list:
                st.markdown("---")
                st.markdown("#### 🤖 Hỗ Trợ AI")

                wrong_labels = [
                    f"Câu: {w['question']} (bạn trả lời '{w['student']}')"
                    for w in wrong_list
                ]
                selected_idx = 0
                if len(wrong_list) > 1:
                    selected = st.selectbox(
                        "Chọn câu muốn hỏi AI:",
                        wrong_labels,
                        key="add_select_wrong"
                    )
                    selected_idx = wrong_labels.index(selected)
                chosen = wrong_list[selected_idx]

                col_hint, col_explain = st.columns(2)

                with col_hint:
                    if st.button("💡 Gợi ý", key="add_hint"):
                        with st.spinner("AI đang nghĩ..."):
                            st.session_state["add_hint_text"] = generate_hint(
                                chosen["question"], "Cộng Trừ Phân Số"
                            )
                    if "add_hint_text" in st.session_state:
                        st.info(f"💡 {st.session_state['add_hint_text']}")

                with col_explain:
                    if st.button("🤖 Giải thích", key="add_explain"):
                        with st.spinner("AI đang giải thích..."):
                            st.session_state["add_explain_text"] = explain_wrong_answer(
                                question       = chosen["question"],
                                correct_answer = chosen["correct"],
                                student_answer = chosen["student"],
                                topic          = "Cộng Trừ Phân Số"
                            )
                    if "add_explain_text" in st.session_state:
                        st.warning(f"🤖 {st.session_state['add_explain_text']}")

    # ══════════════════════════════════════════════════════════
    with tab4:
        st.markdown("### 🔢 Rút Gọn Phân Số")

        if st.button("🎲 Tạo Bài Rút Gọn", key="gen_simplify"):
            problems = []
            for _ in range(5):
                d     = random.choice([4, 6, 8, 9, 10, 12, 15, 16, 18, 20])
                g_val = random.choice([g for g in range(2, d) if d % g == 0])
                n_simplified = random.randint(1, d // g_val - 1)
                n    = n_simplified * g_val
                rn, rd = simplify(n, d)
                problems.append((n, d, rn, rd))
            st.session_state["simplify_problems"] = problems
            # Reset AI state
            st.session_state.pop("simp_wrong_list",   None)
            st.session_state.pop("simp_hint_text",    None)
            st.session_state.pop("simp_explain_text", None)

        if "simplify_problems" in st.session_state:
            problems = st.session_state["simplify_problems"]
            user_ans = {}

            for i, (n, d, rn, rd) in enumerate(problems):
                st.markdown(f"**Câu {i+1}:** Rút gọn phân số **{n}/{d}**")
                c1, c2 = st.columns(2)
                with c1:
                    user_ans[f"{i}_n"] = st.number_input("Tử số:", key=f"sn_{i}", value=0, step=1)
                with c2:
                    user_ans[f"{i}_d"] = st.number_input("Mẫu số:", key=f"sd_{i}", value=1, step=1)

            if st.button("✅ Kiểm Tra Rút Gọn", key="check_simplify"):
                correct    = 0
                wrong_list = []
                details = []

                for i, (n, d, rn, rd) in enumerate(problems):
                    un = user_ans.get(f"{i}_n", 0)
                    ud = user_ans.get(f"{i}_d", 1)
                    ok = (un == rn and ud == rd)
                    details.append({
                        "question": f"Rút gọn phân số {n}/{d}",
                        "correct_answer": f"{rn}/{rd}",
                        "student_answer": f"{un}/{ud}",
                        "is_correct": ok
                    })
                    if ok:
                        correct += 1
                        st.markdown(
                            f'<div class="correct-answer">✅ Câu {i+1}: '
                            f'{n}/{d} = {rn}/{rd} — Đúng!</div>',
                            unsafe_allow_html=True
                        )
                    else:
                        st.markdown(
                            f'<div class="wrong-answer">❌ Câu {i+1}: '
                            f'{n}/{d} rút gọn = {rn}/{rd}</div>',
                            unsafe_allow_html=True
                        )
                        wrong_list.append({
                            "question": f"Rút gọn phân số {n}/{d}",
                            "correct":  f"{rn}/{rd}",
                            "student":  f"{un}/{ud}",
                        })

                st.session_state.score += correct
                st.session_state.total += len(problems)
                st.success(f"🎉 Đúng {correct}/{len(problems)} câu!")
                st.session_state["simp_wrong_list"] = wrong_list
                
                # Lưu lịch sử
                from utils.history import save_attempt
                save_attempt("🍕 Phân Số", "Rút Gọn", details, correct, len(problems))
                # Reset nội dung AI cũ khi kiểm tra lại
                st.session_state.pop("simp_hint_text",    None)
                st.session_state.pop("simp_explain_text", None)

            # ── AI hỗ trợ ─────────────────────────────────────
            wrong_list = st.session_state.get("simp_wrong_list", [])
            if wrong_list:
                st.markdown("---")
                st.markdown("#### 🤖 Hỗ Trợ AI")

                wrong_labels = [
                    f"Câu: {w['question']} (bạn trả lời '{w['student']}')"
                    for w in wrong_list
                ]
                selected_idx = 0
                if len(wrong_list) > 1:
                    selected = st.selectbox(
                        "Chọn câu muốn hỏi AI:",
                        wrong_labels,
                        key="simp_select_wrong"
                    )
                    selected_idx = wrong_labels.index(selected)
                chosen = wrong_list[selected_idx]

                col_hint, col_explain = st.columns(2)

                with col_hint:
                    if st.button("💡 Gợi ý", key="simp_hint"):
                        with st.spinner("AI đang nghĩ..."):
                            st.session_state["simp_hint_text"] = generate_hint(
                                chosen["question"], "Rút Gọn Phân Số"
                            )
                    if "simp_hint_text" in st.session_state:
                        st.info(f"💡 {st.session_state['simp_hint_text']}")

                with col_explain:
                    if st.button("🤖 Giải thích", key="simp_explain"):
                        with st.spinner("AI đang giải thích..."):
                            st.session_state["simp_explain_text"] = explain_wrong_answer(
                                question       = chosen["question"],
                                correct_answer = chosen["correct"],
                                student_answer = chosen["student"],
                                topic          = "Rút Gọn Phân Số"
                            )
                    if "simp_explain_text" in st.session_state:
                        st.warning(f"🤖 {st.session_state['simp_explain_text']}")
