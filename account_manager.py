import sqlite3
import re

from util import extract_unique_code


def add_balance(user_id, unique_code):
    with sqlite3.connect("database.db") as db:

        cursor = db.cursor()

        if str(user_id) == str(unique_code):  # If user trying to follow own referral link
            values = [True, user_id]
            cursor.execute(f"UPDATE users SET already_referral = ? WHERE user_id = ?",
                           values)  # makes user already referral cuz he got registered
            return False

        cursor.execute(f"SELECT user_id FROM users WHERE user_id = ?", [user_id])  # checking if user registered
        if cursor.fetchone() is not None:
            cursor.execute(f"SELECT already_referral FROM users WHERE user_id = ?", [user_id])
            # checking if he referral
            result = re.findall(r"[0-9]", str(cursor.fetchone()))
            if result == ['1']:
                return False  # user already referral
            else:
                values = [True, user_id]
                cursor.execute(f"UPDATE users SET already_referral = ? WHERE user_id = ?", values)
                values = [1, unique_code]
                cursor.execute(f"UPDATE users SET balance = balance + ? WHERE user_id = ?", values)  # updating balance
                db.commit()
                return True
        else:
            return False


def remove_balance(user_id, count):
    with sqlite3.connect("database.db") as db:

        cursor = db.cursor()

        cursor.execute(f"SELECT user_id FROM users WHERE user_id = ?", [user_id])
        if cursor.fetchone() is not None:
            values = [count, user_id]
            cursor.execute(f"UPDATE users SET balance = balance - ? WHERE user_id = ?", values)
            db.commit()
            return True  # removing to balance
        else:
            return False


def get_balance(user_id):
    with sqlite3.connect("database.db") as db:

        cursor = db.cursor()
        cursor.execute(f"SELECT user_id FROM users WHERE user_id = ?", [user_id])
        if cursor.fetchone() is not None:
            cursor.execute(f"SELECT balance FROM users WHERE user_id = ?", [user_id])
            result = re.findall(r"[0-9]", str(cursor.fetchone()))
            return ''.join(result)
        else:
            return False


def register(user_id, username, message):
    with sqlite3.connect("database.db") as db:
        cursor = db.cursor()

        cursor.execute('CREATE TABLE IF NOT EXISTS users(user_id VARCHAR, user_name VARCHAR, balance INTEGER, '
                       'already_referral BOOLEAN)')

        db.commit()

        cursor.execute(f"SELECT user_id FROM users WHERE user_id = ?", [user_id])
        if cursor.fetchone() is None:
            values = [user_id, username, 0, False]
            cursor.execute(f"INSERT INTO users(user_id, user_name, balance, already_referral) VALUES(?, ?, ?, ?)",
                           values)

            if extract_unique_code(message.text) is None:  # Checking for unique code
                values = [True, user_id]
                cursor.execute(f"UPDATE users SET already_referral = ? WHERE user_id = ?", values)
                # makes user already referral

            db.commit()
            return True
        else:
            return False


def admin_update(user_id):  # Delete (function for updating balance by 10)
    with sqlite3.connect("database.db") as db:

        cursor = db.cursor()

        cursor.execute(f"SELECT user_id FROM users WHERE user_id = ?", [user_id])
        if cursor.fetchone() is not None:
            values = [10, user_id]
            cursor.execute(f"UPDATE users SET balance = balance + ? WHERE user_id = ?", values)
            db.commit()
            return True
        else:
            return False
