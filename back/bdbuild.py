import sqlite3

def create_bd():
    con = sqlite3.connect("sql.db")

    cur = con.cursor()

    cur.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                users_id    VARCHAR(31) PRIMARY KEY,
                senha       VARCHAR(40) NOT NULL
            );
            """
        )
    
    cur.execute(
            """ 
            CREATE TABLE IF NOT EXISTS posts (
                post_id     SERIAL PRIMARY KEY,
                users       VARCHAR(31),
                post        TEXT,

                FOREIGN KEY (users) REFERENCES users(users_id)
            );
            """
        )

    cur.execute(
            """
            CREATE TABLE IF NOT EXISTS interaction (
                post        INT,
                users       VARCHAR(31),
                like        BOOL, 

                PRIMARY KEY (post, users),
                FOREIGN KEY (users) REFERENCES users(users_id),
                FOREIGN KEY (post)  REFERENCES posts(post_id)
            );
            """
        )

    con.commit()


