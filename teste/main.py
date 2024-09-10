from flask import render_template, redirect, url_for
from config import app
from models import *
from flask_login import login_user, logout_user, current_user, login_required

# criando uma página do site
# obs: toda página tem um route e uma função
# route (rota) -> é o caminho ou URL que leva a uma determinada página
# função -> o que você quer exibir naquela página

# decorator da função dashboard
# decorator = é uma linha de código que permite modificar o comportamento de uma função 

@app.route('/')  
def index():
    return render_template('index.html') # o que vai aparecer no dashboard


@app.route('/register', methods=['GET', 'POST'])
def register():
    from forms import RegisterForm
    from werkzeug.security import generate_password_hash
    from flask import flash

    formulario = RegisterForm()

    # verifica se os dados enviados são válidos
    if formulario.validate_on_submit(): # se foram válidos ele entra no if
        usuario = formulario.username.data 
        senha = generate_password_hash(formulario.password.data) 
        # o generate_password_hash() pega a senha informada pelo usuário e criptografa ela

        usuario_existe = User.query.filter_by(username=usuario).first() # verifica se o usuário existe

        # if user_exists == True:
        if usuario_existe:
            flash('Erro: O usuário já existe!', 'error')
        else:
            novo_usuario = User(username=usuario, password=senha)

            db.session.add(novo_usuario)
            db.session.commit()

            flash('Sucesso: O usuário foi criado!', 'success')

            return redirect(url_for('login'))

    return render_template('register.html', form=formulario)


@app.route('/login', methods=['GET', 'POST'])
def login():
    from forms import LoginForm
    from werkzeug.security import check_password_hash
    from flask import flash

    formulario = LoginForm()

    if formulario.validate_on_submit():
        usuario = formulario.username.data
        usuario_db = User.query.filter_by(username=usuario).first()

        if usuario_db:
            senha = formulario.password.data
            senha_db = usuario_db.password

            if check_password_hash(senha_db, senha):
                login_user(usuario_db)
                return redirect(url_for('dashboard'))
            else:
                flash('Senha incorreta', 'error')
        else:
            flash('Usuário não encontrado', 'error')

    return render_template('login.html', form=formulario)


# esse código desloga o usuário atual e o redireciona para a página de login
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/dashboard')
@login_required
def dashboard():
    todas_tarefas = Task.query.all() # pega todas as tarefas
    
    # pega as tarefas do usuário logado
    minhas_tarefas = Task.query.filter_by(user_id=current_user.id).all()

    return render_template('dashboard.html', todas_tarefas=todas_tarefas, minhas_tarefas=minhas_tarefas)


@app.route('/create_task', methods=['GET', 'POST'])
def create_task():
    from forms import TaskForm

    formulario = TaskForm()

    if formulario.validate_on_submit():
        nome_tarefa = formulario.task_name.data
        descricao = formulario.description.data
        status_tarefa = formulario.task_status.data

        tarefa_existe = Task.query.filter_by(task_name=nome_tarefa, user_id=current_user.id).first()
        # current_user.id -> usa o ID do usuário logado para associar a nova tarefa ao usuário

        if tarefa_existe:
            print('Erro: a tarefa já existe')
        else:
            nova_tarefa = Task(task_name=nome_tarefa, description=descricao, task_status=status_tarefa, user_id=current_user.id)

            db.session.add(nova_tarefa)
            db.session.commit()

            print('Sucesso: a tarefa foi criada')

            return redirect(url_for('dashboard'))

    return render_template('create_task.html', form=formulario)


@app.route('/edit_task/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    from forms import TaskForm
    
    # busca a tarefa no banco de dados pelo ID
    tarefa = Task.query.get_or_404(task_id)

    # cria o formulário e preenche com os dados da tarefa existente
    formulario = TaskForm(obj=tarefa)

    if formulario.validate_on_submit():
        # atualiza os dados da tarefa com os dados do formulário
        tarefa.task_name = formulario.task_name.data
        tarefa.description = formulario.description.data
        tarefa.task_status = formulario.task_status.data
        
        db.session.commit()
        
        print('Sucesso: a tarefa foi atualizada')

        return redirect(url_for('dashboard'))

    return render_template('edit_task.html', form=formulario, task=tarefa)


@app.route('/delete_task/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    # busca a tarefa no banco de dados pelo ID
    tarefa = Task.query.get_or_404(task_id)
    
    # exclui o evento
    db.session.delete(tarefa)
    db.session.commit()
    
    print('Sucesso: o evento foi excluído')

    return redirect(url_for('dashboard'))


# colocando o site no ar
if __name__ == "__main__":
    app.run(debug=True) # com o debug=True todas as alterações que fizermos no nosso código, serão 
    # automaticamente exibidas no nosso site, para não precisar ficar parando o código e executando de novo
