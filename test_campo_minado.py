import unittest 
from jogo import criar_tabuleiro, contar_bombas_vizinhas


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
        