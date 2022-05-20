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
                time_score  TEXT, 
                score INTEGER
            )
        """)
        self.CONN.commit()

    @classmethod
    def init(cls) -> object:
        """
        calls init method
        :return: object DatabaseManager
        """
        return cls()

    @classmethod
    def tear_down(cls) -> None:
        """
        Closes database connection
        :return:
        """
        cls.CONN.close()
        print("db connection closed successfully")

    @staticmethod
    def add_high_score(name: str, score: str, time_score: str, conn=CONN, cursor=CURSOR) -> None:
        """
        Adds the high score to the database
        :param name: str of person name
        :param score: str person score
        :param time_score: str time score
        :param conn: sqlite connection
        :param cursor: sqlite cursor
        :return:
        """
        name = ''.join(e for e in name if e.isalnum())
        string = f"""
            INSERT INTO high_scores (id, name, time_score, score) 
            VALUES 
                (null, "{name}", "{time_score}", {score})
        """
        cursor.execute(string)
        conn.commit()

    @staticmethod
    def get_scores(cursor=CURSOR) -> list:
        """
        Queries database for top 5 scores in descending order
        :param cursor: sqlite3 cursor
        :return: list of tuples
        """
        string = """
            SELECT name, score, time_score from high_scores
            ORDER BY score DESC
            LIMIT 5;
        """
        cursor.execute(string)
        result = cursor.fetchall()
        return result


atexit.register(DatabaseManager.tear_down)
