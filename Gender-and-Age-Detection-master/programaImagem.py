import base64

with open('./foto6.png', 'rb') as imagem:
    encoded_image = base64.b64encode(imagem.read()).decode('utf-8')
    print(encoded_image)