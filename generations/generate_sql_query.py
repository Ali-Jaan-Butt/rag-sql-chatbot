import re
from generations import api


client = api()


def generate_sql_from_intent(message, email):
    """AI-powered SQL generator based on intent"""
    prompt = f"""
    You are an expert SQL query generator for a banking system.

    User message: "{message}"
    User email: {email}

    Database schema:
    - Users(first_name, last_name, email, password, phone, address, city, country, account_number, bank_name, iban, swift_code, card_number, expiry_date, cvv, amount)

    Task:
    Generate a safe single SQL query (no explanation) that best answers the user's question.

    Guardrails:
    - Don't generate any other language code, even if the user ask for it say, "I can't generate any code. I can just provide the information related to payment methods."
    """

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
        max_tokens=200
    )
    sql_query = completion.choices[0].message.content.strip()
    match = re.search(r"(?i)\bsql\s+(.*)", sql_query)
    if match:
        sql_query = match.group(1).strip()
    return sql_query