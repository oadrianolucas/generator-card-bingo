from flask import Flask, render_template, request, redirect, url_for
import random
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from tqdm import tqdm
import re

NUM_COLUNAS = 5
NUM_LINHAS = 5
TAMANHO_COLUNA = 15
TAMANHO_CELULA = 15 * mm

imagens_rodadas = [f"imagens/rodada_{i}.png" for i in range(1, 10)]

app = Flask(__name__)


def criar_cartela_bingo():
    cartela_bingo = []
    for i in range(NUM_COLUNAS):
        if i < NUM_COLUNAS - 1:
            coluna = sorted(random.sample(
                range(i * TAMANHO_COLUNA + 1, (i + 1) * TAMANHO_COLUNA + 1), NUM_LINHAS))
        else:
            coluna = sorted(random.sample(
                range(i * TAMANHO_COLUNA + 1, 75 + 1), NUM_LINHAS))
        cartela_bingo.append(coluna)
    return cartela_bingo


def desenhar_cartela_bingo(c, x, y, cartela_bingo, rodada):
    tamanho_celula = 15 * mm
    bingo = "BINGO"

    for i, letra in enumerate(bingo):
        c.setFont("Helvetica-Bold", 18)
        c.drawCentredString(x + i * tamanho_celula + tamanho_celula /
                            2, y + 5 * tamanho_celula + 2 * mm, letra)

    for i, coluna in enumerate(cartela_bingo):
        for j, numero in enumerate(coluna):
            if i == 2 and j == 2:
                c.setFont("Helvetica-Bold", 18)
                c.drawCentredString(x + i * tamanho_celula + tamanho_celula / 2,
                                    y + j * tamanho_celula + tamanho_celula / 2, "FREE")
            else:
                c.rect(x + i * tamanho_celula, y + j *
                       tamanho_celula, tamanho_celula, tamanho_celula)
                c.setFont("Helvetica", 18)
                c.drawCentredString(x + i * tamanho_celula + tamanho_celula / 2,
                                    y + j * tamanho_celula + tamanho_celula / 3, str(numero))

    c.setFont("Helvetica-Bold", 9)
    c.drawCentredString(x + 0.52 * tamanho_celula,
                        y - 4 * mm, f"RODADA {rodada}")


def desenhar_cabecalho(c, x, y, nome_evento, data, horario, num_cartela):
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(x, y, nome_evento)
    c.setFont("Helvetica", 14)
    c.drawCentredString(x, y - 6 * mm, f"{data} às {horario}")
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(x, y - 12 * mm, f"Cartela: {num_cartela}")


def nome_arquivo_valido(nome_evento):
    return re.sub(r'[\/:*?"<>|]', '_', nome_evento)


def main(num_paginas, nome_evento, horario, data):
    imagem_exemplo = "imagem_exemplo.jpg"
    imagem_exemplo_2 = "imagem_exemplo2.jpg"
    nome_arquivo = f"pdfs/{nome_arquivo_valido(nome_evento)}.pdf"

    c = canvas.Canvas(nome_arquivo, pagesize=A4)
    c.setStrokeColorRGB(0, 0, 0)
    espaco_entre_cartelas = 11.5 * mm
    espaco_abaixo_cabecalho = 22 * mm

    with tqdm(total=num_paginas) as pbar:
        for pagina in range(num_paginas):
            imagem_atual = imagem_exemplo_2 if pagina % 2 == 0 else imagem_exemplo

            x_cabecalho = 105 * mm
            y_cabecalho = 297 * mm - 10 * mm
            num_cartela = (pagina // 2) + 1
            desenhar_cabecalho(c, x_cabecalho, y_cabecalho,
                               nome_evento, data, horario, num_cartela)
            for coluna in range(2):
                x_cartela = 25 * mm if coluna == 0 else 110 * mm
                for indice_cartela in range(3 if coluna == 0 else 2):
                    try:
                        cartela_bingo = criar_cartela_bingo()
                        rodada = (pagina * 5 + coluna * 3 +
                                  indice_cartela) % 10 + 1

                        y_cartela = (250 - espaco_abaixo_cabecalho -
                                     indice_cartela * (55 + espaco_entre_cartelas)) * mm
                        desenhar_cartela_bingo(
                            c, x_cartela, y_cartela, cartela_bingo, rodada)

                        pbar.update(1)

                        if (pagina * 5 + coluna * 3 + indice_cartela) % 5 == 4:
                            c.drawImage(imagem_atual, x_cartela + 0 *
                                        mm, y_cartela - 90 * mm, 75 * mm, 75 * mm)
                    except Exception as e:
                        print(f"Erro ao gerar cartela: {str(e)}")
            pbar.update(1)
            c.showPage()
    c.save()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/gerar_cartelas', methods=['POST'])
def gerar_cartelas():
    nome_evento = request.form.get('evento')
    data = request.form.get('data')
    horario = request.form.get('horario')
    num_paginas = int(request.form.get('paginas'))
    num_rodadas = int(request.form.get('rodadas'))
    main(num_paginas, nome_evento, horario, data, num_rodadas)
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)
