def merge_answers(answers):
    """Combine DB + PDF answers into one smooth message."""
    if len(answers) == 1:
        return answers[0]
    elif len(answers) > 1:
        return " ".join(answers)
    return "❌ Sorry, I don’t have the information you need."