from models import db_session,Usuario
def criar_usuario():
    admin = Usuario(
        name='luciano',
        email="lsa@email.com"
    )
    admin.set_password("@123")

    db_session.add(admin)
    db_session.commit()
    print("Usuario criado com sucesso!!!")

criar_usuario()