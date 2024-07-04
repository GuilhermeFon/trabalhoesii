import unittest
from jogo import criar_tabuleiro

class TestCampoMinado(unittest.TestCase):

    def test_criar_tabuleiro(self):
        linhas, colunas, bombas = 5, 5, 3
        tabuleiro = criar_tabuleiro(linhas, colunas, bombas)
        self.assertEqual(len(tabuleiro), linhas)
        self.assertEqual(len(tabuleiro[0]), colunas)
        bombas_count = sum(row.count('💣') for row in tabuleiro)
        self.assertEqual(bombas_count, bombas)