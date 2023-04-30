# Gerador de Cartelas de Bingo.

Para gerar as cartelas, basta selecionar o arquivo "main_2.py" e alterar a variável "num_paginas". É importante que o número de páginas seja um valor par, uma vez que cada duas folhas A4 correspondem a uma cartela frente e verso com 10 rodadas.

A "main.py" é para gerar um .exe ou seja. -> Não terminei <-
Execute o comando:

```bash
pyinstaller --onefile main.py
```

Para gerar o buid do projeto e gerar o .exe

Quando o .exe for gerado, não esqueça de criar "free_image.png" e "imagem_exemplo.jpg" na pasta build.
