import os ,time
from jogoteca import *
from flask_wtf import FlaskForm
from wtforms import StringField,validators, SubmitField, PasswordField

class FormularioJogo(FlaskForm):
    nome = StringField('Nome do jogo', [validators.DataRequired(),validators.Length(min=1, max=50)])
    categoria= StringField('Categoria', [validators.DataRequired(),validators.Length(min=1, max=40)])
    console = StringField('Console', [validators.DataRequired(),validators.Length(min=1, max=20)])
    salvar = SubmitField('Salvar')

class FormularioUsuario(FlaskForm):
    nickname = StringField('Nickname', [validators.DataRequired(),validators.Length(min=1, max=8)])
    senha= PasswordField('Senha', [validators.DataRequired(),validators.Length(min=1, max=100)])
    login = SubmitField('Login')


def recupera_imagem(id):
    for nome_arquivo in os.listdir(f'uploads/'):
        if f'capa{id}-' in nome_arquivo:
            return nome_arquivo
    return 'capa_padrao.jpg'
        

def salvar_imagem(request,  id):

    if request.filename != 'capa_padrao.jpg' and request.filename !=  None and request.filename != '':
        deleta_arquivo(id)
        timestamp =time.time()
        request.save(f'uploads/capa{id}-{timestamp}.jpg')


def deleta_arquivo(id):
    arquivo  = recupera_imagem(id)
    if arquivo != 'capa_padrao.jpg':
        os.remove(f'uploads/{arquivo}')
