from models import db_session,Usuario, Proprietario

usuarios = [
    {"nome": "admin", "email": "adm@email.com"},
    {"nome": "João Silva", "email": "joao.silva@email.com"},
    {"nome": "Maria Oliveira", "email": "maria.oliveira@email.com"},
    {"nome": "Pedro Santos", "email": "pedro.santos@email.com"}
]
proprietarios = [

    {"nome": "Gabriel Martins", "email": "gabriel.martins@email.com",
     "telefone": "11900000001", "cpf": "123.456.789-09"},
    {"nome": "Juliana Almeida", "email": "juliana.almeida@email.com",
     "telefone": "11900000002", "cpf": "390.533.447-05"},
    {"nome": "Rafael Rodrigues", "email": "rafael.rodrigues@email.com",
     "telefone": "11900000003", "cpf": "935.411.347-80"},
    {"nome": "Felipe Nascimento", "email": "felipe.nascimento@email.com",
     "telefone": "11900000005", "cpf": "168.995.350-09"},
    {"nome": "João M. O. Andrade", "email": "jm.andrade@email.com",
     "telefone": "11900000009", "cpf": "987.654.321-00"},
    {"nome": "Camila Barbosa", "email": "camila.barbosa@email.com",
     "telefone": "11900000004", "cpf": "111.444.777-35" },
    {"nome": "Ana Barbosa", "email": "ana.barbosa@email.com",
     "telefone": "11900000004", "cpf": "529.982.247-25" }

]
"""

    
    
    """


def criar_usuarios():
    for p in usuarios:
        admin = Usuario(
            name=p['nome'],
            email=p['email']
        )
        admin.set_password("@123")

        db_session.add(admin)
        db_session.commit()
        print("criado com sucesso!!!")

def criar_proprietarios():
    for p in proprietarios:
        pro_ = Proprietario(
            nome=p['nome'],
            email= p['email'],
            telefone=p['telefone']
        )
        print(pro_.nome, pro_.email, pro_.telefone, p['cpf'])
        pro_.set_cpf(p['cpf'])
        #print(pro_.nome, pro_.email, pro_.telefone)

        db_session.add(pro_)
        db_session.commit()
        print("criado com sucesso!!!")

criar_proprietarios()
criar_usuarios()