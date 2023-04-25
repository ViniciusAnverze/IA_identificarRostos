import os
from detect import verificarTodasFotos, printarInformacoes, mudarHistorico, escreverTexto

LISTA_DATA = os.listdir('//192.168.1.136/apps/fotos')
LISTA_HORA = os.listdir(f'//192.168.1.136/apps/fotos/{LISTA_DATA[0]}')
LISTA_FOTOS = os.listdir(f'//192.168.1.136/apps/fotos/{LISTA_DATA[0]}/{LISTA_HORA[0]}')

DATA = LISTA_DATA[0]
HORA = LISTA_HORA[0]

CAMINHO_HORA = f'//192.168.1.136/apps/fotos/{DATA}/{HORA}'
CAMINHO_DATA = f'//192.168.1.136/apps/fotos/{DATA}'

MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
AGE_LIST = ['(0-2)', '(4-6)', '(8-12)', '(15-20)', '(25-32)', '(38-43)', '(48-53)', '(60-100)']
GENDER_LIST = ['Masculino', 'Feminino']

contadorMasculino, contadorFeminino, faixaEtariaFinal = verificarTodasFotos(LISTA_FOTOS, DATA, HORA)

printarInformacoes(DATA, HORA, contadorMasculino, contadorFeminino, faixaEtariaFinal)

filePath = mudarHistorico(CAMINHO_HORA, CAMINHO_DATA, DATA, HORA)

escreverTexto(faixaEtariaFinal, DATA, HORA, contadorMasculino, contadorFeminino, filePath)