from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
#SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# db=_mysql.connect("207.154.236.252","root","winkerdev630",)
SQLALCHEMY_DATABASE_URL = "mysql://root:winkerdev630@207.154.236.252/devdb"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()
