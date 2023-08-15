import sqlite3
import click
from flask import current_app, g
# g is a special object that is unique for each request. 
#it is used to store data that might be accessed by multiple functions during the request. 
#connection is stored and reused instead of creating new connection if get_db is called a second time in the same request



def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            #current_app is special object that points to the flask application
            # handling the request. Since i used an application factory, there is no applicaiton object when writing the reso of your code.
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row # tells the connection to return rows that behave like dicts. This allows accessing the columns by name. 
    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        # open resource opens a file relative to the flaskr package

        db.executescript(f.read().decode('utf8'))

#defines a command line command called init-db that calls the init_db function and show susccess message to the user
@click.command('init-db')
def init_db_command():
    '''clear the existing data and create new tables'''
    init_db()
    click.echo('initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    # tell flask to call that function when cleaning up after returning the response.
    app.cli.add_command(init_db_command)
    # adds a new command that can be called with the flask command.
    