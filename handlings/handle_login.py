from database import verify_credentials
from translation import translate_from_eng


def handle_login_attempt(message, user_lang, pending_login):
    try:
        email, password = message.split()[0], message.split()[1]
        is_valid, user_info_out = verify_credentials.verify_credentials(email, password)
        if is_valid:
            global login_status, user_info
            login_status = True
            pending_login["active"] = False
            user_info = user_info_out
            return translate_from_eng.translate_from_english(f"✅ Login successful! Welcome back, {user_info['first_name']}.", user_lang)
        else:
            return translate_from_eng.translate_from_english("❌ Invalid credentials. Please try again.", user_lang)
    except:
        return translate_from_eng.translate_from_english("⚠️ Please provide login in format:\n**email@example.com password123**", user_lang)