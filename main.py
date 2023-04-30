import random
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from tqdm import tqdm
import argparse

NUM_COLUNAS = 5
NUM_LINHAS = 5
TAMANHO_COLUNA = 15
TAMANHO_CELULA = 15 * mm

def criar_cartela_bingo():
    cartela_bingo = []
    for i in range(NUM_COLUNAS):
        if i < NUM_COLUNAS - 1:
            coluna = sorted(random.sample(range(i * TAMANHO_COLUNA + 1, (i + 1) * TAMANHO_COLUNA + 1), NUM_LINHAS))
        else:
            coluna = sorted(random.sample(range(i * TAMANHO_COLUNA + 1, 75 + 1), NUM_LINHAS))
        cartela_bingo.append(coluna)
    return cartela_bingo

def desenhar_cartela_bingo(c, x, y, cartela_bingo, rodada):
    tamanho_celula = 15 * mm
    bingo = "BINGO"
    free_image = "free_image.png"

    for i, letra in enumerate(bingo):
        c.setFont("Helvetica-Bold", 18)
        c.drawCentredString(x + i * tamanho_celula + tamanho_celula / 2, y + 5 * tamanho_celula + 2 * mm, letra)

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

def main(num_paginas):
    arquivo_saida = "cartelas_bingo.pdf"
    nome_evento = "Evento de Bingo"
    data = "01/01/2023"
    horario = "20:00"
    imagem_exemplo = "imagem_exemplo.jpg"

    c = canvas.Canvas(arquivo_saida, pagesize=A4)
    c.setStrokeColorRGB(0, 0, 0)

    espaco_entre_cartelas = 11.5 * mm
    espaco_abaixo_cabecalho = 22 * mm

    with tqdm(total=num_paginas) as pbar:
        for pagina in range(num_paginas):
            x_cabecalho = 105 * mm
            y_cabecalho = 297 * mm - 10 * mm
            num_cartela = (pagina // 2) + 1
            desenhar_cabecalho(c, x_cabecalho, y_cabecalho, nome_evento, data, horario, num_cartela)

            for coluna in range(2):
                x_cartela = 25 * mm if coluna == 0 else 110 * mm
                for indice_cartela in range(3 if coluna == 0 else 2):
                    try:
                        cartela_bingo = criar_cartela_bingo()
                        rodada = (pagina * 5 + coluna * 3 + indice_cartela) % 10 + 1

                        y_cartela = (250 - espaco_abaixo_cabecalho - indice_cartela * (55 + espaco_entre_cartelas)) * mm
                        desenhar_cartela_bingo(c, x_cartela, y_cartela, cartela_bingo, rodada)

                        pbar.update(1)

                        if (pagina * 5 + coluna * 3 + indice_cartela) % 5 == 4:
                            c.drawImage(imagem_exemplo, x_cartela + 0 * mm, y_cartela - 90 * mm, 75 * mm, 75 * mm)
                    except Exception as e:
                        print(f"Erro ao gerar cartela: {str(e)}")
            pbar.update(1)
            c.showPage()

    c.save()

def main_menu():
    while True:
        try:
            opcao = int(input("Selecione uma opção:\n---------------------------\n1. Gerar cartelas de bingo\n2. Sair\n---------------------------\nOpção:"))
            if opcao == 1:
                num_paginas = int(input("Digite o número de páginas de cartelas a serem geradas: "))
                main(num_paginas)
                print("---------------------------\n100% [/////////////////] Cartelas geradas com sucesso!\n---------------------------")
            elif opcao == 2:
                print("---------------------------\n-> Saindo...\n---------------------------")
                break
        except ValueError:
            print("---------------------------\n-> Entrada inválida! Digite um número válido.\n---------------------------")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Gerador de cartelas de bingo")
    parser.add_argument("num_paginas", type=int, nargs="?", help="Número de páginas de cartelas a serem geradas")
    args = parser.parse_args()
    if args.num_paginas is None:
        main_menu()
    else:
        main(args.num_paginas)
        print("---------------------------\n100% [/////////////////] Cartelas geradas com sucesso!\n---------------------------")
