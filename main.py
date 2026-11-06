
import csv
import random
from pathlib import Path

# ==========================================
# PROJETO UNISA - TECNICAS DE PROGRAMACAO
# BASE DE 1.000 CLIENTES - MOCKAROO
# ==========================================

PASTA = Path(__file__).resolve().parent
ARQUIVO = PASTA / "MOCK_DATA.csv"


# 1. CARREGAR OS CLIENTES
def carregar_clientes():
    clientes = []

    with open(ARQUIVO, "r", encoding="utf-8-sig", newline="") as arquivo:
        leitor = csv.DictReader(arquivo)

        for linha in leitor:
            linha["id_cliente"] = int(linha["id_cliente"])
            clientes.append(linha)

    return clientes


# 2. SALVAR ARQUIVOS CSV
def salvar_csv(nome, clientes):
    with open(PASTA / nome, "w", encoding="utf-8-sig", newline="") as arquivo:
        escritor = csv.DictWriter(
            arquivo,
            fieldnames=clientes[0].keys()
        )
        escritor.writeheader()
        escritor.writerows(clientes)


# 3. CRIAR BASE ORDENADA E DESORDENADA
def preparar_bases(clientes):

    ordenada = sorted(
        clientes,
        key=lambda x: x["id_cliente"]
    )

    desordenada = clientes.copy()
    random.Random(42).shuffle(desordenada)

    salvar_csv("base_1000_ordenada.csv", ordenada)
    salvar_csv("base_1000_desordenada.csv", desordenada)

    return ordenada, desordenada


# 4. BUSCA LINEAR
def busca_linear(clientes, chave):
    comparacoes = 0

    for i in range(len(clientes)):
        comparacoes += 1

        if clientes[i]["id_cliente"] == chave:
            return i, comparacoes

    return -1, comparacoes


# 5. BUSCA LINEAR RECURSIVA
def busca_linear_recursiva(clientes, chave, indice=0, comparacoes=0):

    # Evita ultrapassar o limite de recursao
    if indice >= len(clientes):
        return -1, comparacoes

    comparacoes += 1

    if clientes[indice]["id_cliente"] == chave:
        return indice, comparacoes

    return busca_linear_recursiva(
        clientes, chave, indice + 1, comparacoes
    )


# 6. BUSCA BINARIA ITERATIVA
def busca_binaria(clientes, chave):
    inicio = 0
    fim = len(clientes) - 1
    comparacoes = 0

    while inicio <= fim:
        meio = (inicio + fim) // 2
        comparacoes += 1

        id_atual = clientes[meio]["id_cliente"]

        if id_atual == chave:
            return meio, comparacoes

        elif id_atual < chave:
            inicio = meio + 1

        else:
            fim = meio - 1

    return -1, comparacoes


# 7. BUSCA BINARIA RECURSIVA
def busca_binaria_recursiva(
    clientes, chave, inicio=0, fim=None, comparacoes=0
):
    if fim is None:
        fim = len(clientes) - 1

    if inicio > fim:
        return -1, comparacoes

    meio = (inicio + fim) // 2
    comparacoes += 1

    id_atual = clientes[meio]["id_cliente"]

    if id_atual == chave:
        return meio, comparacoes

    elif id_atual < chave:
        return busca_binaria_recursiva(
            clientes, chave, meio + 1, fim, comparacoes
        )

    else:
        return busca_binaria_recursiva(
            clientes, chave, inicio, meio - 1, comparacoes
        )


# 8. MOSTRAR RESULTADOS
def mostrar_resultado(nome, funcao, clientes, chave):
    posicao, comparacoes = funcao(clientes, chave)

    print(f"\n--- {nome} ---")
    print(f"Comparacoes: {comparacoes}")

    if posicao != -1:
        print(f"Posicao: {posicao}")
        print(f"ID: {clientes[posicao]['id_cliente']}")
        print(f"Nome: {clientes[posicao]['nome']}")
    else:
        print("Cliente nao encontrado!")


# 9. PROGRAMA PRINCIPAL
def main():

    clientes = carregar_clientes()

    print("===================================")
    print(" PROJETO MOCKAROO - UNISA")
    print("===================================")
    print(f"Total de clientes: {len(clientes)}")

    if len(clientes) != 1000:
        print("AVISO: A base deve conter 1.000 registros.")

    ids = [cliente["id_cliente"] for cliente in clientes]
    if len(ids) != len(set(ids)):
        raise ValueError("Existem IDs duplicados no CSV.")

    ordenada, desordenada = preparar_bases(clientes)

    print("\nArquivos gerados com sucesso!")
    print("base_1000_ordenada.csv")
    print("base_1000_desordenada.csv")

    while True:
        entrada = input(
            "\nDigite o ID do cliente (S para sair): "
        ).strip()

        if entrada.lower() == "s":
            print("Programa encerrado!")
            break

        try:
            chave = int(entrada)
        except ValueError:
            print("Digite um numero valido!")
            continue

        mostrar_resultado(
            "BUSCA LINEAR",
            busca_linear,
            desordenada,
            chave
        )

        mostrar_resultado(
            "BUSCA LINEAR RECURSIVA",
            busca_linear_recursiva,
            desordenada,
            chave
        )

        mostrar_resultado(
            "BUSCA BINARIA",
            busca_binaria,
            ordenada,
            chave
        )

        mostrar_resultado(
            "BUSCA BINARIA RECURSIVA",
            busca_binaria_recursiva,
            ordenada,
            chave
        )


if __name__ == "__main__":
    main()
