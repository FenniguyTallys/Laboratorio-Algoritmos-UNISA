Laboratório Experimental de Algoritmos com Dados Sintéticos
Instituição: Universidade Santo Amaro (UNISA)  
Autor: Fenniguy Tallys Barros — RA 5622743  
Curso: Análise e Desenvolvimento de Sistemas — 4º semestre  
Disciplina: Técnicas de Programação  
Ano: 2026
1. Apresentação
Este projeto realiza experimentos de desempenho com algoritmos de busca, ordenação, inserção e remoção em bases de dados sintéticas com 1.000, 10.000 e 100.000 registros. O objetivo é comparar tempos de execução e contagens de operações, considerando o tamanho e a organização dos dados.
2. Origem e características dos dados
A base inicial de 1.000 registros foi obtida com o Mockaroo. As bases maiores foram ampliadas sinteticamente a partir da base inicial, por meio do script de geração; portanto, não são exportações independentes do Mockaroo.
Cada registro contém: `id_cliente`, `nome`, `idade`, `cidade`, `estado`, `data_cadastro`, `numero_compras` e `valor_total`.
Para cada tamanho, são usadas duas versões: ordenada e desordenada pelo identificador do cliente (`id_cliente`). Os dados são artificiais e destinados a fins acadêmicos.
3. Organização dos arquivos
```text
Laboratorio-Algoritmos-UNISA-main/
├── MOCK_DATA.csv
├── gerar_bases.py
├── laboratorio_30_repeticoes.py   # experimento do relatório final
├── laboratorio_completo.py       # execução complementar anterior
├── main.py
├── ordenacao.py
├── insercao_remocao.py
├── dados/                         # seis bases ordenadas e desordenadas
├── resultados/
│   ├── laboratorio_30_repeticoes/
│   │   ├── ambiente.csv
│   │   ├── buscas.csv
│   │   ├── ordenacao.csv
│   │   ├── insercao_remocao.csv
│   │   ├── tempo_total.csv
│   │   ├── ordenacao_ordenada.png
│   │   ├── ordenacao_desordenada.png
│   │   ├── insercao.png
│   │   └── remocao.png
│   └── laboratorio_completo/      # resultados de execução complementar
└── README.md
```
O relatório acadêmico em PDF é entregue separadamente, caso não esteja publicado no repositório.
4. Requisitos
Python 3 instalado (recomendado: Python 3.10 ou superior).
PyCharm, VS Code ou terminal do sistema.
Biblioteca externa `matplotlib`, necessária para gerar os gráficos.
Bibliotecas `csv`, `pathlib`, `multiprocessing`, `random`, `statistics` e `time` fazem parte da biblioteca padrão do Python.
Instale a dependência no terminal do ambiente Python usado pelo projeto:
```bash
python -m pip install matplotlib
```
No Windows, se `python` não for reconhecido, tente `py -m pip install matplotlib`.
5. Como executar
Baixe o repositório em Code → Download ZIP, extraia-o e abra a pasta extraída no PyCharm ou terminal.
Instale a dependência: `python -m pip install matplotlib` (no Windows, também pode usar `py -m pip install matplotlib`).
As seis bases já estão em `dados/`. Não é necessário recriá-las para reproduzir a análise publicada. Caso precise gerar novas bases, execute `python gerar_bases.py`; isso pode produzir dados e medições diferentes.
Para executar o experimento correspondente ao relatório acadêmico final, execute:
```bash
   python laboratorio_30_repeticoes.py
   ```
Consulte os resultados em `resultados/laboratorio_30_repeticoes/`. Os CSVs e gráficos já publicados documentam a execução original; uma nova execução pode apresentar tempos diferentes.
Execução complementar: `python laboratorio_completo.py` gera resultados na pasta `resultados/laboratorio_completo/`, mas não é o protocolo de 30 repetições usado nas tabelas do PDF.
Windows: execute os scripts como arquivos Python, não por um console interativo incompatível com `multiprocessing`, pois os testes de ordenação utilizam processos separados para impor o limite de tempo.
6. Algoritmos avaliados
Busca
Busca linear iterativa;
Busca linear recursiva;
Busca binária iterativa;
Busca binária recursiva.
A busca binária pressupõe dados ordenados. O relatório de busca registra o caso testado, se o alvo foi encontrado, a quantidade de comparações e o tempo médio em microssegundos (`µs`).
Ordenação
Bubble Sort;
Selection Sort;
Insertion Sort;
Shell Sort;
Merge Sort;
Quick Sort;
Heap Sort.
São avaliadas bases ordenadas e desordenadas. O Quick Sort utiliza pivô final, que pode produzir desempenho quadrático em dados já ordenados.
Inserção e remoção
São comparadas operações em lista Python, lista encadeada e árvore binária de busca (BST), conforme as posições e operações definidas no experimento. As contagens de operações possuem significados próprios para cada estrutura e não devem ser comparadas diretamente sem considerar a coluna `unidade`.
7. Protocolo experimental do relatório final
Tamanhos de entrada: 1.000, 10.000 e 100.000 registros, em versões ordenadas e desordenadas.
30 repetições por cenário concluído de busca, ordenação, inserção e remoção.
Buscas: alvos primeiro, central, último e ausente; busca binária somente nas bases ordenadas.
Ordenação: limite de 3 segundos por execução; alguns cenários de custo elevado são excluídos preventivamente.
Estatísticas: média, mediana e desvio padrão dos tempos válidos.
Tempos de busca, inserção e remoção em microssegundos (µs); ordenação em milissegundos (ms).
A construção das estruturas não integra o tempo de uma operação isolada de inserção ou remoção.
Os contadores de operações dependem da estrutura e não são diretamente comparáveis entre estruturas diferentes.
A RAM total do computador foi registrada, mas o consumo de memória por algoritmo não foi medido.
Status	Significado
`OK`	Cenário concluído com medições válidas.
`TEMPO_EXCEDIDO`	Execução ultrapassou o limite de 3 segundos.
`NAO_EXECUTADO_CUSTO_QUADRATICO`	Cenário excluído preventivamente pelo custo esperado.
`NAO_EXECUTADO_PIOR_CASO_PIVO_FINAL`	Cenário excluído pelo pior caso esperado do Quick Sort com pivô final.
Importante: valores de tempo ausentes não representam tempo zero. Os limites e exclusões não devem ser usados como medidas de velocidade.
8. Arquivos de saída do experimento final
Todos os arquivos abaixo estão em `resultados/laboratorio_30_repeticoes/`:
Arquivo	Conteúdo
`ambiente.csv`	Sistema operacional, processador, memória e configuração experimental.
`buscas.csv`	Resultados de busca e estatísticas dos tempos.
`ordenacao.csv`	Tempos, contagens de operações e status por algoritmo e cenário.
`insercao_remocao.csv`	Medições por estrutura, operação e posição.
`tempo_total.csv`	Duração total da execução do laboratório.
`ordenacao_ordenada.png`	Gráfico de ordenação em bases ordenadas.
`ordenacao_desordenada.png`	Gráfico de ordenação em bases desordenadas.
`insercao.png`	Gráfico de inserção.
`remocao.png`	Gráfico de remoção.
Os CSVs usam ponto e vírgula (`;`) como separador. O tempo total inclui leitura, preparação, medições, exportação e gráficos, e não representa o tempo de um algoritmo isolado.
9. Interpretação dos resultados
Os experimentos permitem verificar que a escolha do algoritmo depende do volume de registros e da organização prévia da entrada. Algoritmos quadráticos podem se tornar inviáveis para bases maiores. Os resultados medidos devem ser interpretados em conjunto com a complexidade teórica e com as restrições do protocolo.
As conclusões se aplicam às implementações e ao ambiente utilizados; não representam uma comparação universal entre todas as versões possíveis desses algoritmos.
Resultados de referência do relatório (execução publicada)
Cenário	Resultado
Busca linear por ID ausente, 100.000 registros ordenados	100.000 comparações
Busca binária por ID ausente, 100.000 registros ordenados	17 comparações
Quick Sort, 100.000 registros desordenados	média de 268,947 ms
Shell Sort, 100.000 registros ordenados	média de 225,690 ms
Tempo total do laboratório	285,93 s
Esses valores descrevem a execução documentada; tempos podem variar em outras máquinas ou novas execuções. Não há algoritmo universalmente mais eficiente: o resultado depende da organização dos dados, do tamanho da entrada, da operação e da implementação.
10. Entregáveis acadêmicos
A entrega final deve conter:
Código-fonte: scripts Python utilizados.
Bases CSV: seis arquivos ordenados e desordenados, além da base original quando solicitada.
Resultados CSV: buscas, ordenação, inserção/remoção, ambiente e tempo total do protocolo de 30 repetições.
Gráficos: imagens de apoio à análise.
README: este documento com instruções de execução.
Relatório PDF: fundamentação, metodologia, resultados, discussão e conclusão.
---
Projeto acadêmico — UNISA, 2026.
