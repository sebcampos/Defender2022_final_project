from sqlite3 import connect
import atexit


class DatabaseManager:
    CONN = connect("HighScores.db")
    CURSOR = CONN.cursor()

    def __init__(self):
        self.CURSOR.execute("""
            CREATE TABLE IF NOT EXISTS high_scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                name TEXT, 
                score INTEGER
            )
        """)
        self.CONN.commit()

    @classmethod
    def init(cls):
        return cls()

    @classmethod
    def tear_down(cls):
        cls.CONN.close()
        print("db connection closed successfully")

    @staticmethod
    def add_high_score(name: str, score: str, conn=CONN, cursor=CURSOR) -> None:
        string = f"INSERT INTO high_scores (null, {name}, {score})"
        cursor.execute(string)
        conn.commit()

    @staticmethod
    def find_highest_score(conn=CONN, cursor=CURSOR) -> tuple:
        string = ""  # TODO replace empty string with sql statement to select highest score in table
                     # TODO execute sql statment with cursor
                     # TODO save result of statment into a variable by calling cursor.fetchall()
                     # TODO commit action with conn
                     # TODO return result


atexit.register(DatabaseManager.tear_down)
