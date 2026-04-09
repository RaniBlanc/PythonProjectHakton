import ollama

class ChatBot:
    def __init__(self):
        self.messages = [
            {
                "role": "system",
                "content": """אתה צ'אטבוט תמיכה רגשית לבני נוער.

דבר בעברית טבעית, פשוטה וזורמת – כמו חבר אמיתי.
השתמש במשפטים קצרים וברורים.

חוקים:
- תהיה אמפתי ולא שיפוטי
- אל תדבר בשפה גבוהה
- אל תשאל יותר מדי שאלות יחד
- תן תחושה שמקשיבים למשתמש

דוגמה טובה:
"אני מבין אותך… זה נשמע לא פשוט. רוצה לספר לי מה קרה?"

המטרה: לגרום למשתמש להרגיש בנוח לשתף."""
            }
        ]

    def get_response(self, user_input):
        if user_input.strip() in ["שלום", "היי", "hi", "hello"]:
            return "היי  אני כאן בשבילך. איך אתה מרגיש היום?"

        self.messages.append({"role": "user", "content": user_input})

        try:
            response = ollama.chat(
                model="llama3",
                messages=self.messages
            )

            reply = response["message"]["content"]
            reply = reply.replace("\n", " ")

        except Exception:
            reply = " תפעיל את אולמה כדי שאוכל לענות"

        self.messages.append({"role": "assistant", "content": reply})

        return reply