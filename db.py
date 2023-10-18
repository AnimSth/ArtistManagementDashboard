import psycopg2



db_config = 'postgres://zxahtzhj:fHjZ2nedJAwebEknKUSiNDxb1y445bPJ@suleiman.db.elephantsql.com/zxahtzhj'

def init_db():  
    connection = psycopg2.connect('postgres://zxahtzhj:fHjZ2nedJAwebEknKUSiNDxb1y445bPJ@suleiman.db.elephantsql.com/zxahtzhj')

    cursor = connection.cursor()

    create_table_query = """
        CREATE TABLE IF NOT EXISTS music (
            artist_id INT,
            title VARCHAR(255) NOT NULL,
            album_name VARCHAR(255),
            genre VARCHAR(10),
            created_at TIMESTAMPTZ DEFAULT NOW(),
            updated_at TIMESTAMPTZ DEFAULT NOW(),
            FOREIGN KEY (artist_id) REFERENCES artist(id)
        );

    """
    cursor.execute(create_table_query)

    connection.commit()
    cursor.close()
    connection.close()

