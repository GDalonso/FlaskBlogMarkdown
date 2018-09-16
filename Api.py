from flask import Flask, render_template, request, redirect, session, flash, url_for
from functools import wraps
from Database import dbinsert, dbretrieve, dbretrieveusuario, dbinsertusuario, dbretrievepost, dbretrievecategoria, \
    removepost, dblogaction, dbretrieveusers, removeuser
from werkzeug.security import check_password_hash
from pprint import pprint
from markdown import markdown
from models import BlogPost, User
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'YOURSECRETKEYHERE'

#Verify user password when logging in
def check_password(mongouser, password):
    return check_password_hash(mongouser['pw_hash'], password)

# Post lists related
@app.route('/')
def index():
    '''

    :return: Render a list of all posts from database in the home page template
    '''

    dblogaction({'Log': str(request), 'ip': request.remote_addr, 'time': datetime.now()}) #Log to the database

    bancolista = dbretrieve()
    return render_template('lista.html', titulo='Latest Posts', posts=bancolista)

@app.route('/categorie/<_category>')
def categorie(_category: str):
    '''

    :param _category: string name if a category
    :return: The categories view with the posts by that category
    '''

    dblogaction({'Log': str(request), 'ip': request.remote_addr, 'time': datetime.now()}) #Log action to the database

    postsincategory = dbretrievecategoria(_category)
    if postsincategory:
        return render_template('categorie.html', titulo=_category, posts=postsincategory)
    else:
        return render_template('notfound.html')

@app.route('/postview/<_postid>')
def postview(_postid: str):
    '''

    :param _postid: Post id in database
    :return: Render the post with given id to the user
    '''

    dblogaction({'Log': str(request), 'ip': request.remote_addr, 'time': datetime.now()}) #Log to the database

    post = dbretrievepost(_postid)
    local_post = BlogPost(nomePost=post['nomePost'], conteudoPost=post['conteudoPost'],
                descPost=post['descPost'], categoriaPost=post['categoriaPost'],
                imagemPost=post['imagemPost'], dataPost=post['dataPost'])
    return render_template('postview.html', titulo=post['nomePost'], post=local_post)

# CRUDs
@app.route('/novo')
def formcreatepost():
    '''
    Show the view to create a new post
    '''

    if 'user_logged' not in session or session['user_logged'] == None:
        #build a dynamic url to the login function if user if not logged in
        return redirect(url_for('formlogin', proxima=url_for('formlogin')))
    return render_template('novo.html', titulo='Novo Jogo')

@app.route('/criar', methods=['POST',])
def createpost():
    '''
    Create a new post object in the database with the form contents
    '''

    #Contents of the form
    nomePost = request.form['nomePost']
    conteudoPost = markdown(request.form['conteudoPost']).replace('<img alt', '<img style="max-width: 70%;" alt')
    descPost = request.form['descPost']
    categoriaPost = request.form['categoriaPost']
    imagemPost = request.form['imagemPost']
    post = BlogPost(nomePost=nomePost, conteudoPost=conteudoPost, descPost=descPost, categoriaPost=categoriaPost, imagemPost=imagemPost)

    #Insert the object converted to dict in the database
    dbinsert(post.__dict__)
    dblogaction({'Log': str(request), 'ip': request.remote_addr, 'time': datetime.now()})

    #Dynamic route to the index function
    return redirect(url_for('index'))

@app.route('/novousuario')
def formcreateuser():
    '''
    Shows the new user creation screen to the user
    '''

    if 'user_logged' not in session or session['user_logged'] == None:
        # Dynamic route to the login function
        return redirect(url_for('formlogin', proxima=url_for('index')))
    return render_template('criausuario.html', titulo='Novo usuario')

@app.route('/criarusuario', methods=['POST',])
def createuser():
    '''
    Create a User with the create user form contents
    '''

    dblogaction({'Log': str(request), 'ip': request.remote_addr, 'time': datetime.now()}) #Log the action to the database

    # Form contents
    nomeusuario = request. form['nomeusuario']
    senha = request. form['senha']
    nomedisplay = request. form['nomedisplay']
    usuario = User(nomeusuario, nomedisplay, senha)

    # Insert the object converted to dict in the database
    dbinsertusuario(usuario.__dict__)

    # Dynamic route to the index function
    return redirect(url_for('index'))

@app.route('/postslist')
def postslist():
    '''
    List all posts in the database to the manage posts screen
    '''

    dblogaction({'Log': str(request), 'ip': request.remote_addr, 'time': datetime.now()}) #Log the action to the database

    if 'user_logged' not in session or session['user_logged'] == None:
        # Dynamic route to the login function
        return redirect(url_for('formlogin', proxima=url_for('index')))

    #Retrieve all posts from database
    bancolista = dbretrieve()
    return render_template('adminpostslist.html', titulo='Latest Posts', posts=bancolista)

@app.route('/remover/<_postid>')
def deletepost(_postid: str):
    '''
    Remove the post with the given id from the database

    :param _postid: Id of a post to be removed from database
    '''

    dblogaction({'Log': str(request), 'ip': request.remote_addr, 'time': datetime.now()}) # Log the action to the database

    if 'user_logged' not in session or session['user_logged'] == None:
        # Dynamic route to the login function
        return redirect(url_for('formlogin', proxima=url_for('index')))

    post = removepost(_postid)
    return postslist()

@app.route('/editpost/<_postid>')
def editpost(_postid):
    post = dbretrievepost(_postid)

    dblogaction({'Log': str(request), 'ip': request.remote_addr, 'time': datetime.now()})

    return render_template('editarPost.html', post=post)

@app.route('/usersslist')
def userslist():
    '''
    List all users in the database to the manage users screen
    '''

    dblogaction({'Log': str(request), 'ip': request.remote_addr, 'time': datetime.now()}) #Log the action to the database

    if 'user_logged' not in session or session['user_logged'] == None:
        # Dynamic route to the login function
        return redirect(url_for('formlogin', proxima=url_for('index')))

    #Retrieve all posts from database
    bancolista = dbretrieveusers()
    return render_template('adminuserslist.html', titulo='users', users=bancolista)

@app.route('/removeuser/<_userid>')
def deleteuser(_userid: str):
    '''
    delete user with the given id from the database

    :param _userid: Id of a user to be removed from database
    '''

    dblogaction({'Log': str(request), 'ip': request.remote_addr, 'time': datetime.now()}) # Log the action to the database

    if 'user_logged' not in session or session['user_logged'] == None:
        # Dynamic route to the login function
        return redirect(url_for('formlogin', proxima=url_for('index')))

    user = removeuser(_userid)
    return userslist()

# Login related
@app.route('/login')
def formlogin():
    '''
    present to the user the login screen
    '''

    dblogaction({'Log': str(request), 'ip': request.remote_addr, 'time': datetime.now()}) #log the action to the database

    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)

@app.route('/autenticar', methods=['POST', ])
def authenticatelogin():
    '''
    Verify the user and passwords inputed in the login page
    '''

    usuario = dbretrieveusuario(request.form['usuario'])

    if usuario:
        if check_password(usuario, request.form['senha']):
            session['user_logged'] = usuario["username"]
            flash(usuario["username"] + ' is now logged!')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)

    # Show the error message if login fails
    flash('User or Passowrd incorrect, try again')
    return redirect(url_for('formlogin'))

@app.route('/logout')
def logout():
    '''
    Nullify the logged user
    '''

    session['user_logged'] = None
    flash('You need to log in to see this page!')
    return redirect(url_for('formlogin'))



app.run(host='0.0.0.0')
