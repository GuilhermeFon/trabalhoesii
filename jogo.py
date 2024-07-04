import random        # para gerar posições aleatórias
import time          # controle do tempo 
import os            # funções de sistema operacional
from colorama import Fore, init  # para adicionar cores ao texto no console

init(autoreset=True)  # Inicializa o colorama para que a cor do texto volte ao normal automaticamente após cada impressão.

# Função para criar o tabuleiro do campo minado
def criar_tabuleiro(linhas, colunas, bombas):
    tabuleiro = [['🟦' for _ in range(colunas)] for _ in range(linhas)]
    # Cria um tabuleiro com o número de linhas e colunas especificado, preenchido com o símbolo '🟦'.

    bombas_pos = set()
    while len(bombas_pos) < bombas:
        pos = (random.randint(0, linhas - 1), random.randint(0, colunas - 1))
        bombas_pos.add(pos)

    for linha, coluna in bombas_pos:
        tabuleiro[linha][coluna] = '💣'
        # Coloca as bombas nas posições geradas aleatoriamente no tabuleiro.

    return tabuleiro


def imprimir_tabuleiro(tabuleiro):
    os.system("cls" if os.name == "nt" else "clear")
    # Limpa o console, compatível com Windows ("cls") e outros sistemas operacionais ("clear").

    print("   " + "  ".join(map(str, range(1, len(tabuleiro[0]) + 1))))
    # Imprime os números das colunas.

    for i, linha in enumerate(tabuleiro):
        print(f"{i + 1} " + " ".join(linha))
        # Imprime os números das linhas e o conteúdo do tabuleiro.


def contar_bombas_vizinhas(tabuleiro, linha, coluna):
    linhas, colunas = len(tabuleiro), len(tabuleiro[0])
    # Define o número de linhas e colunas do tabuleiro.

    bombas_vizinhas = 0
    for i in range(max(0, linha - 1), min(linhas, linha + 2)):
        for j in range(max(0, coluna - 1), min(colunas, coluna + 2)):
            if tabuleiro[i][j] == '💣':
                bombas_vizinhas += 1
                # Conta quantas bombas existem nas posições vizinhas.

    return bombas_vizinhas


def revelar_tabuleiro(tabuleiro, tabuleiro_visivel, linha, coluna):
    if not (0 <= linha < len(tabuleiro) and 0 <= coluna < len(tabuleiro[0])):
        return 0
        # Verifica se a posição está dentro dos limites do tabuleiro.

    if tabuleiro_visivel[linha][coluna] != '🟦':
        return 0
        # Verifica se a posição já foi revelada.

    if tabuleiro[linha][coluna] == '💣':
        tabuleiro_visivel[linha][coluna] = '💥'
        return -1
        # Se for uma bomba, revela a bomba e retorna -1.

    bombas_vizinhas = contar_bombas_vizinhas(tabuleiro, linha, coluna)
    tabuleiro_visivel[linha][coluna] = str(bombas_vizinhas)
    reveladas = 1
    # Conta e revela o número de bombas vizinhas na posição.

    if bombas_vizinhas == 0:
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i != 0 or j != 0:
                    reveladas += revelar_tabuleiro(tabuleiro, tabuleiro_visivel, linha + i, coluna + j)

    return reveladas


def carregar_ranking():
    if os.path.isfile("ranking_campo_minado.txt"):
        with open("ranking_campo_minado.txt", "r") as arq:
            return arq.readlines()
    return []
    # Lê o arquivo de ranking, se existir.


def salvar_ranking(jogadores, pontuacoes, tempos):
    com_jogadores = zip(pontuacoes, tempos, jogadores)
    ordenados = sorted(com_jogadores, reverse=True)
    # Ordena os resultados.

    with open("ranking_campo_minado.txt", "w") as arq:
        for posicao, (pontuacao, tempo, jogador) in enumerate(ordenados, 1):
            arq.write(f"{jogador};{pontuacao};{tempo:.3f}\n")
            if jogador == jogadores[-1]:
                print(Fore.RED + f"{posicao:2d} {jogador:20s} {pontuacao:4d} {tempo:7.3f} seg")
            else:
                print(f"{posicao:2d} {jogador:20s} {pontuacao:4d} {tempo:7.3f} seg")
    # Atualiza e exibe o ranking, destacando o resultado do jogador atual.


def processar_ranking(dados):
    jogadores, pontuacoes, tempos = [], [], []
    for linha in dados:
        partes = linha.strip().split(";")
        jogadores.append(partes[0])
        pontuacoes.append(int(partes[1]))
        tempos.append(float(partes[2]))
    return jogadores, pontuacoes, tempos
    # Processa o conteúdo do arquivo de ranking.


def exibir_ranking(jogadores, pontuacoes, tempos, nome):
    print("\nNº Nome do Jogador...: Células Tempo......:")
    print("---------------------------------------------")
    for posicao, (pontuacao, tempo, jogador) in enumerate(zip(pontuacoes, tempos, jogadores), 1):
        if jogador == nome:
            print(Fore.RED + f"{posicao:2d} {jogador:20s} {pontuacao:4d} {tempo:7.3f} seg")
        else:
            print(f"{posicao:2d} {jogador:20s} {pontuacao:4d} {tempo:7.3f} seg")
    # Exibe o ranking, destacando o resultado do jogador atual.


def jogar():
    nome = input("Nome do Jogador: ")
    linhas = int(input("Digite o número de linhas do tabuleiro: "))
    colunas = int(input("Digite o número de colunas do tabuleiro: "))
    bombas = int(input("Digite o número de bombas: "))
    # Solicita o nome do jogador e as configurações do tabuleiro.

    tabuleiro = criar_tabuleiro(linhas, colunas, bombas)
    tabuleiro_visivel = [['🟦' for _ in range(colunas)] for _ in range(linhas)]
    celulas_reveladas = 0
    total_celulas = linhas * colunas - bombas
    hora_inicial = time.time()
    # Inicializa o tabuleiro, o tabuleiro visível, e o contador de células reveladas. Também marca o início do jogo.

    while True:
        imprimir_tabuleiro(tabuleiro_visivel)
        linha_coluna = input("Digite a linha e a coluna (ex: 12 para linha 1 coluna 2) ou 'S' para sair: ").upper()
        # Imprime o tabuleiro visível e solicita a linha e coluna ou opção para sair.

        if linha_coluna == 'S':
            break
            # Se o jogador optar por sair, encerra o loop.

        if len(linha_coluna) != 2 or not linha_coluna.isdigit():
            print(Fore.RED + "Entrada inválida. Tente novamente.")
            time.sleep(2)
            continue
            # Valida a entrada do jogador.

        linha, coluna = int(linha_coluna[0]) - 1, int(linha_coluna[1]) - 1
        # Converte a entrada do jogador em coordenadas do tabuleiro.

        resultado = revelar_tabuleiro(tabuleiro, tabuleiro_visivel, linha, coluna)
        # Revela a célula no tabuleiro.

        if resultado == -1:
            imprimir_tabuleiro(tabuleiro_visivel)
            print(Fore.RED + "Você encontrou uma bomba! Fim de jogo!")
            break
            # Se o jogador revelar uma bomba, termina o jogo.

        celulas_reveladas += resultado
        # Atualiza o contador de células reveladas.

        if celulas_reveladas == total_celulas:
            imprimir_tabuleiro(tabuleiro_visivel)
            print(Fore.GREEN + "Parabéns! Você venceu!")
            break
            # Se todas as células sem bomba foram reveladas, o jogador vence.

    hora_final = time.time()
    duracao = hora_final - hora_inicial
    print(f"{nome} - Você fez um total de {celulas_reveladas} células reveladas!")
    print(f"Tempo: {duracao:.3f} segundos")
    # Calcula e exibe a duração do jogo e o número de células reveladas.

    dados = carregar_ranking()
    jogadores, pontuacoes, tempos = processar_ranking(dados)

    jogadores.append(nome)
    pontuacoes.append(celulas_reveladas)
    tempos.append(duracao)
    # Adiciona o resultado atual ao ranking.

    salvar_ranking(jogadores, pontuacoes, tempos)
    exibir_ranking(jogadores, pontuacoes, tempos, nome)
    # Atualiza, salva e exibe o ranking.


jogar()
