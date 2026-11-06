# Laboratório Experimental de Algoritmos com Dados Sintéticos

**Instituição:** Universidade Santo Amaro (UNISA)  
**Aluno:** Fenniguy Tallys — RA 5622743  
**Ano:** 2026

## 1. Apresentação

Este projeto realiza experimentos de desempenho com algoritmos de **busca, ordenação, inserção e remoção** em bases de dados sintéticas com **1.000, 10.000 e 100.000 registros**. O objetivo é comparar tempos de execução e contagens de operações, considerando o tamanho e a organização dos dados.

## 2. Origem e características dos dados

A base inicial de 1.000 registros foi obtida com o **Mockaroo**. As bases maiores foram **ampliadas sinteticamente a partir da base inicial**, por meio do script de geração; portanto, **não são exportações independentes do Mockaroo**.

Cada registro contém: `id_cliente`, `nome`, `idade`, `cidade`, `estado`, `data_cadastro`, `numero_compras` e `valor_total`.

Para cada tamanho, são usadas duas versões: **ordenada** e **desordenada** pelo identificador do cliente (`id_cliente`). Os dados são artificiais e destinados a fins acadêmicos.

## 3. Organização dos arquivos

```text
Projeto_Mockaroo/
├── MOCK_DATA.csv                 # base original de 1.000 registros
├── gerar_bases.py                # prepara os seis arquivos de entrada
├── laboratorio_completo.py       # executa o experimento completo
├── main.py                       # módulo complementar de buscas, se incluído
├── ordenacao.py                  # módulo complementar de ordenação, se incluído
├── insercao_remocao.py           # módulo complementar de estruturas, se incluído
├── dados/
│   ├── base_1000_ordenada.csv
│   ├── base_1000_desordenada.csv
│   ├── base_10000_ordenada.csv
│   ├── base_10000_desordenada.csv
│   ├── base_100000_ordenada.csv
│   └── base_100000_desordenada.csv
├── resultados/
│   └── laboratorio_completo/
│       ├── buscas.csv
│       ├── ordenacao.csv
│       ├── insercao_remocao.csv
│       ├── ordenacao_ordenada.png
│       ├── ordenacao_desordenada.png
│       ├── insercao.png
│       └── remocao.png
└── README.md
```

**Observação:** o relatório acadêmico em PDF e o gráfico adicional `buscas.png`, quando fornecidos, podem ficar na pasta de entrega final. Os módulos complementares só devem ser incluídos se estiverem presentes e forem parte da entrega.

## 4. Requisitos

- Python 3 instalado (recomendado: Python 3.10 ou superior).
- PyCharm, VS Code ou terminal do sistema.
- Biblioteca externa `matplotlib`, necessária para gerar os gráficos.
- Bibliotecas `csv`, `pathlib`, `multiprocessing`, `random`, `statistics` e `time` fazem parte da biblioteca padrão do Python.

Instale a dependência no terminal do ambiente Python usado pelo projeto:

```bash
python -m pip install matplotlib
```

No Windows, se `python` não for reconhecido, tente `py -m pip install matplotlib`.

## 5. Como executar

1. Extraia a pasta do projeto, mantendo os arquivos e subpastas juntos.
2. Abra a pasta `Projeto_Mockaroo` no PyCharm.
3. Confirme que `MOCK_DATA.csv` e `gerar_bases.py` estão disponíveis, caso seja necessário recriar as bases.
4. Se os seis CSVs já estiverem na pasta `dados/`, **não é necessário gerar novamente**. Caso contrário, execute:

   ```bash
   python gerar_bases.py
   ```

5. Execute o laboratório:

   ```bash
   python laboratorio_completo.py
   ```

6. Aguarde a mensagem `FINALIZADO!` e, no PyCharm, `Process finished with exit code 0`.
7. Consulte os CSVs e gráficos em `resultados/laboratorio_completo/`.

**Importante para Windows:** execute o arquivo principal diretamente; o script usa processos separados para limitar o tempo dos testes de ordenação. Evite iniciar a execução a partir de um console interativo que não suporte adequadamente `multiprocessing`.

## 6. Algoritmos avaliados

### Busca

- Busca linear iterativa;
- Busca linear recursiva;
- Busca binária iterativa;
- Busca binária recursiva.

A busca binária pressupõe dados ordenados. O relatório de busca registra o caso testado, se o alvo foi encontrado, a quantidade de comparações e o tempo médio em microssegundos (`µs`).

### Ordenação

- Bubble Sort;
- Selection Sort;
- Insertion Sort;
- Shell Sort;
- Merge Sort;
- Quick Sort;
- Heap Sort.

São avaliadas bases ordenadas e desordenadas. O Quick Sort utiliza pivô final, que pode produzir desempenho quadrático em dados já ordenados.

### Inserção e remoção

São comparadas operações em lista Python, lista encadeada e árvore binária de busca (BST), conforme as posições e operações definidas no experimento. As contagens de operações possuem significados próprios para cada estrutura e não devem ser comparadas diretamente sem considerar a coluna `unidade`.

## 7. Protocolo experimental

- Tamanhos: **1.000, 10.000 e 100.000 registros**.
- Ordenação: **3 repetições** por cenário, quando a execução é permitida e concluída.
- Inserção e remoção: **15 repetições** por cenário.
- Limite de ordenação: **3 segundos por execução**.
- Os tempos são medidos no computador que executa o programa e podem variar conforme hardware, sistema operacional e carga de processamento.

Os arquivos de resultados distinguem os seguintes estados:

| Status | Significado |
|---|---|
| `OK` | Execução concluída e tempo registrado. |
| `TEMPO_EXCEDIDO` | A execução ultrapassou o limite de 3 segundos. |
| `NAO_EXECUTADO_CUSTO_QUADRATICO` | Teste preventivamente dispensado devido ao custo computacional esperado. |
| `NAO_EXECUTADO_PIOR_CASO_PIVO_FINAL` | Teste dispensado para evitar o pior caso do Quick Sort com pivô final. |

**Não trate valores vazios de tempo como zero.** Eles indicam que não há medição válida naquele cenário.

## 8. Arquivos de saída

| Arquivo | Conteúdo |
|---|---|
| `buscas.csv` | Algoritmo, caso, comparações, sucesso e tempo médio de busca (`µs`). |
| `ordenacao.csv` | Algoritmo, base, status, repetições válidas, tempo médio (`ms`), comparações e movimentações. |
| `insercao_remocao.csv` | Estrutura, operação, posição, tempo médio (`µs`), operações, unidade e repetições. |
| `ordenacao_ordenada.png` | Comparação de ordenação nas bases ordenadas. |
| `ordenacao_desordenada.png` | Comparação de ordenação nas bases desordenadas. |
| `insercao.png` | Comparação das operações de inserção. |
| `remocao.png` | Comparação das operações de remoção. |

Os CSVs de resultados utilizam **ponto e vírgula (`;`) como separador** e codificação UTF-8 com BOM, facilitando a abertura no Excel.

## 9. Interpretação dos resultados

Os experimentos permitem verificar que a escolha do algoritmo depende do volume de registros e da organização prévia da entrada. Algoritmos quadráticos podem se tornar inviáveis para bases maiores. Os resultados medidos devem ser interpretados em conjunto com a complexidade teórica e com as restrições do protocolo.

As conclusões se aplicam às implementações e ao ambiente utilizados; não representam uma comparação universal entre todas as versões possíveis desses algoritmos.

## 10. Entregáveis acadêmicos

A entrega final deve conter:

1. **Código-fonte:** scripts Python utilizados.
2. **Bases CSV:** seis arquivos ordenados e desordenados, além da base original quando solicitada.
3. **Resultados CSV:** os três relatórios gerados pelo laboratório.
4. **Gráficos:** imagens de apoio à análise.
5. **README:** este documento com instruções de execução.
6. **Relatório PDF:** fundamentação, metodologia, resultados, discussão e conclusão.

---

**Projeto acadêmico — UNISA, 2026.**
