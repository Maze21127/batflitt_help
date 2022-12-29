import sqlite3
from dataclasses import dataclass

from loguru import logger


import os


@dataclass
class User:
    tg_id: int
    language: str


class Language:
    def __init__(self):
        self.users = {}
        self.db = Database()
        self.update_users()

    def update_users(self):
        data = self.db.get_all_users()
        for i in data:
            self.users[i[0]] = i[1]

    def update_user(self, tg_id: int, language: str):
        self.db.update_user(User(tg_id=tg_id, language=language))
        self.users[tg_id] = language
        return language

    def get_user_language(self, tg_id: int):
        return self.users.get(tg_id, 'en')

    def add_user(self, tg_id: int, language: str):
        self.db.add_user(User(tg_id=tg_id, language=language))
        self.users[tg_id] = language
        return language


class Statistics:
    def __init__(self):
        self.users = {}
        self.db = Database()

    def get_scores(self, chat_id: int):
        return self.db.get_stats_by_chat(chat_id)

    def add_score(self, user_id: int, chat_id: int, score: int = None):
        self.db.add_score(user_id, chat_id, score if score else 0)


class Database:
    def __init__(self):
        logger.add("logs/error.log", format="{time} {level} {message}", level="ERROR", rotation="01:00")
        logger.add("logs/info.log", format="{time} {level} {message}", level="INFO", rotation="01:00")
        self.connection = None
        self.cursor = None
        self.db_name = 'app.db'
        self.create_tables()
        self.check_connection()

    def create_tables(self):
        if os.path.exists(self.db_name):
            return
        self.check_connection()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS users("
                            "id integer PRIMARY KEY,"
                            "tg_id bigint NOT NULL UNIQUE,"
                            "language varchar(5) NOT NULL)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS stats("
                            "id integer PRIMARY KEY,"
                            "user_id bigint NOT NULL,"
                            "support_chat_id bigint NOT NULL,"
                            "score integer)")
        self.connection.commit()
        logger.info("Таблицы созданы")

    def add_user(self, user: User):
        self.check_connection()
        try:
            self.cursor.execute(
                f"INSERT INTO users (tg_id, language) VALUES (?, ?);", (user.tg_id, user.language)
            )
            self.connection.commit()
            logger.info(f"{user} added")
        except sqlite3.IntegrityError:
            return

    def add_score(self, user_id, chat_id: int, score: int):
        self.check_connection()
        try:
            self.cursor.execute(
                f"INSERT INTO stats (user_id, support_chat_id, score) VALUES (?, ?, ?);", (user_id, chat_id, score)
            )
            self.connection.commit()
            logger.info(f"{user_id} оценил работу {chat_id} в {score}")
        except sqlite3.IntegrityError:
            return

    def get_stats_by_chat(self, chat_id: int):
        self.check_connection()
        self.cursor.execute(f"SELECT score from stats WHERE support_chat_id = ?;", (chat_id, ))
        data = self.cursor.fetchall()
        return data

    def get_all_users(self):
        self.check_connection()
        self.cursor.execute(f"SELECT tg_id, language FROM users;")
        data = self.cursor.fetchall()
        return data

    def update_user(self, user: User):
        self.check_connection()
        self.cursor.execute(f"UPDATE users SET language = ? WHERE tg_id = ?;", (user.language, user.tg_id))
        self.connection.commit()

    def check_connection(self):
        if any((self.connection is None, self.cursor is None)):
            try:
                self.connection = sqlite3.connect(self.db_name)
                self.cursor = self.connection.cursor()
            except sqlite3.Error as e:
                logger.error(e)
