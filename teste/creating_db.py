from config import app, db

# código para criar o banco de dados
# precisa de um contexto
with app.app_context():
    db.create_all() # cria as tabelas no banco de dados se elas não existirem
