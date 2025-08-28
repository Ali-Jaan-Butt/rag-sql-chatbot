def handle_logout():
    user_name = user_info.get('first_name', 'User')
    login_status = False
    user_info = {}
    return f"It's nice to have convo with you {user_name}... You've been logged out. Goodbye dear."