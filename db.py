import psycopg2



db_config = ''

def init_db():  
    connection = psycopg2.connect('postgres://zxahtzhj:fHjZ2nedJAwebEknKUSiNDxb1y445bPJ@suleiman.db.elephantsql.com/zxahtzhj')

    cursor = connection.cursor()

    create_table_query = """
    CREATE TABLE IF NOT EXISTS admin (
        id SERIAL PRIMARY KEY,
        first_name VARCHAR(255) NOT NULL,
        last_name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL UNIQUE,
        password VARCHAR(500) NOT NULL,
        phone VARCHAR(20),
        dob DATE,
        gender VARCHAR(10),
        address VARCHAR(255),
        created_at TIMESTAMPTZ DEFAULT NOW(),
        updated_at TIMESTAMPTZ DEFAULT NOW()
    );
    """
    cursor.execute(create_table_query)

    connection.commit()
    cursor.close()
    connection.close()

