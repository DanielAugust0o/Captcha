import cv2
import os
import glob

arquivos = glob.glob('ajeitado/*')
for arquivo in arquivos:
    imagem = cv2.imread(arquivo)
    imagem = cv2.cvtColor(imagem, cv2.COLOR_RGB2GRAY)
    # EM PRETO E BRANCO
    _, nova_imagem = cv2.threshold(imagem, 0, 255, cv2.THRESH_BINARY_INV)

    # ENCONTRAR OS CONTORNOS DE CADA LETRA
    contornos, _ = cv2.findContours(nova_imagem, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    regiao_letras = []

    # filtrar os contornos que são realmente de letras
    for contorno in contornos:
        x, y, largura, altura = cv2.boundingRect(contorno)
        area = cv2.contourArea(contorno)
        if area > 115:
            regiao_letras.append((x, y, largura, altura))
    if len(regiao_letras) != 5:
        continue

    # DESENHAR OS CONTORNOS E SEPARA AS LETRAS EM ARQUIVOS INDIVIDUAIS
    imagem_final = cv2.merge([imagem] * 3)

    i = 0
    for retangulo in regiao_letras:
        x, y, largura, altura = retangulo
        imagem_letra = imagem[y-2:y+altura+2, x-2:x+largura+2]

        # salvar imagem
        i += 1
        nome_arquivo = os.path.basename(arquivo).replace('.png', f'letra{i}.png')
        cv2.imwrite(f'letras/{nome_arquivo}', imagem_letra)
        cv2.rectangle(imagem_final, (x-2, y-2), (x+largura+2, y+altura+2), (255, 255, 0), 1)
        nome_arquivo = os.path.basename(arquivo)
        cv2.imwrite(f'identificado/{nome_arquivo}', imagem_final)
