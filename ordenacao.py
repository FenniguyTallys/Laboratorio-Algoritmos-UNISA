
import csv
import time
from pathlib import Path
from statistics import mean, stdev

import matplotlib.pyplot as plt


# ============================================================
# UNISA
# LABORATÓRIO EXPERIMENTAL DE ALGORITMOS
# COM DADOS SINTÉTICOS
#
# Experimento: 1.000 registros do Mockaroo
# ============================================================

PASTA_PROJETO = Path(__file__).resolve().parent
PASTA_RESULTADOS = PASTA_PROJETO / "resultados"

PASTA_RESULTADOS.mkdir(parents=True, exist_ok=True)

ARQUIVOS = {
    "Ordenada": PASTA_PROJETO / "base_1000_ordenada.csv",
    "Desordenada": PASTA_PROJETO / "base_1000_desordenada.csv"
}

COLUNA_ID = "id_cliente"
TOTAL_REGISTROS = 1000
REPETICOES = 5


# ============================================================
# 1. CARREGAMENTO DOS ARQUIVOS CSV
# ============================================================

def carregar_dados(caminho):

    if not caminho.exists():
        raise FileNotFoundError(
            f"Arquivo não encontrado: {caminho}"
        )

    with open(
        caminho,
        mode="r",
        encoding="utf-8-sig",
        newline=""
    ) as arquivo:

        leitor = csv.DictReader(arquivo)

        colunas = leitor.fieldnames or []

        coluna_encontrada = next(
            (
                coluna for coluna in colunas
                if coluna.strip().lower() == COLUNA_ID
            ),
            None
        )

        if coluna_encontrada is None:
            raise ValueError(
                f"Coluna '{COLUNA_ID}' não encontrada "
                f"em {caminho.name}.\n"
                f"Colunas disponíveis: {colunas}"
            )

        dados = []

        for numero_linha, registro in enumerate(leitor, 2):

            try:
                identificador = int(
                    registro[coluna_encontrada]
                )

            except (ValueError, TypeError) as erro:
                raise ValueError(
                    f"ID inválido na linha {numero_linha} "
                    f"do arquivo {caminho.name}"
                ) from erro

            dados.append(identificador)

    if len(dados) != TOTAL_REGISTROS:
        raise ValueError(
            f"{caminho.name} contém {len(dados)} registros. "
            f"Esperados: {TOTAL_REGISTROS}."
        )

    if len(set(dados)) != len(dados):
        raise ValueError(
            f"Existem IDs duplicados em {caminho.name}."
        )

    return dados


# ============================================================
# 2. BUBBLE SORT
# ============================================================

def bubble_sort(v):

    comparacoes = 0
    movimentacoes = 0

    n = len(v)

    for i in range(n):

        houve_troca = False

        for j in range(n - i - 1):

            comparacoes += 1

            if v[j] > v[j + 1]:

                v[j], v[j + 1] = v[j + 1], v[j]

                movimentacoes += 2
                houve_troca = True

        if not houve_troca:
            break

    return comparacoes, movimentacoes


# ============================================================
# 3. SELECTION SORT
# ============================================================

def selection_sort(v):

    comparacoes = 0
    movimentacoes = 0

    n = len(v)

    for i in range(n):

        indice_menor = i

        for j in range(i + 1, n):

            comparacoes += 1

            if v[j] < v[indice_menor]:
                indice_menor = j

        if indice_menor != i:

            v[i], v[indice_menor] = (
                v[indice_menor],
                v[i]
            )

            movimentacoes += 2

    return comparacoes, movimentacoes


# ============================================================
# 4. INSERTION SORT
# ============================================================

def insertion_sort(v):

    comparacoes = 0
    movimentacoes = 0

    for i in range(1, len(v)):

        chave = v[i]
        j = i - 1

        while j >= 0:

            comparacoes += 1

            if v[j] > chave:

                v[j + 1] = v[j]
                movimentacoes += 1

                j -= 1

            else:
                break

        v[j + 1] = chave
        movimentacoes += 1

    return comparacoes, movimentacoes


# ============================================================
# 5. SHELL SORT
# ============================================================

def shell_sort(v):

    comparacoes = 0
    movimentacoes = 0

    intervalo = len(v) // 2

    while intervalo > 0:

        for i in range(intervalo, len(v)):

            temporario = v[i]
            j = i

            while j >= intervalo:

                comparacoes += 1

                if v[j - intervalo] > temporario:

                    v[j] = v[j - intervalo]
                    movimentacoes += 1

                    j -= intervalo

                else:
                    break

            v[j] = temporario
            movimentacoes += 1

        intervalo //= 2

    return comparacoes, movimentacoes


# ============================================================
# 6. MERGE SORT
# ============================================================

def merge_sort(v):

    comparacoes = 0
    movimentacoes = 0

    def ordenar(inicio, fim):

        nonlocal comparacoes, movimentacoes

        if fim - inicio <= 1:
            return

        meio = (inicio + fim) // 2

        ordenar(inicio, meio)
        ordenar(meio, fim)

        esquerda = v[inicio:meio]
        direita = v[meio:fim]

        i = 0
        j = 0
        k = inicio

        while i < len(esquerda) and j < len(direita):

            comparacoes += 1

            if esquerda[i] <= direita[j]:

                v[k] = esquerda[i]
                i += 1

            else:

                v[k] = direita[j]
                j += 1

            movimentacoes += 1
            k += 1

        while i < len(esquerda):

            v[k] = esquerda[i]

            movimentacoes += 1
            i += 1
            k += 1

        while j < len(direita):

            v[k] = direita[j]

            movimentacoes += 1
            j += 1
            k += 1

    ordenar(0, len(v))

    return comparacoes, movimentacoes


# ============================================================
# 7. QUICK SORT
# ============================================================

def quick_sort(v):

    comparacoes = 0
    movimentacoes = 0

    def particionar(inicio, fim):

        nonlocal comparacoes, movimentacoes

        pivo = v[fim]
        i = inicio - 1

        for j in range(inicio, fim):

            comparacoes += 1

            if v[j] <= pivo:

                i += 1

                if i != j:

                    v[i], v[j] = v[j], v[i]
                    movimentacoes += 2

        if i + 1 != fim:

            v[i + 1], v[fim] = v[fim], v[i + 1]
            movimentacoes += 2

        return i + 1

    # Pilha para evitar problemas com limite de recursão
    pilha = [(0, len(v) - 1)]

    while pilha:

        inicio, fim = pilha.pop()

        if inicio >= fim:
            continue

        indice_pivo = particionar(inicio, fim)

        pilha.append((inicio, indice_pivo - 1))
        pilha.append((indice_pivo + 1, fim))

    return comparacoes, movimentacoes


# ============================================================
# 8. HEAP SORT
# ============================================================

def heap_sort(v):

    comparacoes = 0
    movimentacoes = 0

    def heapify(n, i):

        nonlocal comparacoes, movimentacoes

        while True:

            maior = i
            esquerda = 2 * i + 1
            direita = 2 * i + 2

            if esquerda < n:

                comparacoes += 1

                if v[esquerda] > v[maior]:
                    maior = esquerda

            if direita < n:

                comparacoes += 1

                if v[direita] > v[maior]:
                    maior = direita

            if maior == i:
                break

            v[i], v[maior] = v[maior], v[i]
            movimentacoes += 2

            i = maior

    n = len(v)

    for i in range(n // 2 - 1, -1, -1):
        heapify(n, i)

    for i in range(n - 1, 0, -1):

        v[0], v[i] = v[i], v[0]
        movimentacoes += 2

        heapify(i, 0)

    return comparacoes, movimentacoes


# ============================================================
# 9. LISTA DOS ALGORITMOS
# ============================================================

ALGORITMOS = {
    "Bubble Sort": bubble_sort,
    "Selection Sort": selection_sort,
    "Insertion Sort": insertion_sort,
    "Shell Sort": shell_sort,
    "Merge Sort": merge_sort,
    "Quick Sort": quick_sort,
    "Heap Sort": heap_sort
}


# ============================================================
# 10. EXECUÇÃO DOS EXPERIMENTOS
# ============================================================

def executar_experimentos():

    resultados = []
    bases_carregadas = {}

    for nome_base, caminho in ARQUIVOS.items():
        bases_carregadas[nome_base] = carregar_dados(caminho)

    # Verifica se ambas possuem os mesmos IDs
    if sorted(bases_carregadas["Ordenada"]) != sorted(
        bases_carregadas["Desordenada"]
    ):
        raise ValueError(
            "As duas bases não possuem o mesmo conjunto de IDs."
        )

    if bases_carregadas["Ordenada"] != sorted(
        bases_carregadas["Ordenada"]
    ):
        raise ValueError(
            "A base identificada como ordenada não está "
            "em ordem crescente de ID."
        )

    print("\n" + "=" * 85)
    print("UNISA - LABORATÓRIO EXPERIMENTAL DE ALGORITMOS")
    print("=" * 85)
    print(f"Registros por base: {TOTAL_REGISTROS}")
    print(f"Algoritmos: {len(ALGORITMOS)}")
    print(f"Repetições: {REPETICOES}")
    print("Critério de ordenação: id_cliente")
    print("=" * 85)

    for nome_base, dados in bases_carregadas.items():

        print("\n" + "-" * 85)
        print(f"BASE: {nome_base.upper()}")
        print("-" * 85)

        referencia = sorted(dados)

        for nome_algoritmo, funcao in ALGORITMOS.items():

            tempos = []
            comparacoes = 0
            movimentacoes = 0

            for repeticao in range(REPETICOES):

                copia = dados.copy()

                inicio = time.perf_counter()

                comp, mov = funcao(copia)

                fim = time.perf_counter()

                if copia != referencia:
                    raise RuntimeError(
                        f"Falha: {nome_algoritmo} "
                        f"na base {nome_base}."
                    )

                tempo_ms = (fim - inicio) * 1000

                tempos.append(tempo_ms)

                if repeticao == 0:
                    comparacoes = comp
                    movimentacoes = mov

                elif (
                    comparacoes != comp
                    or movimentacoes != mov
                ):
                    raise RuntimeError(
                        f"Contagens inconsistentes: {nome_algoritmo}"
                    )

            tempo_medio = mean(tempos)
            desvio = stdev(tempos) if len(tempos) > 1 else 0

            resultado = {
                "Base": nome_base,
                "Algoritmo": nome_algoritmo,
                "Registros": len(dados),
                "Tempo médio (ms)": round(tempo_medio, 6),
                "Desvio padrão (ms)": round(desvio, 6),
                "Comparações": comparacoes,
                "Movimentações": movimentacoes,
                "Execuções": REPETICOES
            }

            resultados.append(resultado)

            print(
                f"{nome_algoritmo:<18} | "
                f"Tempo: {tempo_medio:>11.6f} ms | "
                f"Comp: {comparacoes:>8} | "
                f"Mov: {movimentacoes:>8}"
            )

    return resultados


# ============================================================
# 11. SALVAR RESULTADOS EM CSV
# ============================================================

def salvar_resultados(resultados):

    destino = PASTA_RESULTADOS / "comparacao_algoritmos.csv"

    with open(
        destino,
        mode="w",
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

    print(f"\nRelatório CSV: {destino}")


# ============================================================
# 12. GERAR GRÁFICOS COMPARATIVOS
# ============================================================

def gerar_grafico(resultados, campo, titulo, nome_arquivo):

    nomes = list(ALGORITMOS.keys())

    valores_ordenada = []
    valores_desordenada = []

    for nome in nomes:

        for resultado in resultados:

            if resultado["Algoritmo"] != nome:
                continue

            if resultado["Base"] == "Ordenada":
                valores_ordenada.append(resultado[campo])

            elif resultado["Base"] == "Desordenada":
                valores_desordenada.append(resultado[campo])

    posicoes = list(range(len(nomes)))
    largura = 0.35

    fig, ax = plt.subplots(figsize=(12, 7))

    ax.barh(
        [p - largura / 2 for p in posicoes],
        valores_ordenada,
        height=largura,
        label="Base ordenada",
        color="#163C69"
    )

    ax.barh(
        [p + largura / 2 for p in posicoes],
        valores_desordenada,
        height=largura,
        label="Base desordenada",
        color="#E69F00"
    )

    ax.set_yticks(posicoes)
    ax.set_yticklabels(nomes)

    ax.invert_yaxis()

    ax.set_xlabel(campo)
    ax.set_title(titulo)

    ax.legend()
    ax.grid(axis="x", alpha=0.2)

    fig.tight_layout()

    destino = PASTA_RESULTADOS / nome_arquivo

    fig.savefig(destino, dpi=200)
    plt.close(fig)

    print(f"Gráfico gerado: {destino}")


# ============================================================
# 13. RESUMO FINAL
# ============================================================

def mostrar_resumo(resultados):

    print("\n" + "=" * 85)
    print("RESUMO DOS EXPERIMENTOS")
    print("=" * 85)

    for base in ARQUIVOS:

        dados_base = [
            r for r in resultados
            if r["Base"] == base
        ]

        mais_rapido = min(
            dados_base,
            key=lambda r: r["Tempo médio (ms)"]
        )

        menos_comparacoes = min(
            dados_base,
            key=lambda r: r["Comparações"]
        )

        print(f"\nBase: {base}")

        print(
            "Menor tempo médio: "
            f"{mais_rapido['Algoritmo']} "
            f"({mais_rapido['Tempo médio (ms)']:.6f} ms)"
        )

        print(
            "Menor número de comparações: "
            f"{menos_comparacoes['Algoritmo']} "
            f"({menos_comparacoes['Comparações']})"
        )


# ============================================================
# 14. PROGRAMA PRINCIPAL
# ============================================================

def main():

    try:

        resultados = executar_experimentos()

        salvar_resultados(resultados)

        gerar_grafico(
            resultados,
            "Tempo médio (ms)",
            "Comparação dos Tempos de Execução - 1.000 Registros",
            "grafico_tempos.png"
        )

        gerar_grafico(
            resultados,
            "Comparações",
            "Comparação do Número de Comparações",
            "grafico_comparacoes.png"
        )

        gerar_grafico(
            resultados,
            "Movimentações",
            "Comparação das Movimentações",
            "grafico_movimentacoes.png"
        )

        mostrar_resumo(resultados)

        print("\n" + "=" * 85)
        print("EXPERIMENTOS FINALIZADOS COM SUCESSO!")
        print("=" * 85)

    except (
        FileNotFoundError,
        ValueError,
        RuntimeError
    ) as erro:

        print(f"\nERRO: {erro}")


if __name__ == "__main__":
    main()
