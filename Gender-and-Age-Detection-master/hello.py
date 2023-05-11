import os
import base64
import tempfile
from flask import Flask, request
import base64
from utilities2 import verificarTodasFotos

app = Flask(__name__)

@app.post('/imagem')
def imagem():

    caminho = ''
    
    if(request.headers.get('Authorization') != 'LoopertImagemAPI;'):
        return {'message': 'Token inválido'}, 401
    
    try:
        # for imagens in request.form:  
        #     print(imagens)
        # se quiser fazer isso, eu acho que não pode tudo se chamar 'image', eu pelo menos não consegui fazer.
        # mas da pra fazer um looping, ai o usuario coloca na key o nome da imagem por exemplo.
        
        image_data = base64.b64decode(request.form['image'])

        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_file:
            temp_file.write(image_data)
            temp_file_path = temp_file.name
            caminho = temp_file_path.replace('\\', '/')
            print(caminho)

        informacoes = verificarTodasFotos(caminho)
    except:
        informacoes = [{}]

    if(caminho):
        os.remove(caminho)
    
    return informacoes

app.run(host='0.0.0.0', port=80)