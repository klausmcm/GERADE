import itertools
import string
import sqlite3

DB_NAME = "db.sqlite3"

def generate_id_db( barcode_specs ):
    connection = sqlite3.connect( DB_NAME )
    cursor     = connection.cursor()

    try:
        cursor.execute( "DROP TABLE entries" )
    except Exception:
        pass
    cursor.execute( "CREATE TABLE entries (id_constant, id_variable, is_used)" )

    keywords = itertools.product( string.ascii_lowercase + string.digits, repeat=4 )
    for i in keywords:
        combo = "".join( list( i ) ) 
        cursor.execute( "INSERT INTO entries VALUES (?, ?, ?)", ( barcode_specs[ "prefix" ], combo, 0, ) )

    connection.commit()
    connection.close()
    return

def deactivate_entry( id_variable ):
    connection = sqlite3.connect( DB_NAME )
    cursor     = connection.cursor()

    cursor.execute( "UPDATE entries SET is_used=1 WHERE id_variable=?", ( id_variable, ) )
    connection.commit()
    connection.close()
    return

def get_next_available_id():
    connection = sqlite3.connect( DB_NAME )
    connection.row_factory = sqlite3.Row
    cursor     = connection.cursor()

    cursor.execute( "SELECT * FROM entries WHERE is_used=?", ( 0, ) )
    entry = cursor.fetchone()
    return entry

