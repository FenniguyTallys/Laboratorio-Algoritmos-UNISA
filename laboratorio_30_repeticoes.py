"""UNISA — laboratório experimental com bases de 1 mil, 10 mil e 100 mil.
Execute: python laboratorio_completo.py
Dependência para gráficos: python -m pip install matplotlib
"""
import csv
import platform
import sys
import os
import multiprocessing as mp
import random
import statistics
import time
from pathlib import Path

BASE = Path(__file__).resolve().parent
DADOS = BASE / 'dados'
SAIDA = BASE / 'resultados' / 'laboratorio_30_repeticoes'
TAMANHOS = (1000, 10000, 100000)
REPETICOES_ORDENACAO = 30
REPETICOES_ESTRUTURAS = 30
LIMITE_SEGUNDOS = 3.0  # por execução de ordenação
ALGORITMOS = ('Bubble', 'Selection', 'Insertion', 'Shell', 'Merge', 'Quick', 'Heap')
CAMPOS = ['id_cliente', 'nome', 'idade', 'cidade', 'estado', 'data_cadastro', 'numero_compras', 'valor_total']


def ler_ids(n, tipo):
    caminho = DADOS / f'base_{n}_{tipo}.csv'
    if not caminho.is_file():
        raise FileNotFoundError(f'Arquivo ausente: {caminho}\nExecute gerar_bases.py primeiro.')
    with caminho.open('r', encoding='utf-8-sig', newline='') as f:
        leitor = csv.DictReader(f)
        if leitor.fieldnames != CAMPOS:
            raise ValueError(f'Colunas inesperadas em {caminho.name}: {leitor.fieldnames}')
        ids = [int(linha['id_cliente']) for linha in leitor]
    if len(ids) != n or len(set(ids)) != n:
        raise ValueError(f'Quantidade ou IDs duplicados em {caminho.name}')
    if tipo == 'ordenada' and ids != sorted(ids):
        raise ValueError(f'Arquivo não ordenado: {caminho.name}')
    if tipo == 'desordenada' and ids == sorted(ids):
        raise ValueError(f'Arquivo não está desordenado: {caminho.name}')
    return ids


def salvar_csv(nome, linhas, colunas):
    caminho = SAIDA / nome
    with caminho.open('w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=colunas, delimiter=';')
        writer.writeheader()
        writer.writerows(linhas)
    print('CSV:', caminho)


# BUSCAS: comparação = teste de igualdade do ID

def busca_linear(a, alvo):
    c = 0
    for i, x in enumerate(a):
        c += 1
        if x == alvo:
            return i, c
    return -1, c


def busca_linear_rec(a, alvo):
    # Recursão em metades para não exceder o limite de recursão em 100 mil.
    c = 0
    def procurar(lo, hi):
        nonlocal c
        if lo >= hi:
            return -1
        if hi - lo == 1:
            c += 1
            return lo if a[lo] == alvo else -1
        meio = (lo + hi) // 2
        esquerda = procurar(lo, meio)
        return esquerda if esquerda != -1 else procurar(meio, hi)
    return procurar(0, len(a)), c


def busca_binaria(a, alvo):
    lo, hi, c = 0, len(a) - 1, 0
    while lo <= hi:
        m = (lo + hi) // 2
        c += 1
        if a[m] == alvo:
            return m, c
        if a[m] < alvo:
            lo = m + 1
        else:
            hi = m - 1
    return -1, c


def busca_binaria_rec(a, alvo):
    c = 0
    def procurar(lo, hi):
        nonlocal c
        if lo > hi:
            return -1
        m = (lo + hi) // 2
        c += 1
        if a[m] == alvo:
            return m
        if a[m] < alvo:
            return procurar(m + 1, hi)
        return procurar(lo, m - 1)
    return procurar(0, len(a) - 1), c


def testes_busca(bases):
    print('\n=== BUSCAS ===')
    linhas = []
    for n in TAMANHOS:
        ord_, des = bases[n]['ordenada'], bases[n]['desordenada']
        alvos = {'primeiro': ord_[0], 'central': ord_[n // 2], 'ultimo': ord_[-1], 'ausente': max(ord_) + 1}
        for tipo, a in [('desordenada', des), ('ordenada', ord_)]:
            metodos = [('Linear', busca_linear), ('Linear recursiva', busca_linear_rec)]
            if tipo == 'ordenada':
                metodos += [('Binaria', busca_binaria), ('Binaria recursiva', busca_binaria_rec)]
            for nome, func in metodos:
                for caso, alvo in alvos.items():
                    tempos = []
                    for _ in range(30):
                        ini = time.perf_counter_ns()
                        pos, comp = func(a, alvo)
                        tempos.append((time.perf_counter_ns() - ini) / 1_000)
                    if (pos >= 0) != (caso != 'ausente') or (pos >= 0 and a[pos] != alvo):
                        raise AssertionError(f'Busca incorreta: {nome}, {n}, {caso}')
                    linhas.append(dict(registros=n, base=tipo, algoritmo=nome, caso=caso,
                                       encontrado='sim' if pos >= 0 else 'nao', comparacoes=comp,
                                       tempo_medio_us=round(statistics.mean(tempos), 4),
                                       tempo_mediana_us=round(statistics.median(tempos), 4),
                                       tempo_desvio_padrao_us=round(statistics.stdev(tempos), 4), repeticoes=30))
        print(f'Buscas concluídas: {n:,}')
    salvar_csv('buscas.csv', linhas, ['registros', 'base', 'algoritmo', 'caso', 'encontrado', 'comparacoes', 'tempo_medio_us', 'tempo_mediana_us', 'tempo_desvio_padrao_us', 'repeticoes'])
    return linhas


# ORDENAÇÃO: comparações entre chaves; movimentações = atribuições ao vetor principal
# (para Merge, escrita no vetor principal; alocações auxiliares não contabilizadas).

def ordenar(nome, valores):
    a = valores.copy()
    comp = mov = 0
    n = len(a)
    if nome == 'Bubble':
        for fim in range(n - 1, 0, -1):
            trocou = False
            for j in range(fim):
                comp += 1
                if a[j] > a[j + 1]:
                    a[j], a[j + 1] = a[j + 1], a[j]
                    mov += 2
                    trocou = True
            if not trocou:
                break
    elif nome == 'Selection':
        for i in range(n - 1):
            minimo = i
            for j in range(i + 1, n):
                comp += 1
                if a[j] < a[minimo]:
                    minimo = j
            if minimo != i:
                a[i], a[minimo] = a[minimo], a[i]
                mov += 2
    elif nome == 'Insertion':
        for i in range(1, n):
            chave = a[i]
            j = i - 1
            while j >= 0:
                comp += 1
                if a[j] <= chave:
                    break
                a[j + 1] = a[j]
                mov += 1
                j -= 1
            a[j + 1] = chave
            mov += 1
    elif nome == 'Shell':
        gap = n // 2
        while gap > 0:
            for i in range(gap, n):
                chave = a[i]
                j = i
                while j >= gap:
                    comp += 1
                    if a[j - gap] <= chave:
                        break
                    a[j] = a[j - gap]
                    mov += 1
                    j -= gap
                a[j] = chave
                mov += 1
            gap //= 2
    elif nome == 'Merge':
        aux = [0] * n
        largura = 1
        while largura < n:
            for ini in range(0, n, 2 * largura):
                meio = min(ini + largura, n)
                fim = min(ini + 2 * largura, n)
                i, j, k = ini, meio, ini
                while i < meio and j < fim:
                    comp += 1
                    if a[i] <= a[j]:
                        aux[k] = a[i]
                        i += 1
                    else:
                        aux[k] = a[j]
                        j += 1
                    k += 1
                while i < meio:
                    aux[k] = a[i]
                    i += 1
                    k += 1
                while j < fim:
                    aux[k] = a[j]
                    j += 1
                    k += 1
                for k in range(ini, fim):
                    a[k] = aux[k]
                    mov += 1
            largura *= 2
    elif nome == 'Quick':
        # Pivô final intencional: permite observar o pior caso em base ordenada.
        pilha = [(0, n - 1)]
        while pilha:
            lo, hi = pilha.pop()
            if lo >= hi:
                continue
            pivo = a[hi]
            i = lo
            for j in range(lo, hi):
                comp += 1
                if a[j] <= pivo:
                    if i != j:
                        a[i], a[j] = a[j], a[i]
                        mov += 2
                    i += 1
            if i != hi:
                a[i], a[hi] = a[hi], a[i]
                mov += 2
            # Iterativo para evitar RecursionError.
            pilha.append((lo, i - 1))
            pilha.append((i + 1, hi))
    elif nome == 'Heap':
        def descer(raiz, fim):
            nonlocal comp, mov
            while True:
                filho = 2 * raiz + 1
                if filho >= fim:
                    return
                if filho + 1 < fim:
                    comp += 1
                    if a[filho] < a[filho + 1]:
                        filho += 1
                comp += 1
                if a[raiz] >= a[filho]:
                    return
                a[raiz], a[filho] = a[filho], a[raiz]
                mov += 2
                raiz = filho
        for raiz in range(n // 2 - 1, -1, -1):
            descer(raiz, n)
        for fim in range(n - 1, 0, -1):
            a[0], a[fim] = a[fim], a[0]
            mov += 2
            descer(0, fim)
    else:
        raise ValueError(nome)
    if a != sorted(valores):
        raise AssertionError(f'Ordenação incorreta: {nome}')
    return comp, mov


def worker_ordenacao(fila, nome, valores):
    try:
        inicio = time.perf_counter_ns()
        comp, mov = ordenar(nome, valores)
        ms = (time.perf_counter_ns() - inicio) / 1_000_000
        fila.put(('ok', ms, comp, mov))
    except Exception as exc:
        fila.put(('erro', str(exc), 0, 0))


def executar_ordenacao_com_limite(ctx, nome, valores):
    fila = ctx.Queue()
    proc = ctx.Process(target=worker_ordenacao, args=(fila, nome, valores))
    proc.start()
    proc.join(LIMITE_SEGUNDOS)
    if proc.is_alive():
        proc.terminate()
        proc.join()
        fila.close()
        fila.join_thread()
        return 'TEMPO_EXCEDIDO', None
    try:
        resultado = fila.get(timeout=1)
    except Exception:
        resultado = ('erro', 'Processo terminou sem resultado', 0, 0)
    fila.close()
    fila.join_thread()
    if resultado[0] != 'ok':
        return 'ERRO: ' + str(resultado[1]), None
    return 'OK', resultado[1:]


def testes_ordenacao(bases):
    print('\n=== ORDENAÇÃO (limite de 3 segundos por execução) ===')
    ctx = mp.get_context('spawn')  # compatível com Windows / PyCharm
    linhas = []
    for n in TAMANHOS:
        for tipo in ('ordenada', 'desordenada'):
            valores = bases[n][tipo]
            for nome in ALGORITMOS:
                # Não iniciar testes quadraticamente proibitivos em 100 mil.
                if n == 100000 and nome in ('Bubble', 'Selection', 'Insertion'):
                    status = 'NAO_EXECUTADO_CUSTO_QUADRATICO'
                    tempos = []
                    comp = mov = ''
                elif n == 100000 and tipo == 'ordenada' and nome == 'Quick':
                    status = 'NAO_EXECUTADO_PIOR_CASO_PIVO_FINAL'
                    tempos = []
                    comp = mov = ''
                else:
                    tempos = []
                    comp = mov = ''
                    status = 'OK'
                    for _ in range(REPETICOES_ORDENACAO):
                        status, resultado = executar_ordenacao_com_limite(ctx, nome, valores)
                        if status != 'OK':
                            break
                        ms, comp, mov = resultado
                        tempos.append(ms)
                # Se não concluiu todas as repetições, não apresentar média parcial.
                media = round(statistics.mean(tempos), 5) if status == 'OK' and len(tempos) == REPETICOES_ORDENACAO else ''
                mediana = round(statistics.median(tempos), 5) if media != '' else ''
                desvio = round(statistics.stdev(tempos), 5) if media != '' else ''
                linhas.append(dict(registros=n, base=tipo, algoritmo=nome, status=status,
                                   repeticoes_validas=len(tempos), tempo_medio_ms=media,
                                   tempo_mediana_ms=mediana, tempo_desvio_padrao_ms=desvio,
                                   comparacoes=comp if media != '' else '', movimentacoes=mov if media != '' else ''))
                print(f'{n:>6} | {tipo:<12} | {nome:<10} | {status:<37} | {str(media):>10} ms')
    salvar_csv('ordenacao.csv', linhas, ['registros', 'base', 'algoritmo', 'status', 'repeticoes_validas', 'tempo_medio_ms', 'tempo_mediana_ms', 'tempo_desvio_padrao_ms', 'comparacoes', 'movimentacoes'])
    return linhas


# ESTRUTURAS: preparação fora da medição; lista encadeada sem ponteiro de cauda.
class No:
    __slots__ = ('valor', 'proximo')
    def __init__(self, valor, proximo=None):
        self.valor = valor
        self.proximo = proximo


class Encadeada:
    def __init__(self, dados):
        self.inicio = None
        ultimo = None
        for x in dados:
            novo = No(x)
            if ultimo is None:
                self.inicio = novo
            else:
                ultimo.proximo = novo
            ultimo = novo
        self.tamanho = len(dados)

    def inserir(self, indice, valor):
        visitas = 0
        if indice == 0:
            self.inicio = No(valor, self.inicio)
        else:
            atual = self.inicio
            visitas = 1
            for _ in range(indice - 1):
                atual = atual.proximo
                visitas += 1
            atual.proximo = No(valor, atual.proximo)
        self.tamanho += 1
        return visitas

    def remover(self, indice):
        visitas = 0
        if indice == 0:
            self.inicio = self.inicio.proximo
        else:
            atual = self.inicio
            visitas = 1
            for _ in range(indice - 1):
                atual = atual.proximo
                visitas += 1
            atual.proximo = atual.proximo.proximo
        self.tamanho -= 1
        return visitas


class NoBST:
    __slots__ = ('valor', 'esq', 'dir')
    def __init__(self, valor):
        self.valor = valor
        self.esq = None
        self.dir = None


class BST:
    def __init__(self, dados):
        self.raiz = None
        for x in dados:
            self.inserir(x)

    def inserir(self, x):
        c = 0
        if self.raiz is None:
            self.raiz = NoBST(x)
            return c
        atual = self.raiz
        while True:
            c += 1
            if x < atual.valor:
                if atual.esq is None:
                    atual.esq = NoBST(x)
                    return c
                atual = atual.esq
            elif x > atual.valor:
                if atual.dir is None:
                    atual.dir = NoBST(x)
                    return c
                atual = atual.dir
            else:
                raise ValueError('ID duplicado')

    def remover(self, x):
        pai, atual, c = None, self.raiz, 0
        while atual is not None:
            c += 1
            if x == atual.valor:
                break
            pai = atual
            atual = atual.esq if x < atual.valor else atual.dir
        if atual is None:
            raise ValueError('ID ausente')
        if atual.esq is not None and atual.dir is not None:
            pai_sucessor, sucessor = atual, atual.dir
            c += 1
            while sucessor.esq is not None:
                pai_sucessor, sucessor = sucessor, sucessor.esq
                c += 1
            atual.valor = sucessor.valor
            pai, atual = pai_sucessor, sucessor
        filho = atual.esq if atual.esq is not None else atual.dir
        if pai is None:
            self.raiz = filho
        elif pai.esq is atual:
            pai.esq = filho
        else:
            pai.dir = filho
        return c


def teste_individual_estrutura(preparar, executar):
    tempos = []
    operacoes = []
    for _ in range(REPETICOES_ESTRUTURAS):
        estrutura = preparar()
        ini = time.perf_counter_ns()
        ops = executar(estrutura)
        tempos.append((time.perf_counter_ns() - ini) / 1000)
        operacoes.append(ops)
    return (round(statistics.mean(tempos), 5), round(statistics.median(tempos), 5),
            round(statistics.stdev(tempos), 5), round(statistics.mean(operacoes), 2))


def testes_estruturas(bases):
    print('\n=== INSERÇÃO E REMOÇÃO ===')
    linhas = []
    for n in TAMANHOS:
        dados = bases[n]['desordenada']
        novo = max(dados) + 1
        alvo = dados[n // 2]
        for estrutura in ('Lista Python', 'Lista encadeada'):
            preparar = (lambda d=dados: d.copy()) if estrutura == 'Lista Python' else (lambda d=dados: Encadeada(d))
            for operacao in ('Insercao', 'Remocao'):
                for posicao in ('Inicio', 'Meio', 'Fim'):
                    idx = {'Inicio': 0, 'Meio': n // 2, 'Fim': n if operacao == 'Insercao' else n - 1}[posicao]
                    if estrutura == 'Lista Python':
                        if operacao == 'Insercao':
                            def executar(a, i=idx, x=novo):
                                desloc = len(a) - i
                                a.insert(i, x)
                                return desloc
                        else:
                            def executar(a, i=idx):
                                desloc = len(a) - i - 1
                                a.pop(i)
                                return desloc
                        unidade = 'deslocamentos'
                    else:
                        if operacao == 'Insercao':
                            executar = lambda a, i=idx, x=novo: a.inserir(i, x)
                        else:
                            executar = lambda a, i=idx: a.remover(i)
                        unidade = 'visitas_a_nos'
                    tempo, mediana, desvio, ops = teste_individual_estrutura(preparar, executar)
                    linhas.append(dict(registros=n, estrutura=estrutura, operacao=operacao, posicao=posicao,
                                       tempo_medio_us=tempo, tempo_mediana_us=mediana,
                                       tempo_desvio_padrao_us=desvio, operacoes=ops, unidade=unidade, repeticoes=REPETICOES_ESTRUTURAS))
        for operacao in ('Insercao', 'Remocao'):
            executar = (lambda a, x=novo: a.inserir(x)) if operacao == 'Insercao' else (lambda a, x=alvo: a.remover(x))
            tempo, mediana, desvio, ops = teste_individual_estrutura(lambda d=dados: BST(d), executar)
            linhas.append(dict(registros=n, estrutura='Arvore BST', operacao=operacao, posicao='Por ID',
                               tempo_medio_us=tempo, tempo_mediana_us=mediana,
                                       tempo_desvio_padrao_us=desvio, operacoes=ops, unidade='comparacoes', repeticoes=REPETICOES_ESTRUTURAS))
        print(f'Estruturas concluídas: {n:,}')
    salvar_csv('insercao_remocao.csv', linhas, ['registros', 'estrutura', 'operacao', 'posicao', 'tempo_medio_us', 'tempo_mediana_us', 'tempo_desvio_padrao_us', 'operacoes', 'unidade', 'repeticoes'])
    return linhas


def gerar_graficos(ordenacao, estruturas):
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
    except ImportError:
        print('Gráficos não gerados: instale matplotlib com: python -m pip install matplotlib')
        return
    for tipo in ('ordenada', 'desordenada'):
        fig, ax = plt.subplots(figsize=(11, 6))
        for nome in ALGORITMOS:
            pontos = [r for r in ordenacao if r['base'] == tipo and r['algoritmo'] == nome and r['status'] == 'OK']
            if pontos:
                ax.plot([r['registros'] for r in pontos], [r['tempo_medio_ms'] for r in pontos], marker='o', label=nome)
        ax.set_xscale('log')
        ax.set_yscale('log')
        ax.set_xticks(TAMANHOS, ['1.000', '10.000', '100.000'])
        ax.set_xlabel('Registros')
        ax.set_ylabel('Tempo médio (ms, escala log)')
        ax.set_title('Ordenação - base ' + tipo + ' (somente testes concluídos)')
        ax.grid(True, alpha=.25)
        ax.legend()
        fig.tight_layout()
        caminho = SAIDA / f'ordenacao_{tipo}.png'
        fig.savefig(caminho, dpi=180)
        plt.close(fig)
        print('Gráfico:', caminho)
    for op in ('Insercao', 'Remocao'):
        fig, ax = plt.subplots(figsize=(11, 6))
        grupos = sorted(set((r['estrutura'], r['posicao']) for r in estruturas if r['operacao'] == op))
        for estrutura, posicao in grupos:
            pontos = [r for r in estruturas if r['operacao'] == op and r['estrutura'] == estrutura and r['posicao'] == posicao]
            ax.plot([r['registros'] for r in pontos], [r['tempo_medio_us'] for r in pontos], marker='o', label=f'{estrutura} - {posicao}')
        ax.set_xscale('log')
        ax.set_yscale('log')
        ax.set_xticks(TAMANHOS, ['1.000', '10.000', '100.000'])
        ax.set_xlabel('Registros')
        ax.set_ylabel('Tempo médio (microssegundos, escala log)')
        ax.set_title(op + ' - comparação por volume')
        ax.grid(True, alpha=.25)
        ax.legend(fontsize=8)
        fig.tight_layout()
        caminho = SAIDA / f'{op.lower()}.png'
        fig.savefig(caminho, dpi=180)
        plt.close(fig)
        print('Gráfico:', caminho)


def registrar_ambiente():
    """Registra características do ambiente; RAM pode ficar indisponível."""
    ram = 'nao_identificada'
    if sys.platform == 'win32':
        try:
            import ctypes
            class MEMORYSTATUSEX(ctypes.Structure):
                _fields_ = [('dwLength', ctypes.c_ulong), ('dwMemoryLoad', ctypes.c_ulong),
                            ('ullTotalPhys', ctypes.c_ulonglong), ('ullAvailPhys', ctypes.c_ulonglong),
                            ('ullTotalPageFile', ctypes.c_ulonglong), ('ullAvailPageFile', ctypes.c_ulonglong),
                            ('ullTotalVirtual', ctypes.c_ulonglong), ('ullAvailVirtual', ctypes.c_ulonglong),
                            ('ullAvailExtendedVirtual', ctypes.c_ulonglong)]
            estado = MEMORYSTATUSEX()
            estado.dwLength = ctypes.sizeof(estado)
            if ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(estado)):
                ram = f'{estado.ullTotalPhys / (1024 ** 3):.2f} GB'
        except Exception:
            pass
    ambiente = {
        'sistema_operacional': platform.platform(),
        'processador': platform.processor() or 'nao_identificado',
        'nucleos_logicos': os.cpu_count(),
        'ram_total': ram,
        'python': sys.version.split()[0],
        'interpretador': sys.executable,
        'ide': 'PyCharm (confirmar versao manualmente)',
        'repeticoes_por_cenario': 30,
        'limite_por_execucao_ordenacao_segundos': LIMITE_SEGUNDOS,
        'nota': 'Tempo total inclui leitura, preparacao, exportacao e graficos; nao equivale ao tempo dos algoritmos.'
    }
    salvar_csv('ambiente.csv', [{'item': k, 'valor': v} for k, v in ambiente.items()], ['item', 'valor'])
    for k, v in ambiente.items():
        print(f'{k}: {v}')


def main():
    SAIDA.mkdir(parents=True, exist_ok=True)
    inicio_total = time.perf_counter()
    registrar_ambiente()
    print('=' * 70)
    print('UNISA — LABORATÓRIO COMPLETO: 1.000 / 10.000 / 100.000')
    print('=' * 70)
    bases = {}
    for n in TAMANHOS:
        bases[n] = {tipo: ler_ids(n, tipo) for tipo in ('ordenada', 'desordenada')}
        if set(bases[n]['ordenada']) != set(bases[n]['desordenada']):
            raise ValueError(f'Bases de {n} não têm os mesmos IDs')
        print(f'Bases de {n:,} verificadas.')
    testes_busca(bases)
    ordenacao = testes_ordenacao(bases)
    estruturas = testes_estruturas(bases)
    gerar_graficos(ordenacao, estruturas)
    print('\n' + '=' * 70)
    total = time.perf_counter() - inicio_total
    salvar_csv('tempo_total.csv', [{'tempo_total_segundos': round(total, 4)}], ['tempo_total_segundos'])
    print(f'Tempo total do laboratorio: {total:.2f} segundos')
    print('FINALIZADO! Resultados em:', SAIDA)
    print('Status NAO_EXECUTADO e TEMPO_EXCEDIDO são dados válidos do protocolo, não erros.')
    print('=' * 70)


if __name__ == '__main__':
    mp.freeze_support()
    main()
