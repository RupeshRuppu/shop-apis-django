def get_username_else_email(user):
    return user.username if user.username else user.email
