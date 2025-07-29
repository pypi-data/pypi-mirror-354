import cv2
import numpy as np

def carregar_imagem(caminho):
    return cv2.imread(caminho)

def salvar_imagem(caminho, imagem):
    cv2.imwrite(caminho, imagem)

def converter_para_cinza(imagem):
    return cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)

def redimensionar(imagem, largura, altura):
    return cv2.resize(imagem, (largura, altura))

def detectar_bordas(imagem):
    imagem_cinza = converter_para_cinza(imagem)
    return cv2.Canny(imagem_cinza, 50, 150)
