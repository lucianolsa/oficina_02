from models import Usuario, db_session

usuario = Usuario(
    name="João",
    email="j@email.com"
)

usuario.set_password("@123")

usuario.set_cpf("12345678909")

db_session.add(usuario)
db_session.commit()