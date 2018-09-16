# FlaskWebApp

Blog built with Flask, MongoDB hosted in MLab with autentication, interface to create posts and users, and to delete them.

Post can be written in Markdown, for convenience.

Live version in [Umobiteam](http://blog.umobiteam.com/)

### Files tree

###### Root

    Api.py : Contain all the Flask app structure, with routes and corresponding functions.
    
    Database.py: Contain all the operations envolving mongodb, hosted in mlab.
    
    Setup.py: Dependencies.

###### /templates

Blog Pages

    template.html : The base template of the application.
    
    lista.html : The index page.
    
    notfound.html: 404 page.
    
    postview.html: Post visualization page.
    
    categorie.html: Posts of a given category visualization.

Administration pages
    
    BACKtemplate.html: template used in the administration pages.
    
    adminpostslis.html: Post deletion form.
    
    adminuserslis.html: User deletion form.
    
    criausuario.html: User creation form.
    
    novo.html : Post creation form.
    
    login.html : Login form.

###### /static

The static files needed to the template such as CSS and JS scripts.


##### Update the Database.py file with your database connection data
    def connectDB(coll: str):
        try:
            #Create the auth client in mlab
            client = MongoClient('PUT YOUR CONNECTION STRING HERE')
            #Select the database we want to use
            db = client.YOURDATABASENAME
            #Return the desired collection
            if coll == 'posts':
                return db.YOURPOSTSCOLLECTIONNAME
            elif coll == 'users':
                return db.YOURUSERSSCOLLECTIONNAME
            elif coll == 'logs':
                return db.YOURLOGSCOLLECTIONNAME
        except:
            print ("Error trying to connect to database")

## Deploy with virtualEnv
            
Install pip3 if you're using Linux

`sudo apt-get install python3-pip`

When you install Python 3 in Windows it install pip3 too.

Create a virtualenv inside FlaskBlogMarkdown folder

`virtualenv venvflaskblog`

Activate VirtualEnv

`source venvflaskblog/bin/activate`

Install dependencies on the virtualenv

`python Setup.py install`

## Export and run the application

### Linux Script
`chmod 777 run.sh`

`./run.sh`

### Linux
`export FLASK_APP=Api.py`

`Python3 Api.py`

### Windows
`set FLASK_APP=Api.py`

`flask run`
