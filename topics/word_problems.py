import streamlit as st
import random


# ─── Problem Generators ───────────────────────────────────────

def gen_shopping_problem():
    items = [
        ("quyển vở", random.randint(3, 15) * 1000),
        ("cái bút", random.randint(2, 8) * 1000),
        ("hộp màu", random.randint(15, 40) * 1000),
        ("cái thước", random.randint(5, 12) * 1000),
        ("quyển sách", random.randint(20, 60) * 1000),
    ]
    item1, price1 = random.choice(items)
    item2, price2 = random.choice([x for x in items if x[0] != item1])
    qty1 = random.randint(2, 5)
    qty2 = random.randint(2, 5)
    total = qty1 * price1 + qty2 * price2
    money = (total // 10000 + random.randint(1, 5)) * 10000
    change = money - total

    question = (
        f"Mẹ mua {qty1} {item1} (mỗi cái {price1:,} đồng) và {qty2} {item2} "
        f"(mỗi cái {price2:,} đồng). Mẹ đưa {money:,} đồng. "
        f"Hỏi mẹ được trả lại bao nhiêu tiền?"
    ).replace(",", ".")

    hint = (
        f"**Bước 1:** Tiền {qty1} {item1} = {qty1} × {price1:,} = {qty1 * price1:,} đồng\n\n"
        f"**Bước 2:** Tiền {qty2} {item2} = {qty2} × {price2:,} = {qty2 * price2:,} đồng\n\n"
        f"**Bước 3:** Tổng tiền = {qty1 * price1:,} + {qty2 * price2:,} = {total:,} đồng\n\n"
        f"**Bước 4:** Tiền thừa = {money:,} - {total:,} = **{change:,} đồng**"
    ).replace(",", ".")

    return question, change, hint


def gen_distance_problem():
    speed = random.choice([30, 40, 45, 50, 60])
    time_h = random.randint(2, 5)
    distance = speed * time_h
    question = (
        f"Một xe ô tô đi với vận tốc {speed} km/giờ. "
        f"Hỏi sau {time_h} giờ xe đi được bao nhiêu km?"
    )
    hint = (
        f"**Quãng đường** = Vận tốc × Thời gian\n\n"
        f"= {speed} × {time_h} = **{distance} km**"
    )
    return question, distance, hint


def gen_farm_problem():
    rows = random.randint(4, 10)
    trees_per_row = random.randint(5, 15)
    total = rows * trees_per_row
    extra = random.randint(1, 5)
    question = (
        f"Vườn cây có {rows} hàng, mỗi hàng có {trees_per_row} cây. "
        f"Người ta trồng thêm {extra} cây nữa. "
        f"Hỏi vườn có tất cả bao nhiêu cây?"
    )
    ans = total + extra
    hint = (
        f"**Bước 1:** Số cây ban đầu = {rows} × {trees_per_row} = {total} cây\n\n"
        f"**Bước 2:** Tổng cây = {total} + {extra} = **{ans} cây**"
    )
    return question, ans, hint


def gen_sharing_problem():
    total_candy = random.randint(50, 200)
    people = random.randint(3, 8)
    each = total_candy // people
    remainder = total_candy % people

    if remainder == 0:
        question = (
            f"Có {total_candy} cái kẹo chia đều cho {people} bạn. "
            f"Hỏi mỗi bạn nhận được bao nhiêu cái kẹo?"
        )
        hint = (
            f"**Phép tính:** {total_candy} ÷ {people} = **{each} cái**"
        )
        # Use a simple integer answer (no remainder)
        return question, each, hint
    else:
        question = (
            f"Có {total_candy} cái kẹo chia đều cho {people} bạn. "
            f"Hỏi mỗi bạn nhận được bao nhiêu cái kẹo và còn thừa bao nhiêu cái?"
        )
        hint = (
            f"**Phép tính:** {total_candy} ÷ {people} = {each} (dư {remainder})\n\n"
            f"Mỗi bạn nhận **{each} cái**, còn thừa **{remainder} cái**"
        )
        # Encode: ans = each * 1000 + remainder (both < 1000 guaranteed)
        return question, each * 1000 + remainder, hint


def gen_area_problem():
    length = random.randint(5, 25)
    width = random.randint(3, 15)
    area = length * width
    ptype = random.choice(["area", "fence"])

    if ptype == "area":
        question = (
            f"Một mảnh vườn hình chữ nhật có chiều dài {length} m, "
            f"chiều rộng {width} m. Tính diện tích mảnh vườn (m²)."
        )
        ans = area
        hint = (
            f"**Diện tích** = chiều dài × chiều rộng\n\n"
            f"= {length} × {width} = **{area} m²**"
        )
    else:
        perimeter = 2 * (length + width)
        question = (
            f"Người ta muốn rào xung quanh mảnh vườn hình chữ nhật "
            f"dài {length} m, rộng {width} m. "
            f"Hỏi cần bao nhiêu mét hàng rào?"
        )
        ans = perimeter
        hint = (
            f"**Chu vi** = (chiều dài + chiều rộng) × 2\n\n"
            f"= ({length} + {width}) × 2 = {length + width} × 2 = **{perimeter} m**"
        )
    return question, ans, hint


def gen_age_problem():
    child_age = random.randint(8, 12)
    diff = random.randint(20, 35)
    parent_age = child_age + diff
    years_later = random.randint(3, 10)
    question = (
        f"Năm nay bạn An {child_age} tuổi, bố An {parent_age} tuổi. "
        f"Hỏi sau {years_later} năm nữa, tổng số tuổi của hai bố con là bao nhiêu?"
    )
    ans = (child_age + years_later) + (parent_age + years_later)
    hint = (
        f"**Sau {years_later} năm:**\n\n"
        f"- Tuổi An = {child_age} + {years_later} = {child_age + years_later}\n\n"
        f"- Tuổi bố = {parent_age} + {years_later} = {parent_age + years_later}\n\n"
        f"- Tổng = {child_age + years_later} + {parent_age + years_later} = **{ans} tuổi**"
    )
    return question, ans, hint


PROBLEM_GENERATORS = {
    "🛒 Mua Sắm": gen_shopping_problem,
    "🚗 Quãng Đường": gen_distance_problem,
    "🌳 Vườn Cây": gen_farm_problem,
    "🍬 Chia Kẹo": gen_sharing_problem,
    "🏡 Diện Tích": gen_area_problem,
    "👨‍👦 Tuổi Tác": gen_age_problem,
}


# ─── Helper: check if problem is "sharing with remainder" type ────
def _is_sharing_encoded(p):
    """Return True if answer is encoded as each*1000 + remainder."""
    return (
        p["ans"] > 1000
        and p["ans"] % 1000 != 0
        and "chia" in p["q"].lower()
    )


# ─── Render input for one problem ─────────────────────────────
def _render_input(i, p, key_prefix):
    if _is_sharing_encoded(p):
        c1, c2 = st.columns(2)
        with c1:
            u_each = st.number_input(
                "Mỗi bạn nhận (cái):",
                key=f"{key_prefix}_each_{i}",
                value=0, step=1, min_value=0
            )
        with c2:
            u_rem = st.number_input(
                "Còn thừa (cái):",
                key=f"{key_prefix}_rem_{i}",
                value=0, step=1, min_value=0
            )
        return u_each * 1000 + u_rem
    else:
        return st.number_input(
            "Đáp số:",
            key=f"{key_prefix}_{i}",
            value=0, step=1, min_value=0
        )


# ─── Format answer for display ────────────────────────────────
def _format_ans(p):
    if _is_sharing_encoded(p):
        each = p["ans"] // 1000
        rem  = p["ans"] % 1000
        return f"mỗi bạn {each} cái, thừa {rem} cái"
    return f"{p['ans']:,}".replace(",", ".")


# ─── Main show() ──────────────────────────────────────────────
def show():
    st.markdown("## 📝 Toán Đố — Bài Toán Có Lời Văn")

    # ── Liên kết SGK ──────────────────────────────────────────
    from utils.pdf_viewer import render_page_links
    with st.expander("📖 Xem trang SGK liên quan", expanded=False):
        render_page_links("📝 Toán Đố")

    tab1, tab2, tab3 = st.tabs(["📖 Hướng Dẫn", "✏️ Luyện Tập", "🎯 Thi Thử"])

    # ── Tab 1: Hướng dẫn ──────────────────────────────────────
    with tab1:
        st.markdown("""
        ### 📌 Các Bước Giải Toán Có Lời Văn

        **Bước 1 — Đọc kỹ đề bài** 📖
        > Hiểu bài toán hỏi gì, cho biết gì.

        **Bước 2 — Tóm tắt đề bài** ✏️
        > Ghi lại các dữ kiện quan trọng bằng ký hiệu ngắn gọn.

        **Bước 3 — Lập kế hoạch giải** 🧠
        > Xác định phép tính cần dùng (cộng, trừ, nhân, chia).

        **Bước 4 — Thực hiện tính toán** 🔢
        > Tính từng bước, ghi rõ đơn vị.

        **Bước 5 — Kiểm tra lại** ✅
        > Đọc lại đề, kiểm tra đáp số có hợp lý không.

        ---

        ### 🗂️ Các Dạng Toán Đố Lớp 4
        | Dạng | Mô tả |
        |------|-------|
        | 🛒 Mua Sắm | Tính tổng tiền, tiền thừa |
        | 🚗 Quãng Đường | Quãng đường = vận tốc × thời gian |
        | 🌳 Vườn Cây | Tính số lượng theo hàng, cột |
        | 🍬 Chia Kẹo | Chia có dư, chia hết |
        | 🏡 Diện Tích | Diện tích, chu vi sân vườn |
        | 👨‍👦 Tuổi Tác | Tính tuổi sau N năm |
        """)

    # ── Tab 2: Luyện tập ──────────────────────────────────────
    with tab2:
        st.markdown("### ✏️ Luyện Tập Toán Đố")

        col1, col2 = st.columns([1, 2])
        with col1:
            selected_type = st.selectbox(
                "Chọn dạng toán:",
                list(PROBLEM_GENERATORS.keys()) + ["🔀 Ngẫu nhiên"],
                key="wp_type_select"
            )
            num_q = st.slider("Số bài:", 1, 5, 3, key="wp_num")

        with col2:
            if st.button("🎲 Tạo Bài Toán Đố", use_container_width=True, key="gen_wp"):
                problems = []
                for _ in range(num_q):
                    if selected_type == "🔀 Ngẫu nhiên":
                        gen_fn = random.choice(list(PROBLEM_GENERATORS.values()))
                    else:
                        gen_fn = PROBLEM_GENERATORS[selected_type]
                    q, ans, hint = gen_fn()
                    problems.append({"q": q, "ans": ans, "hint": hint})
                st.session_state["wp_problems"]    = problems
                st.session_state["wp_user"]        = {}
                st.session_state["wp_show_hints"]  = {}
                st.session_state["wp_submitted"]   = False

        if "wp_problems" in st.session_state and not st.session_state.get("wp_submitted", False):
            problems   = st.session_state["wp_problems"]
            user       = st.session_state.get("wp_user", {})
            show_hints = st.session_state.get("wp_show_hints", {})

            for i, p in enumerate(problems):
                st.markdown("---")
                st.markdown(f"### 📝 Bài {i + 1}")
                st.info(p["q"])

                # Hint toggle
                if st.button(f"💡 Xem Gợi Ý Bài {i + 1}", key=f"hint_btn_{i}"):
                    show_hints[i] = not show_hints.get(i, False)
                    st.session_state["wp_show_hints"] = show_hints

                if show_hints.get(i, False):
                    st.markdown(
                        f'<div class="hint-box">💡 <b>Gợi ý:</b><br>{p["hint"]}</div>',
                        unsafe_allow_html=True
                    )

                user[i] = _render_input(i, p, "wp")

            st.session_state["wp_user"] = user
            st.markdown("---")

            if st.button("✅ Nộp Bài Toán Đố", use_container_width=True, key="submit_wp"):
                correct = 0
                for i, p in enumerate(problems):
                    if user.get(i) == p["ans"]:
                        correct += 1
                        st.markdown(
                            f'<div class="correct-answer">✅ Bài {i + 1}: Đúng! 🎉</div>',
                            unsafe_allow_html=True
                        )
                    else:
                        st.markdown(
                            f'<div class="wrong-answer">'
                            f'❌ Bài {i + 1}: Đáp án đúng là <b>{_format_ans(p)}</b><br>'
                            f'<small>{p["hint"]}</small>'
                            f'</div>',
                            unsafe_allow_html=True
                        )
                st.session_state.score += correct
                st.session_state.total += len(problems)
                st.session_state["wp_submitted"] = True
                st.success(f"🎉 Bạn đúng {correct}/{len(problems)} bài!")

    # ── Tab 3: Thi thử ────────────────────────────────────────
    with tab3:
        st.markdown("### 🎯 Thi Thử — 5 Bài Ngẫu Nhiên")
        st.markdown("Hoàn thành 5 bài toán đố ngẫu nhiên để nhận điểm tổng kết!")

        if st.button("🚀 Bắt Đầu Thi Thử", key="start_exam"):
            generators = list(PROBLEM_GENERATORS.values())
            random.shuffle(generators)
            exam_problems = []
            for gen_fn in generators[:5]:
                q, ans, hint = gen_fn()
                exam_problems.append({"q": q, "ans": ans, "hint": hint})
            st.session_state["exam_problems"]  = exam_problems
            st.session_state["exam_user"]      = {}
            st.session_state["exam_submitted"] = False

        if (
            "exam_problems" in st.session_state
            and not st.session_state.get("exam_submitted", False)
        ):
            exam_problems = st.session_state["exam_problems"]
            exam_user     = st.session_state.get("exam_user", {})

            for i, p in enumerate(exam_problems):
                st.markdown(f"**Bài {i + 1}/5:** {p['q']}")
                exam_user[i] = _render_input(i, p, "ex")
                st.markdown("")

            st.session_state["exam_user"] = exam_user

            if st.button("📨 Nộp Bài Thi", use_container_width=True, key="submit_exam"):
                correct = sum(
                    1 for i, p in enumerate(exam_problems)
                    if exam_user.get(i) == p["ans"]
                )
                st.session_state["exam_submitted"] = True
                st.session_state["exam_score"]     = correct
                st.session_state.score += correct
                st.session_state.total += 5

        if st.session_state.get("exam_submitted", False):
            score = st.session_state.get("exam_score", 0)
            pct   = score / 5 * 100

            if score == 5:
                emoji, msg = "🏆", "Xuất sắc! Bạn đúng tất cả!"
            elif score >= 4:
                emoji, msg = "🥇", "Giỏi lắm! Gần hoàn hảo rồi!"
            elif score >= 3:
                emoji, msg = "🥈", "Khá tốt! Cố gắng thêm nhé!"
            else:
                emoji, msg = "📚", "Hãy ôn luyện thêm nhé!"

            st.markdown(f"""
            <div class="score-box">
                {emoji} Kết Quả Thi Thử<br>
                <span style="font-size:2rem">{score}/5</span><br>
                <small>{pct:.0f}% — {msg}</small>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("### 📋 Đáp Án Chi Tiết")
            exam_problems = st.session_state.get("exam_problems", [])
            exam_user     = st.session_state.get("exam_user", {})

            for i, p in enumerate(exam_problems):
                if exam_user.get(i) == p["ans"]:
                    st.markdown(
                        f'<div class="correct-answer">✅ Bài {i + 1}: Đúng!</div>',
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown(
                        f'<div class="wrong-answer">'
                        f'❌ Bài {i + 1}: Đáp án = <b>{_format_ans(p)}</b><br>'
                        f'<small>{p["hint"]}</small>'
                        f'</div>',
                        unsafe_allow_html=True
                    )
