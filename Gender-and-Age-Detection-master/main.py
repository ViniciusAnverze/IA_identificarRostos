import os
from utilities import verificarTodasFotos, printarInformacoes, mudarHistorico, escreverTexto

LISTA_DATA = os.listdir('//192.168.1.136/apps/fotos')
LISTA_HORA = os.listdir(f'//192.168.1.136/apps/fotos/{LISTA_DATA[0]}')
LISTA_FOTOS = os.listdir(f'//192.168.1.136/apps/fotos/{LISTA_DATA[0]}/{LISTA_HORA[0]}')

DATA = LISTA_DATA[0]
HORA = LISTA_HORA[0]

CAMINHO_HORA = f'//192.168.1.136/apps/fotos/{DATA}/{HORA}'
CAMINHO_DATA = f'//192.168.1.136/apps/fotos/{DATA}'

contadorMasculino, contadorFeminino, faixaEtariaFinal = verificarTodasFotos(LISTA_FOTOS, DATA, HORA)

printarInformacoes(DATA, HORA, contadorMasculino, contadorFeminino, faixaEtariaFinal)

# filePath = mudarHistorico(CAMINHO_HORA, CAMINHO_DATA, DATA, HORA)

# escreverTexto(faixaEtariaFinal, DATA, HORA, contadorMasculino, contadorFeminino, filePath)

