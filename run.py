from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from logsite import APP as application, db

def create_schema():
    engine = create_engine(application.config['SQLALCHEMY_DATABASE_URI'])
    if not database_exists(engine.url):
        create_database(engine.url)
    engine.dispose()

create_schema()
db.db.create_all()

if __name__ == '__main__':
    application.run(host='0.0.0.0', debug=True)
