import cv2
import os

# listaData = os.listdir('C:/Users/Dell/Desktop/ia/Gender-and-Age-Detection-master/Gender-and-Age-Detection-master/fotos')
# listaHora = os.listdir(f'C:/Users/Dell/Desktop/ia/Gender-and-Age-Detection-master/Gender-and-Age-Detection-master/fotos/{listaData[0]}')
# listaFotos = os.listdir(f'C:/Users/Dell/Desktop/ia/Gender-and-Age-Detection-master/Gender-and-Age-Detection-master/fotos/{listaData[0]}/{listaHora[0]}')
# ##Ele pega o primeiro termo do horario, por isso não pega a pasta historico.

listaData = os.listdir('//192.168.1.136/apps/fotos')
listaHora = os.listdir(f'//192.168.1.136/apps/fotos/{listaData[0]}')
listaFotos = os.listdir(f'//192.168.1.136/apps/fotos/{listaData[0]}/{listaHora[0]}')
# Ele pega o primeiro termo do horario, por isso não pega a pasta historico.

contadorMasculino = 0
contadorFeminino = 0


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


faceProto = "opencv_face_detector.pbtxt"
faceModel = "opencv_face_detector_uint8.pb"
ageProto = "age_deploy.prototxt"
ageModel = "age_net.caffemodel"
genderProto = "gender_deploy.prototxt"
genderModel = "gender_net.caffemodel"

MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
ageList = ['(0-2)', '(4-6)', '(8-12)', '(15-20)', '(25-32)', '(38-43)', '(48-53)', '(60-100)']

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

genderList = ['Masculino', 'Feminino']

faceNet = cv2.dnn.readNet(faceModel, faceProto)
ageNet = cv2.dnn.readNet(ageModel, ageProto)
genderNet = cv2.dnn.readNet(genderModel, genderProto)


def verificarFoto(foto):
    video = cv2.VideoCapture(foto if foto else 0)
    padding = 20
    while cv2.waitKey(1) < 0:

        hasFrame, frame = video.read()
        if not hasFrame:
            cv2.waitKey()
            break

        resultImg, faceBoxes = highlightFace(faceNet, frame)
        if not faceBoxes:
            print("Nenhum rosto detectado")

        for faceBox in faceBoxes:
            face = frame[max(0, faceBox[1]-padding): min(faceBox[3]+padding, frame.shape[0]-1), max(0, faceBox[0]-padding):min(faceBox[2]+padding, frame.shape[1]-1)]

            blob = cv2.dnn.blobFromImage(face, 1.0, (227, 227), MODEL_MEAN_VALUES, swapRB=False)
            genderNet.setInput(blob)
            genderPreds = genderNet.forward()
            gender = genderList[genderPreds[0].argmax()]
            print(f'Gênero: {gender}')
            if (gender == 'Masculino'):
                global contadorMasculino
                contadorMasculino += 1
            else:
                global contadorFeminino
                contadorFeminino += 1

            ageNet.setInput(blob)
            agePreds = ageNet.forward()
            age = ageList[agePreds[0].argmax()]
            faixaEtariaFinal[age] += 1
            print(f'Idade: {age[1:-1]} anos')

            cv2.putText(resultImg, f'{gender}, {age}', (faceBox[0], faceBox[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2, cv2.LINE_AA)
            # cv2.imshow("Detecting age and gender", resultImg)


for foto in listaFotos:
    print('nome: '+foto)
    # verificarFoto(f'./fotos/{listaData[0]}/{listaHora[0]}/'+foto)
    verificarFoto(f'//192.168.1.136/apps/fotos/{listaData[0]}/{listaHora[0]}/'+foto)
    print(end='\n')

contadorTotal = contadorMasculino+contadorFeminino

print('---'*20, end='\n\n')
print(f'data: {listaData[0]} \nhora: {listaHora[0]}')
print(f'total: {contadorTotal} pessoas identificadas, {contadorMasculino} homens e {contadorFeminino} mulheres')
print(f'{(contadorMasculino/contadorTotal)*100}% dos ouvintes são homens')
print(f'{(contadorFeminino/contadorTotal)*100}% dos ouvintes são mulheres', end='\n\n')
print(f'Número de ouvintes em relação a cada faixa etária:')
for idade in faixaEtariaFinal:
    print(f'{idade} anos: {faixaEtariaFinal[idade]} ouvinte(s)')

# os.rename(f'C:/Users/Dell/Desktop/ia/Gender-and-Age-Detection-master/Gender-and-Age-Detection-master/fotos/{listaData[0]}/{listaHora[0]}', f'C:/Users/Dell/Desktop/ia/Gender-and-Age-Detection-master/Gender-and-Age-Detection-master/fotos/{listaData[0]}/historico/{listaHora[0]} - historico')

# if(listaHora[0] == '23-30-00'):
#     os.rename(f'C:/Users/Dell/Desktop/ia/Gender-and-Age-Detection-master/Gender-and-Age-Detection-master/fotos/{listaData[0]}', f'C:/Users/Dell/Desktop/ia/Gender-and-Age-Detection-master/Gender-and-Age-Detection-master/fotos/historico/{listaData[0]} - historico')
text = ''

for idade in faixaEtariaFinal:
    text += f'{idade} anos: {faixaEtariaFinal[idade]} ouvinte(s) \n'


os.rename(f'//192.168.1.136/apps/fotos/{listaData[0]}/{listaHora[0]}',
          f'//192.168.1.136/apps/fotos/{listaData[0]}/historico/{listaHora[0]} - historico')

if (listaHora[0] == '00-00'):
    os.rename(f'//192.168.1.136/apps/fotos/{listaData[0]}',
              f'//192.168.1.136/apps/fotos/historico/{listaData[0]} - historico')


file_path =f'//192.168.1.136/apps/fotos/{listaData[0]}/historico/{listaHora[0]} - historico/dados.txt'

try:
    with open(file_path, 'w') as file:
        file.write(
f"""
data: {listaData[0]}
hora: {listaHora[0]}

total: {contadorTotal} pessoas identificadas, {contadorMasculino} homens e {contadorFeminino} mulheres
{(contadorMasculino/contadorTotal)*100}% dos ouvintes são homens
{(contadorFeminino/contadorTotal)*100}% dos ouvintes são mulheres


Número de ouvintes em relação a cada faixa etária:
{text}
"""
        )
except FileNotFoundError:
    print("Directory or file not found")
