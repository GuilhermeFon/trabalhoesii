import unittest
import os
from jogo import criar_tabuleiro, contar_bombas_vizinhas, revelar_tabuleiro, processar_ranking

class TestCampoMinado(unittest.TestCase):

    def test_criar_tabuleiro(self):
        linhas, colunas, bombas = 5, 5, 3
        tabuleiro = criar_tabuleiro(linhas, colunas, bombas)
        self.assertEqual(len(tabuleiro), linhas)
        self.assertEqual(len(tabuleiro[0]), colunas)
        bombas_count = sum(row.count('💣') for row in tabuleiro)
        self.assertEqual(bombas_count, bombas)

    def test_contar_bombas_vizinhas(self):
        tabuleiro = [
            ['🟦', '🟦', '🟦'],
            ['🟦', '💣', '🟦'],
            ['🟦', '🟦', '🟦']
        ]
        self.assertEqual(contar_bombas_vizinhas(tabuleiro, 0, 0), 1)
        self.assertEqual(contar_bombas_vizinhas(tabuleiro, 1, 1), 0)
        self.assertEqual(contar_bombas_vizinhas(tabuleiro, 2, 2), 1)

    def test_revelar_tabuleiro(self):
        tabuleiro = [
            ['🟦', '🟦', '🟦'],
            ['🟦', '💣', '🟦'],
            ['🟦', '🟦', '🟦']
        ]
        tabuleiro_visivel = [
            ['🟦', '🟦', '🟦'],
            ['🟦', '🟦', '🟦'],
            ['🟦', '🟦', '🟦']
        ]
        resultado = revelar_tabuleiro(tabuleiro, tabuleiro_visivel, 0, 0)
        self.assertEqual(resultado, 1)
        self.assertEqual(tabuleiro_visivel[0][0], '1')

        resultado = revelar_tabuleiro(tabuleiro, tabuleiro_visivel, 1, 1)
        self.assertEqual(resultado, -1)
        self.assertEqual(tabuleiro_visivel[1][1], '💥')

    def test_processar_ranking(self):
        nome = "Jogador1"
        celulas_reveladas = 10
        duracao = 100.0
        arquivo_ranking = "ranking_teste.txt"

        with open(arquivo_ranking, "w") as f:
            f.write("Jogador2;15;200.0\n")
            f.write("Jogador3;5;50.0\n")

        processar_ranking(nome, celulas_reveladas, duracao, arquivo_ranking)

        with open(arquivo_ranking, "r") as f:
            linhas = f.readlines()
        
        self.assertIn(f"{nome};{celulas_reveladas};{duracao:.3f}\n", linhas)

        os.remove(arquivo_ranking)

if __name__ == "__main__":
    unittest.main()