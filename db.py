import psycopg2



db_config = 'postgres://zxahtzhj:fHjZ2nedJAwebEknKUSiNDxb1y445bPJ@suleiman.db.elephantsql.com/zxahtzhj'

def init_db():  
    connection = psycopg2.connect('postgres://zxahtzhj:fHjZ2nedJAwebEknKUSiNDxb1y445bPJ@suleiman.db.elephantsql.com/zxahtzhj')

    cursor = connection.cursor()

    create_table_query = """
    CREATE TABLE IF NOT EXISTS artist (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        dob DATE,
        gender VARCHAR(10),
        address VARCHAR(255),
        first_release_year INT,
        no_of_albums_released INT,
        created_at TIMESTAMPTZ DEFAULT NOW(),
        updated_at TIMESTAMPTZ DEFAULT NOW()
    );
    """
    cursor.execute(create_table_query)

    connection.commit()
    cursor.close()
    connection.close()

