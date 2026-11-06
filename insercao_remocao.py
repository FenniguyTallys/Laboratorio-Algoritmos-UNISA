
import csv
import time
from pathlib import Path
from statistics import mean, stdev

import matplotlib.pyplot as plt


# ============================================================
# UNISA - LABORATÓRIO EXPERIMENTAL DE ALGORITMOS
# ETAPA: INSERÇÃO E REMOÇÃO
# BASE: 1.000 REGISTROS SINTÉTICOS
# ============================================================

PASTA = Path(__file__).resolve().parent
RESULTADOS = PASTA / "resultados"
RESULTADOS.mkdir(parents=True, exist_ok=True)

ARQUIVO = PASTA / "base_1000_desordenada.csv"

REPETICOES = 100
TOTAL = 1000


# ============================================================
# 1. LEITURA DOS DADOS
# ============================================================

def carregar_dados():
    with open(ARQUIVO, encoding="utf-8-sig", newline="") as f:
        leitor = csv.DictReader(f)

        if not leitor.fieldnames or "id_cliente" not in leitor.fieldnames:
            raise ValueError("Coluna id_cliente não encontrada.")

        dados = [int(linha["id_cliente"]) for linha in leitor]

    if len(dados) != TOTAL:
        raise ValueError(
            f"Esperados {TOTAL} registros, encontrados {len(dados)}."
        )

    if len(set(dados)) != len(dados):
        raise ValueError("Existem IDs duplicados.")

    return dados


# ============================================================
# 2. LISTA PYTHON
# ============================================================

def inserir_lista(lista, valor, posicao):
    # Número de elementos deslocados para a direita
    deslocamentos = len(lista) - posicao
    lista.insert(posicao, valor)
    return deslocamentos


def remover_lista(lista, posicao):
    # Número de elementos deslocados para a esquerda
    deslocamentos = len(lista) - posicao - 1
    lista.pop(posicao)
    return deslocamentos


# ============================================================
# 3. LISTA ENCADEADA
# ============================================================

class NoLista:
    def __init__(self, valor):
        self.valor = valor
        self.proximo = None


class ListaEncadeada:
    def __init__(self, valores=None):
        self.inicio = None
        self.tamanho = 0

        if valores is not None:
            ultimo = None

            for valor in valores:
                novo = NoLista(valor)

                if ultimo is None:
                    self.inicio = novo
                else:
                    ultimo.proximo = novo

                ultimo = novo
                self.tamanho += 1

    def inserir(self, posicao, valor):
        if not 0 <= posicao <= self.tamanho:
            raise IndexError("Posição inválida.")

        novo = NoLista(valor)
        visitas = 0

        if posicao == 0:
            novo.proximo = self.inicio
            self.inicio = novo
        else:
            atual = self.inicio
            visitas = 1

            for _ in range(posicao - 1):
                atual = atual.proximo
                visitas += 1

            novo.proximo = atual.proximo
            atual.proximo = novo

        self.tamanho += 1
        return visitas

    def remover(self, posicao):
        if not 0 <= posicao < self.tamanho:
            raise IndexError("Posição inválida.")

        visitas = 0

        if posicao == 0:
            self.inicio = self.inicio.proximo
        else:
            atual = self.inicio
            visitas = 1

            for _ in range(posicao - 1):
                atual = atual.proximo
                visitas += 1

            atual.proximo = atual.proximo.proximo

        self.tamanho -= 1
        return visitas


# ============================================================
# 4. ÁRVORE BINÁRIA DE BUSCA (BST)
# ============================================================

class NoArvore:
    def __init__(self, valor):
        self.valor = valor
        self.esquerda = None
        self.direita = None


class ArvoreBST:
    def __init__(self, valores=None):
        self.raiz = None

        if valores is not None:
            for valor in valores:
                self.inserir(valor)

    def inserir(self, valor):
        comparacoes = 0

        if self.raiz is None:
            self.raiz = NoArvore(valor)
            return comparacoes

        atual = self.raiz

        while True:
            comparacoes += 1

            if valor < atual.valor:
                if atual.esquerda is None:
                    atual.esquerda = NoArvore(valor)
                    break
                atual = atual.esquerda

            elif valor > atual.valor:
                if atual.direita is None:
                    atual.direita = NoArvore(valor)
                    break
                atual = atual.direita

            else:
                raise ValueError("ID duplicado na árvore.")

        return comparacoes

    def remover(self, valor):
        comparacoes = 0
        pai = None
        atual = self.raiz

        # Localiza o nó
        while atual is not None:
            comparacoes += 1

            if valor == atual.valor:
                break

            pai = atual

            if valor < atual.valor:
                atual = atual.esquerda
            else:
                atual = atual.direita

        if atual is None:
            raise ValueError("ID não encontrado na árvore.")

        # Caso com dois filhos:
        # substitui pelo sucessor em ordem
        if atual.esquerda is not None and atual.direita is not None:
            pai_sucessor = atual
            sucessor = atual.direita

            while sucessor.esquerda is not None:
                comparacoes += 1
                pai_sucessor = sucessor
                sucessor = sucessor.esquerda

            comparacoes += 1
            atual.valor = sucessor.valor

            pai = pai_sucessor
            atual = sucessor

        # Nó com zero ou um filho
        filho = (
            atual.esquerda
            if atual.esquerda is not None
            else atual.direita
        )

        if pai is None:
            self.raiz = filho
        elif pai.esquerda is atual:
            pai.esquerda = filho
        else:
            pai.direita = filho

        return comparacoes


# ============================================================
# 5. EXECUÇÃO DOS TESTES
# ============================================================

def medir_operacao(preparar, executar):
    tempos = []
    operacoes = []

    for _ in range(REPETICOES):
        # Preparação fora da medição
        estrutura = preparar()

        inicio = time.perf_counter_ns()
        quantidade = executar(estrutura)
        fim = time.perf_counter_ns()

        tempos.append((fim - inicio) / 1000)
        operacoes.append(quantidade)

    return {
        "tempo_us": mean(tempos),
        "desvio_us": stdev(tempos) if len(tempos) > 1 else 0,
        "operacoes": mean(operacoes)
    }


def executar_experimentos(dados):
    resultados = []

    novo_id = max(dados) + 1
    id_remocao = dados[len(dados) // 2]

    def registrar(estrutura, operacao, posicao, preparar, executar):
        resultado = medir_operacao(preparar, executar)

        linha = {
            "Estrutura": estrutura,
            "Operação": operacao,
            "Posição": posicao,
            "Tempo médio (us)": round(resultado["tempo_us"], 6),
            "Desvio padrão (us)": round(resultado["desvio_us"], 6),
            "Operações estruturais": round(resultado["operacoes"], 2),
            "Repetições": REPETICOES
        }

        resultados.append(linha)

        print(
            f"{estrutura:<17} | "
            f"{operacao:<8} | "
            f"{posicao:<8} | "
            f"{linha['Tempo médio (us)']:>12.4f} us | "
            f"Operações: {linha['Operações estruturais']:>8.0f}"
        )

    print("\n" + "=" * 90)
    print("UNISA - EXPERIMENTOS DE INSERÇÃO E REMOÇÃO")
    print("=" * 90)

    # LISTA PYTHON E LISTA ENCADEADA
    estruturas = {
        "Lista Python": lambda: dados.copy(),
        "Lista Encadeada": lambda: ListaEncadeada(dados)
    }

    for nome, preparar in estruturas.items():
        for operacao in ("Inserção", "Remoção"):
            for posicao_nome in ("Início", "Meio", "Fim"):

                if operacao == "Inserção":
                    indice = {
                        "Início": 0,
                        "Meio": len(dados) // 2,
                        "Fim": len(dados)
                    }[posicao_nome]
                else:
                    indice = {
                        "Início": 0,
                        "Meio": len(dados) // 2,
                        "Fim": len(dados) - 1
                    }[posicao_nome]

                if nome == "Lista Python":
                    if operacao == "Inserção":
                        executar = (
                            lambda lista, i=indice:
                            inserir_lista(lista, novo_id, i)
                        )
                    else:
                        executar = (
                            lambda lista, i=indice:
                            remover_lista(lista, i)
                        )
                else:
                    if operacao == "Inserção":
                        executar = (
                            lambda lista, i=indice:
                            lista.inserir(i, novo_id)
                        )
                    else:
                        executar = (
                            lambda lista, i=indice:
                            lista.remover(i)
                        )

                registrar(
                    nome,
                    operacao,
                    posicao_nome,
                    preparar,
                    executar
                )

    # ÁRVORE BINÁRIA
    registrar(
        "Árvore BST",
        "Inserção",
        "Por ID",
        lambda: ArvoreBST(dados),
        lambda arvore: arvore.inserir(novo_id)
    )

    registrar(
        "Árvore BST",
        "Remoção",
        "Por ID",
        lambda: ArvoreBST(dados),
        lambda arvore: arvore.remover(id_remocao)
    )

    return resultados


# ============================================================
# 6. EXPORTAÇÃO CSV
# ============================================================

def salvar_csv(resultados):
    destino = RESULTADOS / "comparacao_insercao_remocao.csv"

    with open(
        destino,
        "w",
        encoding="utf-8-sig",
        newline=""
    ) as arquivo:
        escritor = csv.DictWriter(
            arquivo,
            fieldnames=list(resultados[0].keys()),
            delimiter=";"
        )

        escritor.writeheader()
        escritor.writerows(resultados)

    print(f"\nRelatório salvo: {destino}")


# ============================================================
# 7. GRÁFICOS
# ============================================================

def gerar_graficos(resultados):
    for operacao in ("Inserção", "Remoção"):
        selecionados = [
            r for r in resultados
            if r["Operação"] == operacao
        ]

        rotulos = [
            f"{r['Estrutura']} - {r['Posição']}"
            for r in selecionados
        ]

        tempos = [
            r["Tempo médio (us)"]
            for r in selecionados
        ]

        fig, ax = plt.subplots(figsize=(12, 7))

        ax.barh(rotulos, tempos, color="#163C69")
        ax.invert_yaxis()

        ax.set_xlabel("Tempo médio (microssegundos)")
        ax.set_title(
            f"Comparação de {operacao} - 1.000 Registros"
        )

        ax.grid(axis="x", alpha=0.2)

        fig.tight_layout()

        nome = (
            "grafico_insercao.png"
            if operacao == "Inserção"
            else "grafico_remocao.png"
        )

        destino = RESULTADOS / nome
        fig.savefig(destino, dpi=200)
        plt.close(fig)

        print(f"Gráfico gerado: {destino}")


# ============================================================
# 8. PROGRAMA PRINCIPAL
# ============================================================

def main():
    try:
        dados = carregar_dados()

        print(f"Registros carregados: {len(dados)}")
        print(f"Repetições por teste: {REPETICOES}")
        print("Unidade de tempo: microssegundos (us)")

        resultados = executar_experimentos(dados)

        salvar_csv(resultados)
        gerar_graficos(resultados)

        print("\n" + "=" * 90)
        print("EXPERIMENTOS CONCLUÍDOS COM SUCESSO!")
        print("=" * 90)

    except (
        FileNotFoundError,
        ValueError,
        RuntimeError
    ) as erro:
        print(f"\nERRO: {erro}")


if __name__ == "__main__":
    main()
