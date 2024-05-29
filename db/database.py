from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
load_dotenv()

Database_Host = os.environ.get("DB_HOST")
Database_port = os.environ.get("DB_PORT")
Database_user = os.environ.get("DB_USER")
Database_name = os.environ.get("DATA_NAME", "data_table")
Database_pass = os.environ.get("DB_PASSPHRASE", "Passphrase")

DATABASE_URL = f"postgresql+psycopg2://{Database_user}:{Database_pass}@{Database_Host}:{Database_port}/{Database_name}"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
