
import csv
import random
import re
from pathlib import Path
from datetime import datetime, timedelta
from collections import Counter


# ============================================================
# UNISA - LABORATÓRIO EXPERIMENTAL DE ALGORITMOS
# GERAÇÃO DE BASES SINTÉTICAS
#
# Quantidades: 1.000, 10.000 e 100.000 registros
# Origem: arquivo MOCK_DATA.csv
# Linguagem: Python
# ============================================================

PASTA_PROJETO = Path(__file__).resolve().parent
PASTA_DADOS = PASTA_PROJETO / "dados"

ARQUIVO_ORIGINAL = PASTA_PROJETO / "MOCK_DATA.csv"

QUANTIDADES = [1000, 10000, 100000]

SEMENTE = 2026

CAMPOS = [
    "id_cliente",
    "nome",
    "idade",
    "cidade",
    "estado",
    "data_cadastro",
    "numero_compras",
    "valor_total"
]


# ============================================================
# 1. LEITURA DO ARQUIVO MOCKAROO
# ============================================================

def carregar_csv():

    if not ARQUIVO_ORIGINAL.exists():
        raise FileNotFoundError(
            f"Arquivo não encontrado:\n{ARQUIVO_ORIGINAL}"
        )

    with open(
        ARQUIVO_ORIGINAL,
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as arquivo:

        amostra = arquivo.read(4096)
        arquivo.seek(0)

        try:
            dialeto = csv.Sniffer().sniff(
                amostra,
                delimiters=",;"
            )
            delimitador = dialeto.delimiter

        except csv.Error:
            delimitador = ","

        leitor = csv.DictReader(
            arquivo,
            delimiter=delimitador
        )

        colunas = leitor.fieldnames or []

        faltando = [
            campo for campo in CAMPOS
            if campo not in colunas
        ]

        if faltando:
            raise ValueError(
                "Campos ausentes no CSV: "
                + ", ".join(faltando)
            )

        registros = []

        for numero, linha in enumerate(leitor, start=2):

            try:
                id_cliente = int(linha["id_cliente"])
                idade = int(linha["idade"])
                compras = int(linha["numero_compras"])

                valor = converter_valor(
                    linha["valor_total"]
                )

                data = converter_data(
                    linha["data_cadastro"]
                )

            except (ValueError, TypeError) as erro:
                raise ValueError(
                    f"Erro na linha {numero}: {erro}"
                ) from erro

            registros.append({
                "id_cliente": id_cliente,
                "nome": linha["nome"],
                "idade": idade,
                "cidade": linha["cidade"],
                "estado": linha["estado"],
                "data_cadastro": data,
                "numero_compras": compras,
                "valor_total": valor
            })

    if len(registros) != 1000:
        raise ValueError(
            "A base original precisa conter "
            "exatamente 1.000 registros. "
            f"Encontrados: {len(registros)}"
        )

    ids = [r["id_cliente"] for r in registros]

    if len(ids) != len(set(ids)):
        raise ValueError(
            "O arquivo original possui IDs duplicados."
        )

    return registros


# ============================================================
# 2. CONVERSÃO DOS VALORES
# ============================================================

def converter_valor(texto):

    texto = str(texto).strip()

    texto = re.sub(
        r"[^\d,.\-]",
        "",
        texto
    )

    if not texto:
        raise ValueError("Valor monetário vazio.")

    if "," in texto and "." in texto:

        if texto.rfind(",") > texto.rfind("."):
            texto = texto.replace(".", "")
            texto = texto.replace(",", ".")

        else:
            texto = texto.replace(",", "")

    elif "," in texto:
        texto = texto.replace(",", ".")

    return round(float(texto), 2)


def converter_data(texto):

    texto = str(texto).strip()

    formatos = [
        "%Y-%m-%d",
        "%d/%m/%Y",
        "%Y-%m-%d %H:%M:%S",
        "%m/%d/%Y"
    ]

    for formato in formatos:

        try:
            data = datetime.strptime(
                texto,
                formato
            )

            return data.strftime("%Y-%m-%d")

        except ValueError:
            continue

    raise ValueError(
        f"Formato de data não reconhecido: {texto}"
    )


# ============================================================
# 3. GERAÇÃO DOS REGISTROS
# ============================================================

def gerar_registros(base_original, quantidade, rng):

    # Mantém os registros originais dentro da nova base.
    registros = [
        registro.copy()
        for registro in base_original
    ]

    ids_existentes = {
        r["id_cliente"]
        for r in registros
    }

    proximo_id = max(ids_existentes) + 1

    # Combinações observadas na base original.
    localidades = [
        (r["cidade"], r["estado"])
        for r in base_original
    ]

    nomes = [
        r["nome"]
        for r in base_original
    ]

    idades = [
        r["idade"]
        for r in base_original
    ]

    compras_base = [
        r["numero_compras"]
        for r in base_original
    ]

    valores_base = [
        r["valor_total"]
        for r in base_original
    ]

    datas_base = [
        datetime.strptime(
            r["data_cadastro"],
            "%Y-%m-%d"
        )
        for r in base_original
    ]

    while len(registros) < quantidade:

        # Gera ID único e sequencial.
        novo_id = proximo_id
        proximo_id += 1

        nome = rng.choice(nomes)
        idade = rng.choice(idades)

        cidade, estado = rng.choice(localidades)

        numero_compras = rng.choice(compras_base)

        # Valor sintético com variação de até 15%.
        valor_referencia = rng.choice(valores_base)

        fator = rng.uniform(0.85, 1.15)

        valor_total = round(
            max(0, valor_referencia * fator),
            2
        )

        # Data baseada nas datas observadas.
        data_referencia = rng.choice(datas_base)

        variacao_dias = rng.randint(-30, 30)

        nova_data = (
            data_referencia
            + timedelta(days=variacao_dias)
        )

        registro = {
            "id_cliente": novo_id,
            "nome": nome,
            "idade": idade,
            "cidade": cidade,
            "estado": estado,
            "data_cadastro": nova_data.strftime(
                "%Y-%m-%d"
            ),
            "numero_compras": numero_compras,
            "valor_total": valor_total
        }

        registros.append(registro)

    return registros


# ============================================================
# 4. EXPORTAÇÃO CSV
# ============================================================

def salvar_csv(caminho, registros):

    with open(
        caminho,
        "w",
        encoding="utf-8-sig",
        newline=""
    ) as arquivo:

        escritor = csv.DictWriter(
            arquivo,
            fieldnames=CAMPOS,
            delimiter=","
        )

        escritor.writeheader()

        for registro in registros:

            linha = registro.copy()

            linha["valor_total"] = (
                f"{registro['valor_total']:.2f}"
            )

            escritor.writerow(linha)


# ============================================================
# 5. VALIDAÇÃO
# ============================================================

def validar_base(registros, quantidade):

    if len(registros) != quantidade:
        raise ValueError(
            "Quantidade incorreta de registros."
        )

    ids = [
        r["id_cliente"]
        for r in registros
    ]

    if len(set(ids)) != quantidade:
        raise ValueError(
            "Foram encontrados IDs duplicados."
        )

    for registro in registros:

        if list(registro.keys()) != CAMPOS:
            raise ValueError(
                "Estrutura de campos inconsistente."
            )

    return True


def validar_arquivos(caminho, quantidade, ordenado):

    with open(
        caminho,
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as arquivo:

        leitor = csv.DictReader(arquivo)

        if leitor.fieldnames != CAMPOS:
            raise ValueError(
                f"Colunas incorretas: {caminho.name}"
            )

        ids = [
            int(linha["id_cliente"])
            for linha in leitor
        ]

    if len(ids) != quantidade:
        raise ValueError(
            f"Quantidade incorreta em {caminho.name}"
        )

    if len(set(ids)) != quantidade:
        raise ValueError(
            f"IDs duplicados em {caminho.name}"
        )

    if ordenado and ids != sorted(ids):
        raise ValueError(
            f"Arquivo não está ordenado: {caminho.name}"
        )

    if not ordenado and ids == sorted(ids):
        raise ValueError(
            f"Arquivo deveria estar desordenado: "
            f"{caminho.name}"
        )


# ============================================================
# 6. ESTATÍSTICAS
# ============================================================

def mostrar_estatisticas(registros):

    idades = [
        r["idade"]
        for r in registros
    ]

    valores = [
        r["valor_total"]
        for r in registros
    ]

    estados = Counter(
        r["estado"]
        for r in registros
    )

    print(
        f"Idade mínima: {min(idades)} | "
        f"Máxima: {max(idades)}"
    )

    print(
        f"Valor médio: R$ "
        f"{sum(valores) / len(valores):.2f}"
    )

    print(
        f"Estados diferentes: {len(estados)}"
    )


# ============================================================
# 7. PROGRAMA PRINCIPAL
# ============================================================

def main():

    print("=" * 72)
    print("UNISA - GERAÇÃO DE BASES SINTÉTICAS")
    print("=" * 72)

    print("\nCarregando arquivo original...")

    base_original = carregar_csv()

    print(
        f"Registros originais: {len(base_original)}"
    )

    PASTA_DADOS.mkdir(
        parents=True,
        exist_ok=True
    )

    rng = random.Random(SEMENTE)

    for quantidade in QUANTIDADES:

        print("\n" + "-" * 72)

        print(
            f"GERANDO BASE DE {quantidade:,} REGISTROS"
        )

        print("-" * 72)

        registros = gerar_registros(
            base_original,
            quantidade,
            rng
        )

        validar_base(
            registros,
            quantidade
        )

        # Base ordenada por id_cliente
        ordenada = sorted(
            registros,
            key=lambda r: r["id_cliente"]
        )

        # Base desordenada
        desordenada = registros.copy()

        rng.shuffle(desordenada)

        nome_ordenada = (
            f"base_{quantidade}_ordenada.csv"
        )

        nome_desordenada = (
            f"base_{quantidade}_desordenada.csv"
        )

        caminho_ordenada = (
            PASTA_DADOS / nome_ordenada
        )

        caminho_desordenada = (
            PASTA_DADOS / nome_desordenada
        )

        salvar_csv(
            caminho_ordenada,
            ordenada
        )

        salvar_csv(
            caminho_desordenada,
            desordenada
        )

        validar_arquivos(
            caminho_ordenada,
            quantidade,
            True
        )

        validar_arquivos(
            caminho_desordenada,
            quantidade,
            False
        )

        print("\nArquivos gerados:")

        print(f"  {nome_ordenada}")
        print(f"  {nome_desordenada}")

        print("\nEstatísticas:")

        mostrar_estatisticas(registros)

        print("\nValidação: OK")

    print("\n" + "=" * 72)
    print("TODAS AS BASES FORAM GERADAS COM SUCESSO!")
    print("=" * 72)

    print(
        f"\nPasta dos arquivos:\n{PASTA_DADOS}"
    )


if __name__ == "__main__":

    try:
        main()

    except (
        FileNotFoundError,
        ValueError,
        OSError
    ) as erro:

        print("\nERRO DURANTE A EXECUÇÃO:")
        print(erro)
        raise
