from flask import render_template, request, redirect, session, flash, url_for
from jogoteca import app
from Modelos.Usuarios import Usuarios
from helpers import FormularioUsuario
from flask_bcrypt import check_password_hash

@app.route('/login')
def login():
    query_request =  request.args.get('next')
    form  = FormularioUsuario()
    return render_template('login.html', next = query_request, form = form)


@app.route('/autenticar', methods=['POST',])
def autenticar():

    form  =  FormularioUsuario(request.form)
    usuario = Usuarios.query.filter_by(nickname = form.nickname.data).first()
    senha = check_password_hash(usuario.senha, form.senha.data)
    
    if usuario  and senha:
        flash(f'{usuario.nome} logado com sucesso.')
        session['usuario_logado'] = form.nickname.data
        return redirect(request.form['next'])

    flash(f'Não foi possivel o usuario {form.nickname.data} logar com sucesso.')
    return redirect(url_for('login', next = request.form['next']))


@app.route('/logout')
def logout():
    flash(f'Usuario {session['usuario_logado']} Deslogado com sucesso')
    session['usuario_logado'] = None 
    return redirect(url_for('index'))