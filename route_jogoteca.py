from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from jogoteca import app,db
from Modelos.Jogo import Jogos
from helpers import FormularioJogo, salvar_imagem, recupera_imagem

# Index tela inicial home
@app.route('/')
def index():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
          return redirect(url_for('login', next = url_for('index')))
    
    jogos = Jogos.query.order_by(Jogos.id)
    lista =[]

    for jogo in jogos:
        lista.append(
            {
                "id": jogo.id,
                "nome": jogo.nome,
                "categoria": jogo.categoria,
                "console": jogo.console,
                "capa": recupera_imagem(jogo.id)
            }
           
        )
    return render_template('lista.html', title = 'Jogos', lista = lista )


# Rotas pra cadastro de um novo jogo
@app.route('/new')
def novo_jogo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', next = url_for('novo_jogo')))
    form = FormularioJogo()
    return render_template('novo.html', title = 'Novo Jogo', form = form)

@app.route('/create', methods=['POST',])
def criar():

    form  =  FormularioJogo(request.form)

    if not form.validate_on_submit():
        return redirect(url_for('novo_jogo'))
    
    nome = form.nome.data
    categoria = form.categoria.data
    console = form.console.data

    jogo = Jogos.query.filter_by(nome=nome).first()

    if jogo: 
        flash ('jogo ja existe!')
        return redirect(url_for('novo_jogo'))
    
    jogo_novo = Jogos(nome =  nome, categoria = categoria, console = console)
    db.session.add(jogo_novo)
    db.session.commit()
    
    salvar_imagem(request.files['img_jogo'], jogo_novo.id)
    return redirect(url_for('index'))


# Rotas para atualizar um jogo 
@app.route('/edit/<int:id>')
def editar_jogo(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', next = url_for('novo_jogo')))
    
    jogo  = Jogos.query.filter_by(id=id).first()
    form  =  FormularioJogo()

    form.nome.data = jogo.nome
    form.categoria.data = jogo.categoria
    form.console.data = jogo.console

    capa_jogo = recupera_imagem(id)
    return render_template('editar.html', title = 'Novo Jogo', id = jogo.id, capa_jogo = capa_jogo, form = form)




@app.route('/atualizar', methods=['POST',])
def atualizar():
    jogo = Jogos.query.filter_by(id =  request.form['id']).first()
   
    form  =  FormularioJogo(request.form)

    if not form.validate_on_submit():
        flash (str(form.errors))
        return redirect(url_for('novo_jogo'))
    
    jogo.nome = form.nome.data
    jogo.categoria = form.categoria.data
    jogo.console = form.console.data

    db.session.add(jogo)
    db.session.commit()
    
    salvar_imagem(request.files['img_jogo'], jogo.id)

    return redirect(url_for('index'))




#Deletar jogo
@app.route('/delete/<int:id>')
def deletar_jogo(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))
     
    Jogos.query.filter_by(id = id).delete()
    db.session.commit()
    flash ('Jogo deletado com sucesso')
    return redirect(url_for('index'))



#Deletar jogo
@app.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
   return send_from_directory('uploads', nome_arquivo)




