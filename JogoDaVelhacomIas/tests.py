"""Testes do JogoDaVelhacomIas.

Rodar:
    .venv/bin/python tests.py
    .venv/bin/python -m unittest tests -v

Nenhum teste chama o Ollama: o LLM e trocado por um duble que devolve jogadas
pre-programadas. Assim o que fica sob teste e a logica do grafo, nao o modelo.

Cada teste falha por um defeito especifico do codigo atual. A mensagem de falha
diz qual comportamento era esperado.
"""

import builtins
import io
import os
import sys
import unittest
from contextlib import redirect_stdout
from types import SimpleNamespace
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import graph
import utils
from llm import OStructure
from pydantic import ValidationError

VAZIO = "."

# Roteiro que empata: X pega 0, 2, 3, 7, 8 / O pega 1, 4, 5, 6.
# Serve para testar partida completa sem vitoria no meio.
JOGADAS_EMPATE = [0, 1, 2, 4, 3, 5, 7, 6, 8]
TABULEIRO_EMPATE = ["X", "O", "X", "X", "O", "O", "O", "X", "X"]


class FakeLLM:
    """Substitui load_llm.

    - devolve as jogadas do roteiro, uma por chamada;
    - registra com qual modelo foi chamado (modelos_pedidos);
    - registra as mensagens enviadas (prompts).
    """

    def __init__(self, jogadas):
        self.jogadas = list(jogadas)
        self.modelos_pedidos = []
        self.prompts = []

    def __call__(self, model=None, **kwargs):
        self.modelos_pedidos.append(model)
        return self

    def invoke(self, messages):
        self.prompts.append(messages)
        if not self.jogadas:
            raise AssertionError(
                "LLM foi chamado mais vezes do que o roteiro previu. "
                "O grafo nao parou quando devia."
            )
        return SimpleNamespace(pos=self.jogadas.pop(0))


class GraphTestCase(unittest.TestCase):
    """Base: neutraliza entrada de teclado, clear de tela e o LLM."""

    respostas_modelo = ("1", "1")

    def setUp(self):
        self.fake = FakeLLM([])
        self.entradas = list(self.respostas_modelo)
        self.avisos_de_vitoria = []

        patches = [
            mock.patch.object(graph, "load_llm", self.fake),
            mock.patch.object(graph.os, "system", return_value=0),
            mock.patch.object(
                builtins, "input", side_effect=lambda prompt="": self.entradas.pop(0)
            ),
            # winMessage real tem sleep de 0.1s por caractere
            mock.patch.object(graph, "winMessage", self.avisos_de_vitoria.append),
        ]
        for patch in patches:
            patch.start()
            self.addCleanup(patch.stop)

    def jogar(self, jogadas, tabuleiro=None, limite=60):
        """Roda a partida com o roteiro de jogadas e devolve (resultado, tabuleiro)."""
        self.fake.jogadas = list(jogadas)
        if tabuleiro is None:
            tabuleiro = [VAZIO] * 9
        with redirect_stdout(io.StringIO()):
            resultado = graph.buildGraph().invoke(
                {"board": tabuleiro}, {"recursion_limit": limite}
            )
        return resultado, tabuleiro


class TestValidMove(unittest.TestCase):
    def test_casa_livre_dentro_do_tabuleiro_e_valida(self):
        for pos in (0, 4, 8):
            with self.subTest(pos=pos):
                self.assertTrue(
                    utils.validMove([VAZIO] * 9, pos),
                    f"casa {pos} esta livre e dentro de 0..8, deveria ser valida",
                )

    def test_posicao_9_e_invalida(self):
        self.assertFalse(
            utils.validMove([VAZIO] * 9, 9),
            "9 nao existe num tabuleiro de 9 casas (0..8)",
        )

    def test_posicao_negativa_e_invalida(self):
        self.assertFalse(
            utils.validMove([VAZIO] * 9, -1),
            "-1 nao e indice valido",
        )

    def test_casa_ocupada_e_invalida(self):
        tabuleiro = ["X"] + [VAZIO] * 8
        self.assertFalse(
            utils.validMove(tabuleiro, 0),
            "casa 0 ja tem X, nao pode receber jogada",
        )


class TestCheckTie(unittest.TestCase):
    TABULEIRO_CHEIO = ["X", "O", "X", "O", "X", "O", "O", "X", "O"]

    def test_tabuleiro_cheio_e_empate(self):
        with redirect_stdout(io.StringIO()):
            self.assertTrue(
                utils.checkTie(self.TABULEIRO_CHEIO),
                "sem casa vazia o jogo empatou",
            )

    def test_tabuleiro_com_casa_livre_nao_e_empate(self):
        with redirect_stdout(io.StringIO()):
            self.assertFalse(
                utils.checkTie([VAZIO] * 9),
                "tabuleiro ainda tem casa livre",
            )

    def test_mensagem_de_empate_e_impressa_inteira(self):
        saida = io.StringIO()
        with redirect_stdout(saida):
            utils.checkTie(self.TABULEIRO_CHEIO)
        texto = "".join(saida.getvalue().split())
        self.assertIn(
            "OJOGOEMPATOU",
            texto,
            "a mensagem de empate foi cortada antes do fim",
        )


class TestOStructure(unittest.TestCase):
    def test_aceita_casas_de_0_a_8(self):
        for pos in (0, 4, 8):
            with self.subTest(pos=pos):
                OStructure(pos=pos)

    def test_rejeita_9(self):
        with self.assertRaises(ValidationError):
            OStructure(pos=9)

    def test_rejeita_posicao_negativa(self):
        with self.assertRaises(ValidationError):
            OStructure(pos=-1)


class TestJogo(GraphTestCase):
    def test_x_joga_primeiro(self):
        resultado, _ = self.jogar(JOGADAS_EMPATE)
        self.assertEqual(
            resultado["board"][0],
            "X",
            "quem comeca no jogo da velha e X",
        )

    def test_jogadas_alternam_entre_x_e_o(self):
        resultado, _ = self.jogar(JOGADAS_EMPATE)
        self.assertEqual(
            resultado["board"],
            TABULEIRO_EMPATE,
            "as jogadas devem alternar X, O, X, O... ate o tabuleiro encher",
        )

    def test_vitoria_de_x_encerra_a_partida(self):
        # X: 0, 3, 6 (coluna da esquerda) | O: 1, 2
        resultado, _ = self.jogar([0, 1, 3, 2, 6])
        self.assertEqual(
            resultado["board"],
            ["X", "O", "O", "X", VAZIO, VAZIO, "X", VAZIO, VAZIO],
            "a partida deve terminar assim que X fecha a trinca",
        )
        self.assertEqual(
            self.avisos_de_vitoria,
            ["X"],
            "o vencedor deve ser anunciado uma unica vez",
        )

    def test_empate_encerra_com_tabuleiro_cheio(self):
        # X: 0, 2, 3, 7, 8 | O: 1, 4, 5, 6  -> ninguem fecha trinca
        resultado, _ = self.jogar([0, 1, 2, 4, 3, 5, 7, 6, 8])
        self.assertNotIn(
            VAZIO,
            resultado["board"],
            "no empate todas as 9 casas ficam ocupadas",
        )
        self.assertEqual(
            self.avisos_de_vitoria,
            [],
            "empate nao tem vencedor para anunciar",
        )

    def test_partida_roda_mais_de_uma_jogada(self):
        resultado, _ = self.jogar(JOGADAS_EMPATE)
        preenchidas = [casa for casa in resultado["board"] if casa != VAZIO]
        self.assertEqual(
            len(preenchidas),
            9,
            "o grafo deve voltar para o proximo turno, nao terminar na 1a jogada",
        )

    def test_cada_ia_recebe_o_prompt_do_seu_lado(self):
        self.jogar(JOGADAS_EMPATE)
        prompts = [
            " ".join(getattr(msg, "content", str(msg)) for msg in prompt)
            for prompt in self.fake.prompts
        ]
        self.assertGreaterEqual(len(prompts), 2, "as duas IAs devem jogar")
        self.assertIn("as X", prompts[0], "a 1a jogada e de X")
        self.assertIn("as O", prompts[1], "a 2a jogada e de O")

    def test_modelos_escolhidos_sao_os_usados(self):
        self.respostas_modelo = ("1", "2")  # X = qwen3:4b-instruct, O = llama3.2:3b
        self.entradas = list(self.respostas_modelo)
        self.jogar(JOGADAS_EMPATE)
        self.assertGreaterEqual(len(self.fake.modelos_pedidos), 2)
        self.assertEqual(
            self.fake.modelos_pedidos[0],
            "qwen3:4b-instruct",
            "a primeira IA escolhida deve jogar de X",
        )
        self.assertEqual(
            self.fake.modelos_pedidos[1],
            "llama3.2:3b",
            "a segunda IA escolhida deve jogar de O",
        )

    def test_tabuleiro_de_entrada_nao_e_alterado(self):
        entrada = [VAZIO] * 9
        self.jogar(JOGADAS_EMPATE, tabuleiro=entrada)
        self.assertEqual(
            entrada,
            [VAZIO] * 9,
            "o estado recebido nao deve ser mutado no lugar; use uma copia do board",
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
