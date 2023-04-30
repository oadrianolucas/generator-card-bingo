import random
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from tqdm import tqdm

NUM_COLUNAS = 5
NUM_LINHAS = 5
TAMANHO_COLUNA = 15
TAMANHO_CELULA = 15 * mm

cartelas_geradas = []
def criar_cartela_bingo():
    while True:
        cartela_bingo = []
        for i in range(NUM_COLUNAS):
            if i < NUM_COLUNAS - 1:
                coluna = sorted(random.sample(range(i * TAMANHO_COLUNA + 1, (i + 1) * TAMANHO_COLUNA + 1), NUM_LINHAS))
            else:
                coluna = sorted(random.sample(range(i * TAMANHO_COLUNA + 1, 75 + 1), NUM_LINHAS))
            cartela_bingo.append(coluna)
        
        cartela_tuple = tuple(tuple(coluna) for coluna in cartela_bingo)
        if cartela_tuple not in cartelas_geradas:
            cartelas_geradas.append(cartela_tuple)
            return cartela_bingo

def desenhar_cartela_bingo(c, x, y, cartela_bingo, rodada):
    tamanho_celula = 15 * mm
    bingo = "BINGO"
    free_image = "free_image.png"
    
    for i, letra in enumerate(bingo):
        c.setFont("Helvetica-Bold", 18)
        c.drawCentredString(x + i * tamanho_celula + tamanho_celula / 2, y + 5 * tamanho_celula + 2 * mm, letra)

    # Se quiser trocar a imagem e adicionar um texto no lugar do FREE
    #for i, letra in enumerate(bingo):
    #    c.setFont("Helvetica-Bold", 18)
    #    c.drawCentredString(x + i * tamanho_celula + tamanho_celula / 2, y + 5 * tamanho_celula + 2 * mm, letra)

    for i, coluna in enumerate(cartela_bingo):
        for j, numero in enumerate(coluna):
            if i == 2 and j == 2:
                c.drawImage(free_image, x + i * tamanho_celula, y + j * tamanho_celula, tamanho_celula, tamanho_celula)
            else:
                c.rect(x + i * tamanho_celula, y + j * tamanho_celula, tamanho_celula, tamanho_celula)
                c.setFont("Helvetica", 18)
                c.drawCentredString(x + i * tamanho_celula + tamanho_celula / 2, y + j * tamanho_celula + tamanho_celula / 3, str(numero))

    c.setFont("Helvetica-Bold", 9)
    c.drawCentredString(x + 0.52 * tamanho_celula, y - 4 * mm, f"RODADA {rodada}")

def desenhar_cabecalho(c, x, y, nome_evento, data, horario, num_cartela):
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(x, y, nome_evento)
    c.setFont("Helvetica", 14)
    c.drawCentredString(x, y - 6 * mm, f"{data} às {horario}")
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(x, y - 12 * mm, f"Cartela: {num_cartela}")

def desenhar_cabecalho(c, x, y, nome_evento, data, horario, num_cartela):
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(x, y, nome_evento)
    c.setFont("Helvetica", 14)
    c.drawCentredString(x, y - 6 * mm, f"{data} às {horario}")
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(x, y - 12 * mm, f"Cartela: {num_cartela}")

def main():
    arquivo_saida = "cartelas_bingo.pdf"
    num_paginas = 1000
    nome_evento = "Evento de Bingo"
    data = "01/01/2023"
    horario = "20:00"
    imagem_exemplo = "imagem_exemplo.jpg"

    c = canvas.Canvas(arquivo_saida, pagesize=A4)
    c.setStrokeColorRGB(0, 0, 0)

    espaco_entre_cartelas = 11.5 * mm
    espaco_abaixo_cabecalho = 22 * mm

    for pagina in tqdm(range(num_paginas), desc="Gerando 'cartelas_bingo.pdf'"):
        x_cabecalho = 105 * mm
        y_cabecalho = 297 * mm - 10 * mm
        num_cartela = (pagina // 2) + 1
        desenhar_cabecalho(c, x_cabecalho, y_cabecalho, nome_evento, data, horario, num_cartela)

        for coluna in range(2):
            x_cartela = 25 * mm if coluna == 0 else 110 * mm
            for indice_cartela in range(3 if coluna == 0 else 2):
                cartela_bingo = criar_cartela_bingo()
                rodada = (pagina * 5 + coluna * 3 + indice_cartela) % 10 + 1

                y_cartela = (250 - espaco_abaixo_cabecalho - indice_cartela * (55 + espaco_entre_cartelas)) * mm
                desenhar_cartela_bingo(c, x_cartela, y_cartela, cartela_bingo, rodada)

                if (pagina * 5 + coluna * 3 + indice_cartela) % 5 == 4:
                    c.drawImage(imagem_exemplo, x_cartela + 0 * mm, y_cartela - 90 * mm, 75 * mm, 75 * mm)

        c.showPage()

    c.save()

if __name__ == "__main__":
    main()