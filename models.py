from sqlalchemy import (
    create_engine, Column, Integer, String, DateTime, ForeignKey, select, Date)
from sqlalchemy.sql import func
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import (
    relationship, declarative_base, sessionmaker, scoped_session, DeclarativeBase)

# create an engine to connect to the database
engine = create_engine('sqlite:///saep_db.sqlite3', echo=False)

# create a base class for declarative class definitions
#Base = declarative_base()
class Base(DeclarativeBase):
    pass

# create a scoped session to manage database sessions
db_session = scoped_session(sessionmaker(bind=engine))


# define the User model
class Usuario(Base, UserMixin):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    senha_hash = Column(String(255), nullable=False)
    criado_em = Column(DateTime(timezone=True), server_default=func.now())
    # ---------------------
    # Senha
    # ---------------------

    def set_password(self, password):
        self.senha_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.senha_hash, password)