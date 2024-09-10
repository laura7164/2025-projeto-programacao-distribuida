from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length

# criamos uma classe RegisterForm que será usada para criar um formulário de registro de usuário
class RegisterForm(FlaskForm):
    # criando os campos do formulário
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=25)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Registrar')

# criamos uma classe LoginForm que será usada para criar um formulário de login de usuário
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

# criamos uma classe TaskForm que será usada para criar um formulário de tarefa, onde 
# a pessoa vai adicionar informações sobre a tarefa
class TaskForm(FlaskForm):
    task_name = StringField('Nome da tarefa', validators=[DataRequired()])
    description = TextAreaField('Descrição', validators=[DataRequired()])
    # SelectField -> para que o usuário possa selecionar opções
    task_status = SelectField('Status da tarefa', 
                              choices=[('pendente', 'Pendente'), 
                                       ('em andamento', 'Em andamento'), 
                                       ('concluida', 'Concluída')], 
                              validators=[DataRequired()])
    submit = SubmitField('Criar tarefa')
