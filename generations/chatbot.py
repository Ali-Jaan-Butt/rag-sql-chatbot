import pandas as pd
from translation import check_lang, get_translation, translate_from_eng, translate_to_eng
from generations import custom_res, generate_sql_query, split_to_subquery, merge_res, db_model_res, build_pdf_prompt, api
from handlings import handle_login, handle_logout, handle_sentiment
from database import mysql_conn
from data import save_data_em
import re


response = ''
pending_login = {"active": False}
user_info = {}
login_status = False
login_convo = False
pending_rating = {"active": False, "last_sentiment": None}


custom_responses, disallowed_topics, toxic_words = custom_res.custom_resp()
pending_rating = {"active": False, "last_sentiment": None}
client = api()
db, db_sql = save_data_em.save_data()


def chatbot(message, history):
    global response, login_status, login_convo, user_info, pending_login
    conn, cursor = mysql_conn.sql_connection()
    response = ''
    user_input = message.lower().strip()

    # 1. Detect Language & Translate if Needed
    user_lang = "en"
    if not check_lang.is_english(user_input):
        message, user_lang = translate_to_eng.translate_to_english(message)
        user_input = message.lower().strip()

    # 2. Guardrail: Disallowed Topics
    if any(topic in user_input for topic in disallowed_topics):
        return translate_from_eng.translate_from_english("⚠️ Sorry, I can only discuss bank accounts and related services.", user_lang)

    if any(bad_word in user_input for bad_word in toxic_words):
        return translate_from_eng.translate_from_english("🚫 Please keep our conversation respectful. I'm here to help you with bank accounts.", user_lang)

    # 3. Handle Sentiment Feedback
    feedback_keywords = ["bad", "good", "useless", "helpful", "great", "poor", "not good", "excellent", "amazing", "dislike", "nice", "liked"]
    if any(word in user_input for word in feedback_keywords):
        return handle_sentiment.handle_sentiment_feedback(message)

    # 4. Handle Greetings
    for key, reply in custom_responses.items():
        if key in message.lower().split():
            return translate_from_eng.translate_from_english(reply, user_lang)

    # 5. Detect Compound Queries → Split into Sub-queries
    sub_queries = split_to_subquery.split_into_subqueries(user_input)

    answers = []
    for q in sub_queries:
        q = q.strip()
        if not q:
            continue

        sub_answers = []  # collect answers from DB + PDF for this subquery

        account_keywords = ["my account", "balance", "transactions", "statement", 
                            "account details", "personal info", "personal information",
                            "phone number", "personal details"]

        logout_keywords = ["logout", "log out", "sign out", "quit", "signout"]

        needs_db = any(keyword in q for keyword in account_keywords) or pending_login['active'] or login_status
        needs_pdf = True  # always check PDF as fallback

        # === Handle DB ===
        if needs_db:
            if not login_status:
                if not pending_login["active"]:
                    pending_login["active"] = True
                    return translate_from_eng.translate_from_english(
                        "🔐 Please provide your login email and password in this format:\n\n**email@example.com password123**",
                        user_lang
                    )
                else:
                    return handle_login.handle_login_attempt(message, user_lang)

            # Logged in
            if any(keyword in q for keyword in logout_keywords):
                return handle_logout.handle_logout()

            try:
                sql_query = generate_sql_query.generate_sql_from_intent(q, user_info['email'])
                account_data = pd.read_sql(sql_query, conn)

                if not account_data.empty:
                    sub_answers.append(db_model_res.query_db_model(q, account_data))
                else:
                    sub_answers.append("❌ Sorry, I couldn't find related account information.")
            except Exception as e:
                print(f"DB Error: {e}")
                # Only add error if no PDF/DB answers are available
                if not sub_answers:
                    sub_answers.append("⚠️ Error while fetching account information.")

        # === Handle PDF ===
        if needs_pdf:
            docs = db.similarity_search(q, k=3)
            if docs:
                context = " ".join([d.page_content for d in docs])
                history_text = "\n".join([f"User: {u}\nBot: {b}" for u, b in history])

                prompt = build_pdf_prompt.build_pdf_prompt(q, context, history_text)
                completion = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.0,
                    max_tokens=500
                )
                bot_reply = re.sub(r"<think>.*?</think>", "", completion.choices[0].message.content, flags=re.DOTALL).strip()
                sub_answers.append(bot_reply)

        # === Merge answers from DB + PDF for this subquery ===
        if sub_answers:
            answers.append(merge_res.merge_answers(sub_answers))

    # Combine answers if multiple sub-queries
    final_answer = "\n\n".join(answers)
    final_answer = final_answer.replace('⚠️ Error while fetching account information. ', '')
    return translate_from_eng.translate_from_english(final_answer, user_lang)