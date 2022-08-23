def is_subscribed(chat_id, user_id, bot, status):  # checking if user subscribing
    if bot.get_chat_member(chat_id, user_id).status in status:
        return True
    else:
        return False


def extract_unique_code(text):
    # Extracts the unique_code from the sent /start command.
    return text.split()[1] if len(text.split()) > 1 else None
