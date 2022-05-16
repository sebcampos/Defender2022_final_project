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
    def init(cls):
        return cls()

    @classmethod
    def tear_down(cls):
        cls.CONN.close()
        print("db connection closed successfully")

    @staticmethod
    def add_high_score(name: str, score: str, time_score: str, conn=CONN, cursor=CURSOR) -> None:
        name = ''.join(e for e in name if e.isalnum())
        string = f"""
            INSERT INTO high_scores (id, name, time_score, score) 
            VALUES 
                (null, "{name}", "{time_score}", {score})
        """
        cursor.execute(string)
        conn.commit()

    @staticmethod
    def get_scores(cursor=CURSOR) -> str:
        string = """
            SELECT name, score, time_score from high_scores
            ORDER BY score DESC
            LIMIT 10;
        """
        cursor.execute(string)
        result = cursor.fetchall()
        max_length = 0
        for tup in result:
            for val in tup:
                length = len(str(val))
                if length > max_length:
                    max_length = length
        final_string = "_"*max_length*3+"\n|"
        row_length = len(final_string)
        for column in ["Name", "Score", "Time"]:
            spacer = row_length - len(column)
            final_string += column+(" "*spacer)+"|"
        final_string += "\n"+"-"*max_length*3+"\n"
        for tup in result:
            mini_string = "|"
            for val in tup:
                val_str = str(val)
                spacer = row_length - len(val_str) - 2
                print(max_length)
                print(len(val_str), spacer)
                mini_string += val_str+(" "*spacer)+"|"
                print(len(mini_string))
            final_string += mini_string+"\n"+"_"*max_length*3+"\n"

        return final_string


atexit.register(DatabaseManager.tear_down)
