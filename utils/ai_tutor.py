import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# ── Khởi tạo client ───────────────────────────────────────────
apikey = "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"
#client = Groq(api_key=os.getenv("GROQ_API_KEY"))
client = Groq(api_key="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"
)

SYSTEM_PROMPT = """
Bạn là một gia sư toán thân thiện, chuyên dạy học sinh lớp 4 Việt Nam.
Nguyên tắc trả lời:
- Luôn dùng tiếng Việt, ngôn ngữ đơn giản, dễ hiểu
- Giải thích từng bước một, rõ ràng
- Dùng ví dụ thực tế gần gũi (trái cây, đồ vật, tiền...)
- Khuyến khích và động viên học sinh
- Không giải thích quá dài, tối đa 150 từ mỗi câu trả lời
- Nếu học sinh làm sai, chỉ ra lỗi nhẹ nhàng và hướng dẫn lại
"""


def ask_ai(question: str, chat_history: list = []) -> str:
    """
    Gửi câu hỏi đến Groq và nhận câu trả lời.
    chat_history: list các dict {"role": "user/assistant", "content": "..."}
    """
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages += chat_history
    messages.append({"role": "user", "content": question})

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages,
            max_tokens=300,
            temperature=0.7,
        )
        return response.choices[0].message.content

    except Exception as e:
        return f"⚠️ Lỗi kết nối AI: {str(e)}"


def explain_wrong_answer(
    question: str,
    correct_answer: str,
    student_answer: str,
    topic: str
) -> str:
    """
    AI giải thích tại sao học sinh làm sai
    và hướng dẫn cách làm đúng.
    """
    prompt = f"""
Học sinh lớp 4 đang học chủ đề: {topic}

Bài toán: {question}
Đáp án đúng: {correct_answer}
Học sinh trả lời: {student_answer}

Hãy:
1. Nhẹ nhàng chỉ ra học sinh sai ở đâu
2. Giải thích cách làm đúng từng bước
3. Động viên học sinh thử lại
"""
    return ask_ai(prompt)


def generate_hint(question: str, topic: str) -> str:
    """Tạo gợi ý cho bài toán mà không tiết lộ đáp án."""
    prompt = f"""
Bài toán toán lớp 4 ({topic}): {question}

Hãy đưa ra 1 gợi ý nhỏ giúp học sinh tự tìm ra đáp án.
KHÔNG được nói đáp án, chỉ gợi ý hướng suy nghĩ.
Tối đa 2 câu.
"""
    return ask_ai(prompt)
