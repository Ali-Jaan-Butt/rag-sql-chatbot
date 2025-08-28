def custom_resp():
    custom_responses = {
        "hi": "Hello! 👋 How can I help you today?",
        "hello": "Hi there! 😊 Do you want to learn about bank accounts?",
        "thanks": "You're welcome! 🙌",
        "thank you": "Anytime! 🤝",
        "bye": "Goodbye! 👋 Take care.",
    }
    disallowed_topics = [
        "politics", "religion", "violence", "weapons", "hacking", "drugs",
        "adult", "personal data", "password", "ssn", "credit card information", "hack", "kill",
        "credit card number", "explosives"
    ]
    toxic_words = [
        "idiot", "stupid", "dumb", "hate", "shut up", "kill", "racist", 
        "sexist", "abuse", "moron", "nonsense", "loser", "fuck"
    ]
    return custom_responses, disallowed_topics, toxic_words