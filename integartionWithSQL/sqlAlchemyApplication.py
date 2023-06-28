import sqlalchemy
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy import inspect
from sqlalchemy import Column 
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey


Base = declarative_base()


class User(Base):
    __tablename__ = "user_account"
   
    # atributos
    id = Column(Integer, primary_key= True )
    name = Column(String)
    fullname = Column(String)


    address = relationship(
        "Address", back_populates= "user" , cascade= "all, delete-orphan"
    )

    def __repr__(self):
        return f"User(id= {self.id}, name = {self.name}, fullname = {self.fullname})"


class Address(Base):
    __tablename__ = "address"

    # atributos

    id = Column(Integer, primary_key = True)
    email_address = Column(String(30), nullable = False )
    user_id = Column(Integer, ForeignKey("user_account.id"), nullable=False)


    user = relationship(
        "user" , back_populates="address" 
    )

    def __repr__(self):
        return f"Address (id = {self.id}, email = {self.email_address})"
    



print(User.__tablename__)
print(Address.__tablename__)


#conexão com o banco de dados
engine = create_engine("sqlite://")


#Criando as Classes com tabelas no banco de dados 
Base.metadata.create_all(engine)

#depreciado - será removido em um futuro release 
inspetor_engine = inspect(engine)

print(inspetor_engine.has_table("user_account"))

#get_table_names seria um metodo para puxar o das tabelas que no caso seria address e user 
print(inspetor_engine.get_table_names())









