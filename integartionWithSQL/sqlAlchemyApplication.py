import sqlalchemy
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy import select
from sqlalchemy import inspect
from sqlalchemy import Column 
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey


Base = declarative_base()


class User(Base):
    __tablename__ = "user_account"
   
    # atributos
    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)

    address = relationship(
        "Address", back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"User(id = {self.id}, name = {self.name}, fullname = {self.fullname})"


class Address(Base):
    __tablename__ = "address"

    # atributos
    id = Column(Integer, primary_key=True)
    email_address = Column(String(30), nullable=False)
    user_id = Column(Integer, ForeignKey("user_account.id"), nullable=False)

    user = relationship("User", back_populates="address")

    def __repr__(self):
        return f"Address(id = {self.id}, email_address = {self.email_address})"


print(User.__tablename__)
print(Address.__tablename__)

# conexão com o banco de dados
engine = create_engine("sqlite://")

# Criando as Classes com tabelas no banco de dados 
Base.metadata.create_all(engine)

# Investiga o esquema de banco de dados 
inspector = inspect(engine)
print(inspector.has_table("user_account"))
print(inspector.get_table_names())
print(inspector.default_schema_name)

# Criando a sessão
Session = sessionmaker(bind=engine)
session = Session()

# Estabelecendo valores para as tabelas, como os usuários
leonardo = User(
    name='leonardo',
    fullname='Leonardo Gabriel Barbosa de Melo',
    address=[Address(email_address='leonardo@email.com')]
)

sandy = User(
    name='sandy',
    fullname='Sandy da Silva Sauro Simpsons',
    address=[Address(email_address='sandybartsimpsons@email.com') ,
             Address(email_address='sandysimpsons@email.com')]

)

patrick = User(
    name='patrick',
    fullname='Patrick da Silva'
)

# Enviando para o banco de dados (persistência de dados)
session.add_all([leonardo, sandy, patrick])

session.commit()

#Mostra onde esta Leonardo no banco de dados
#filtragem em cima dos dados 
stmt_user = select(User).where(User.name.in_(['leonardo', 'sandy']))
print('Recuperando usuários a partir de condição de filtragem')
for user in session.scalars(stmt_user):
    print(user)

stmt_address = select(Address).where(Address.user_id.in_([2]))
print('\nRecuperando os endereços de email de sandy')
for address in session.scalars(stmt_address):
    print(address)