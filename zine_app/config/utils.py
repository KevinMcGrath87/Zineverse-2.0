import os
from zine_app.__init__ import app

app.config['DATABASE'] = "zineverse"
app.config['UPLOAD_FOLDER']=os.path.join(os.path.dirname(os.getcwd()),'zineverse_2.0','zine_app','static','zinelib')

DATABASE = app.config['DATABASE']
UPLOAD_FOLDER = app.config['UPLOAD_FOLDER']
ALLOWED_EXTENSIONS = {'pdf','png','jpg','jpeg','svg'}