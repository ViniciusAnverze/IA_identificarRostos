import cv2

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

    return faceBoxes



def verificarFoto(foto):

    informacoes = []

    video = cv2.VideoCapture(foto if foto else 0)
    padding = 20
    while cv2.waitKey(1) < 0:
        hasFrame, frame = video.read()
        if not hasFrame:
            cv2.waitKey()
            break
        print(type(frame))

        faceBoxes = highlightFace(FACE_NET, frame)

        if not faceBoxes:
            print("Nenhum rosto detectado")

        for faceBox in faceBoxes:

            pessoa = {}

            face = frame[max(0, faceBox[1]-padding): min(faceBox[3]+padding, frame.shape[0]-1), max(0, faceBox[0]-padding):min(faceBox[2]+padding, frame.shape[1]-1)]

            blob = cv2.dnn.blobFromImage(face, 1.0, (227, 227), MODEL_MEAN_VALUES, swapRB=False)

            GENDER_NET.setInput(blob)
            genderPreds = GENDER_NET.forward()
            gender = GENDER_LIST[genderPreds[0].argmax()]

            if (gender == 'Masculino'):
                pessoa['genero'] = 'masculino'
            else:
                pessoa['genero'] = 'feminino' 

            AGE_NET.setInput(blob)
            agePreds = AGE_NET.forward()
            age = AGE_LIST[agePreds[0].argmax()]
            pessoa['idade'] = age

            informacoes.append(pessoa)

        return informacoes


def verificarTodasFotos(foto):  

    informacoes = verificarFoto(foto)   
    
    return informacoes

