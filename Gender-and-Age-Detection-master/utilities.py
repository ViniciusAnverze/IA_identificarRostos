import cv2
import os

FACE_PROTO = "opencv_face_detector.pbtxt"
FACE_MODEL = "opencv_face_detector_uint8.pb"
AGE_PROTO = "age_deploy.prototxt"
AGE_MODEL = "age_net.caffemodel"
GENDER_PROTO = "gender_deploy.prototxt"
GENDER_MODEL = "gender_net.caffemodel"

MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
AGE_LIST = ['(0-2)', '(4-6)', '(8-12)', '(15-20)', '(25-32)', '(38-43)', '(48-53)', '(60-100)']
GENDER_LIST = ['Masculino', 'Feminino']

FACE_NET = cv2.dnn.readNet(FACE_MODEL, FACE_PROTO)
AGE_NET = cv2.dnn.readNet(AGE_MODEL, AGE_PROTO)
GENDER_NET = cv2.dnn.readNet(GENDER_MODEL, GENDER_PROTO)


def highlightFace(net, frame, conf_threshold=0.7):
    frameOpencvDnn = frame.copy()
    frameHeight = frameOpencvDnn.shape[0]
    frameWidth = frameOpencvDnn.shape[1]
    blob = cv2.dnn.blobFromImage(frameOpencvDnn, 1.0, (300, 300), [104, 117, 123], True, False)

    net.setInput(blob)
    detections = net.forward()
    faceBoxes = []

    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > conf_threshold:
            x1 = int(detections[0, 0, i, 3]*frameWidth)
            y1 = int(detections[0, 0, i, 4]*frameHeight)
            x2 = int(detections[0, 0, i, 5]*frameWidth)
            y2 = int(detections[0, 0, i, 6]*frameHeight)
            faceBoxes.append([x1, y1, x2, y2])
            cv2.rectangle(frameOpencvDnn, (x1, y1), (x2, y2), (0, 255, 0), int(round(frameHeight/150)), 8)

    return frameOpencvDnn, faceBoxes


def verificarFoto(foto, highlightFace, faixaEtariaFinal, contadorGenero):
    video = cv2.VideoCapture(foto if foto else 0)
    padding = 20
    while cv2.waitKey(1) < 0:

        hasFrame, frame = video.read()
        if not hasFrame:
            cv2.waitKey()
            break

        resultImg, faceBoxes = highlightFace(FACE_NET, frame)

        if not faceBoxes:
            print("Nenhum rosto detectado")

        for faceBox in faceBoxes:
            face = frame[max(0, faceBox[1]-padding): min(faceBox[3]+padding, frame.shape[0]-1), max(0, faceBox[0]-padding):min(faceBox[2]+padding, frame.shape[1]-1)]

            blob = cv2.dnn.blobFromImage(face, 1.0, (227, 227), MODEL_MEAN_VALUES, swapRB=False)
            GENDER_NET.setInput(blob)
            genderPreds = GENDER_NET.forward()
            gender = GENDER_LIST[genderPreds[0].argmax()]
            print(f'Gênero: {gender}')
            if (gender == 'Masculino'):
                contadorGenero['masculino'] += 1
            else:
                contadorGenero['feminino'] += 1

            AGE_NET.setInput(blob)
            agePreds = AGE_NET.forward()
            age = AGE_LIST[agePreds[0].argmax()]
            faixaEtariaFinal[age] += 1
            print(f'Idade: {age[1:-1]} anos')

            cv2.putText(resultImg, f'{gender}, {age}', (faceBox[0], faceBox[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2, cv2.LINE_AA)
            # cv2.imshow("Detecting age and gender", resultImg)


def verificarTodasFotos(listaFotos, data, hora):  

    contadorGenero = {'masculino': 0, 'feminino': 0}

    faixaEtariaFinal = {
    '(0-2)': 0,
    '(4-6)': 0,
    '(8-12)': 0,
    '(15-20)': 0,
    '(25-32)': 0,
    '(38-43)': 0,
    '(48-53)': 0,
    '(60-100)': 0
    }

    for foto in listaFotos:
        try:
            print('nome: '+foto)
            verificarFoto(f'//192.168.1.136/apps/fotos/{data}/{hora}/'+foto, highlightFace, faixaEtariaFinal, contadorGenero)
            print(end='\n')      
        except:
            print('Não encontrado')  
    
    return contadorGenero['masculino'], contadorGenero['feminino'], faixaEtariaFinal


def printarInformacoes(data, hora, contadorMasculino, contadorFeminino, faixaEtariaFinal):
    contadorTotal = contadorFeminino + contadorMasculino
    print('---'*20, end='\n\n')
    print(f'data: {data} \nhora: {hora}')
    print(f'total: {contadorTotal} pessoas identificadas, {contadorMasculino} homens e {contadorFeminino} mulheres')
    print(f'{(contadorMasculino/contadorTotal)*100}% dos ouvintes são homens')
    print(f'{(contadorFeminino/contadorTotal)*100}% dos ouvintes são mulheres', end='\n\n')
    print(f'Número de ouvintes em relação a cada faixa etária:')
    for idade in faixaEtariaFinal:
        print(f'{idade} anos: {faixaEtariaFinal[idade]} ouvinte(s)') 


def escreverTexto(faixaEtariaFinal, data, hora, contadorMasculino, contadorFeminino, filePath):
    text = ''
    contadorTotal = contadorFeminino + contadorMasculino

    for idade in faixaEtariaFinal:
        text += f'{idade} anos: {faixaEtariaFinal[idade]} ouvinte(s) \n'

    try:
        with open(filePath, 'w') as file:
            file.write(
    f"""
data: {data}
hora: {hora}

total: {contadorTotal} pessoas identificadas, {contadorMasculino} homens e {contadorFeminino} mulheres
{(contadorMasculino/contadorTotal)*100}% dos ouvintes são homens
{(contadorFeminino/contadorTotal)*100}% dos ouvintes são mulheres


Número de ouvintes em relação a cada faixa etária:
{text}
""")
    except FileNotFoundError:
        print("Directory or file not found")


def mudarHistorico(caminhoHora, caminhoData, data, hora):
    os.rename(caminhoHora,
            f'{caminhoData}/historico/{hora} - historico')

    if (hora == '00-00'):
        os.rename(f'//192.168.1.136/apps/fotos/{data}',
                f'//192.168.1.136/apps/fotos/historico/{data} - historico')


    return f'//192.168.1.136/apps/fotos/{data}/historico/{hora} - historico/dados.txt'

