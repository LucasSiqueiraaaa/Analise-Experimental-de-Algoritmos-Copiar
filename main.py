import bisect
import csv
import platform
import random
import statistics
import sys
import time
from pathlib import Path

# Pastas do projeto
PASTA = Path(__file__).resolve().parent
DADOS = PASTA / "dados"
RESULTADOS = PASTA / "resultados"
GRAFICOS = PASTA / "graficos"
TAMANHOS = [1_000, 10_000, 100_000]
SEMENTE = 2026
# ALGORITMOS DE BUSCA
# As comparações contam comparações entre a chave pesquisada e um ID.
# Na busca binária, cada teste de igualdade ou de menor/maior é contado.

def busca_linear(lista, valor):
    comparacoes = 0
    for posicao, item in enumerate(lista):
        comparacoes += 1
        if item == valor:
            return posicao, comparacoes
    return -1, comparacoes


def busca_linear_recursiva(lista, valor):
    # A busca percorre blocos para evitar ultrapassar o limite de recursão
    # do Python em bases de 100.000 itens
    tamanho_bloco = 500

    def buscar_bloco(inicio, comparacoes):
        fim = min(inicio + tamanho_bloco, len(lista))
        for posicao in range(inicio, fim):
            comparacoes += 1
            if lista[posicao] == valor:
                return posicao, comparacoes
        if fim >= len(lista):
            return -1, comparacoes
        return buscar_bloco(fim, comparacoes)

    return buscar_bloco(0, 0)


def busca_binaria(lista, valor):
    inicio, fim = 0, len(lista) - 1
    comparacoes = 0
    while inicio <= fim:
        meio = (inicio + fim) // 2
        comparacoes += 1
        if lista[meio] == valor:
            return meio, comparacoes
        comparacoes += 1
        if lista[meio] < valor:
            inicio = meio + 1
        else:
            fim = meio - 1
    return -1, comparacoes


def busca_binaria_recursiva(lista, valor):
    def buscar(inicio, fim, comparacoes):
        if inicio > fim:
            return -1, comparacoes
        meio = (inicio + fim) // 2
        comparacoes += 1
        if lista[meio] == valor:
            return meio, comparacoes
        comparacoes += 1
        if lista[meio] < valor:
            return buscar(meio + 1, fim, comparacoes)
        return buscar(inicio, meio - 1, comparacoes)

    return buscar(0, len(lista) - 1, 0)

# ALGORITMOS DE ORDENACAO


def bubble_sort(a):
    comparacoes = trocas = 0
    for fim in range(len(a) - 1, 0, -1):
        mudou = False
        for i in range(fim):
            comparacoes += 1
            if a[i] > a[i + 1]:
                a[i], a[i + 1] = a[i + 1], a[i]
                trocas += 1
                mudou = True
        if not mudou:
            break
    return comparacoes, trocas


def selection_sort(a):
    comparacoes = trocas = 0
    for i in range(len(a) - 1):
        menor = i
        for j in range(i + 1, len(a)):
            comparacoes += 1
            if a[j] < a[menor]:
                menor = j
        if menor != i:
            a[i], a[menor] = a[menor], a[i]
            trocas += 1
    return comparacoes, trocas


def insertion_sort(a):
    comparacoes = movimentos = 0
    for i in range(1, len(a)):
        atual = a[i]
        j = i - 1
        while j >= 0:
            comparacoes += 1
            if a[j] > atual:
                a[j + 1] = a[j]
                movimentos += 1
                j -= 1
            else:
                break
        a[j + 1] = atual
        movimentos += 1
    return comparacoes, movimentos


def shell_sort(a):
    comparacoes = movimentos = 0
    intervalo = len(a) // 2
    while intervalo > 0:
        for i in range(intervalo, len(a)):
            atual = a[i]
            j = i
            while j >= intervalo:
                comparacoes += 1
                if a[j - intervalo] > atual:
                    a[j] = a[j - intervalo]
                    movimentos += 1
                    j -= intervalo
                else:
                    break
            a[j] = atual
            movimentos += 1
        intervalo //= 2
    return comparacoes, movimentos


def merge_sort(a):
    def ordenar(v):
        if len(v) <= 1:
            return v, 0, 0
        meio = len(v) // 2
        esq, c1, m1 = ordenar(v[:meio])
        dir_, c2, m2 = ordenar(v[meio:])
        resultado = []
        i = j = comp = mov = 0
        while i < len(esq) and j < len(dir_):
            comp += 1
            if esq[i] <= dir_[j]:
                resultado.append(esq[i])
                i += 1
            else:
                resultado.append(dir_[j])
                j += 1
            mov += 1
        resultado.extend(esq[i:])
        resultado.extend(dir_[j:])
        mov += len(esq) - i + len(dir_) - j
        return resultado, c1 + c2 + comp, m1 + m2 + mov

    ordenado, comparacoes, movimentos = ordenar(a)
    a[:] = ordenado
    return comparacoes, movimentos


def quick_sort(a):
    comparacoes = movimentos = 0

    def ordenar(inicio, fim):
        nonlocal comparacoes, movimentos
        if inicio >= fim:
            return
        pivo = a[(inicio + fim) // 2]
        i, j = inicio, fim
        while i <= j:
            while i <= fim:
                comparacoes += 1
                if a[i] < pivo:
                    i += 1
                else:
                    break
            while j >= inicio:
                comparacoes += 1
                if a[j] > pivo:
                    j -= 1
                else:
                    break
            if i <= j:
                if i != j:
                    a[i], a[j] = a[j], a[i]
                    movimentos += 1
                i += 1
                j -= 1
        if inicio < j:
            ordenar(inicio, j)
        if i < fim:
            ordenar(i, fim)

    ordenar(0, len(a) - 1)
    return comparacoes, movimentos


def heap_sort(a):
    comparacoes = movimentos = 0

    def descer(n, i):
        nonlocal comparacoes, movimentos
        maior = i
        esq, dir_ = 2 * i + 1, 2 * i + 2
        if esq < n:
            comparacoes += 1
            if a[esq] > a[maior]:
                maior = esq
        if dir_ < n:
            comparacoes += 1
            if a[dir_] > a[maior]:
                maior = dir_
        if maior != i:
            a[i], a[maior] = a[maior], a[i]
            movimentos += 1
            descer(n, maior)

    n = len(a)
    for i in range(n // 2 - 1, -1, -1):
        descer(n, i)
    for fim in range(n - 1, 0, -1):
        a[0], a[fim] = a[fim], a[0]
        movimentos += 1
        descer(fim, 0)
    return comparacoes, movimentos

ORDENACOES = {
    "Bubble Sort": bubble_sort,
    "Selection Sort": selection_sort,
    "Insertion Sort": insertion_sort,
    "Shell Sort": shell_sort,
    "Merge Sort": merge_sort,
    "Quick Sort": quick_sort,
    "Heap Sort": heap_sort,
}
# DADOS: prioriza CSV exportado do Mockaroo
# Aceita clientes_1000.csv ou base_1000.csv como arquivo de origem
# Se nao encontrar, cria uma base sintetica com os oito campos pedidos
def localizar_base_original(tamanho):
    candidatos = [
        DADOS / f"base_{tamanho}.csv",
        PASTA / f"base_{tamanho}.csv",
    ]
    for caminho in candidatos:
        if caminho.exists():
            return caminho
    return None

def ler_clientes(caminho):
    with caminho.open(encoding="utf-8-sig", newline="") as arquivo:
        leitor = csv.DictReader(arquivo)
        if not leitor.fieldnames:
            raise ValueError(f"O arquivo {caminho.name} nao possui cabecalho.")
        campo_id = next(
            (campo for campo in leitor.fieldnames
             if campo.strip().lower() in ("id", "id_cliente", "idcliente")),
            None
        )
        if campo_id is None:
            raise ValueError(
                f"Coluna de ID nao encontrada em {caminho.name}. "
                "Use id_cliente, id ou idcliente."
            )
        linhas = list(leitor)
    if not linhas:
        raise ValueError(f"A base {caminho.name} esta vazia.")
    try:
        for linha in linhas:
            linha[campo_id] = str(int(float(linha[campo_id])))
    except (ValueError, TypeError):
        raise ValueError(f"A coluna {campo_id} precisa conter IDs numericos inteiros.")
    ids = [int(linha[campo_id]) for linha in linhas]
    if len(ids) != len(set(ids)):
        raise ValueError(f"Existem IDs repetidos em {caminho.name}.")
    return linhas, campo_id


def preparar_bases():
    DADOS.mkdir(parents=True, exist_ok=True)
    for tamanho in TAMANHOS:
        origem = localizar_base_original(tamanho)
        if origem is None:
            origem = DADOS / f"clientes_{tamanho}.csv"
            if not origem.exists():
                gerar_base_sintetica(origem, tamanho)
                print(f"Base sintetica criada: {origem.name}")
        linhas, campo_id = ler_clientes(origem)
        if len(linhas) != tamanho:
            print(
                f"ATENCAO: {origem.name} possui {len(linhas)} registros; "
                f"o esperado para esta base e {tamanho}."
            )

        ordenadas = sorted(linhas, key=lambda linha: int(linha[campo_id]))
        embaralhadas = linhas.copy()
        random.Random(SEMENTE + tamanho).shuffle(embaralhadas)

        campos = list(linhas[0].keys())
        for sufixo, conteudo in (
            ("ordenada", ordenadas),
            ("desordenada", embaralhadas),
        ):
            destino = DADOS / f"base_{tamanho}_{sufixo}.csv"
            with destino.open("w", newline="", encoding="utf-8-sig") as arquivo:
                escritor = csv.DictWriter(arquivo, fieldnames=campos)
                escritor.writeheader()
                escritor.writerows(conteudo)

        print(f"Base de {tamanho:,} registros preparada.".replace(",", "."))


def carregar_ids(caminho):
    linhas, campo_id = ler_clientes(caminho)
    return [int(linha[campo_id]) for linha in linhas]


def salvar_csv(nome, colunas, linhas):
    RESULTADOS.mkdir(parents=True, exist_ok=True)
    with (RESULTADOS / nome).open("w", newline="", encoding="utf-8-sig") as arquivo:
        escritor = csv.writer(arquivo)
        escritor.writerow(colunas)
        escritor.writerows(linhas)


def estatisticas(tempos):
    return (
        round(statistics.mean(tempos), 3),
        round(statistics.median(tempos), 3),
        round(statistics.stdev(tempos), 3) if len(tempos) > 1 else 0.0,
    )


# EXPERIMENTO 1, 2 E 3: BUSCAS, POSICOES E COMPARACOES

def testar_buscas(repeticoes):
    print("\nTestando algoritmos de busca...")
    saida = []
    algoritmos = [
        ("Busca Linear", busca_linear, False),
        ("Busca Linear Recursiva", busca_linear_recursiva, False),
        ("Busca Binaria", busca_binaria, True),
        ("Busca Binaria Recursiva", busca_binaria_recursiva, True),
    ]

    for n in TAMANHOS:
        ordenada = carregar_ids(DADOS / f"base_{n}_ordenada.csv")
        desordenada = carregar_ids(DADOS / f"base_{n}_desordenada.csv")
        for nome, funcao, exige_ordenacao in algoritmos:
            estados = [("ordenada", ordenada)] if exige_ordenacao else [
                ("desordenada", desordenada), ("ordenada", ordenada)
            ]
            for estado, lista in estados:
                pontos = [
                    ("inicio", 0),
                    ("25%", int((len(lista) - 1) * 0.25)),
                    ("meio", int((len(lista) - 1) * 0.50)),
                    ("75%", int((len(lista) - 1) * 0.75)),
                    ("final", len(lista) - 1),
                    ("nao encontrado", None),
                ]
                for posicao, indice in pontos:
                    chave = -1 if indice is None else lista[indice]
                    tempos = []
                    comparacoes = 0
                    encontrado = False
                    for _ in range(repeticoes):
                        inicio = time.perf_counter_ns()
                        resultado, comparacoes = funcao(lista, chave)
                        tempos.append(time.perf_counter_ns() - inicio)
                        encontrado = resultado >= 0
                    media, mediana, desvio = estatisticas(tempos)
                    saida.append([
                        nome, n, estado, posicao, media, mediana, desvio,
                        comparacoes, encontrado
                    ])
        print(f"  Busca: base {n:,} concluida.".replace(",", "."))

    salvar_csv(
        "resultados_busca.csv",
        ["algoritmo", "quantidade", "estado", "posicao",
         "tempo_medio_ns", "tempo_mediano_ns", "desvio_padrao_ns",
         "comparacoes", "encontrado"],
        saida
    )



# EXPERIMENTO 5 E 6: ORDENACAO E ESTADO INICIAL
# Algoritmos quadraticos sao registrados como pulados a partir de 10 mil.


def testar_ordenacoes(repeticoes):
    print("\nTestando algoritmos de ordenacao...")
    saida = []
    for n in TAMANHOS:
        aleatoria = carregar_ids(DADOS / f"base_{n}_desordenada.csv")
        ordenada = carregar_ids(DADOS / f"base_{n}_ordenada.csv")
        inversa = list(reversed(ordenada))
        for estado, original in [
            ("aleatorio", aleatoria), ("ordenado", ordenada), ("inverso", inversa)
        ]:
            for nome, funcao in ORDENACOES.items():
                quadratico = nome in ("Bubble Sort", "Selection Sort", "Insertion Sort")
                if quadratico and n >= 10_000:
                    saida.append([
                        nome, n, estado, 0, "", "", "", "", "",
                        "pulado: custo elevado esperado"
                    ])
                    continue

                tempos = []
                comparacoes = movimentos = 0
                correto = True
                for _ in range(repeticoes):
                    copia = original.copy()
                    inicio = time.perf_counter()
                    c, m = funcao(copia)
                    tempos.append((time.perf_counter() - inicio) * 1000)
                    comparacoes, movimentos = c, m
                    correto = correto and copia == sorted(original)

                media, mediana, desvio = estatisticas(tempos)
                saida.append([
                    nome, n, estado, repeticoes, media, mediana, desvio,
                    comparacoes, movimentos, "correto" if correto else "ERRO"
                ])
        print(f"  Ordenacao: base {n:,} concluida.".replace(",", "."))

    salvar_csv(
        "resultados_ordenacao.csv",
        ["algoritmo", "quantidade", "estado_inicial", "repeticoes",
         "tempo_medio_ms", "tempo_mediano_ms", "desvio_padrao_ms",
         "comparacoes", "movimentacoes", "validacao"],
        saida
    )



# EXPERIMENTO 7: INSERCAO
# Estrategia A: acrescenta no fim e ordena tudo novamente.
# Estrategia B: encontra a posicao com bisect e insere mantendo ordenado.


def testar_insercao(repeticoes):
    print("\nTestando as duas estrategias de insercao...")
    saida = []
    regioes = [
        ("inicio", 0.00), ("25%", 0.25), ("meio", 0.50),
        ("75%", 0.75), ("final", 1.00)
    ]
    for n in TAMANHOS:
        base = carregar_ids(DADOS / f"base_{n}_ordenada.csv")
        for regiao, fracao in regioes:
            posicao = min(int(len(base) * fracao), len(base))
            # Escolhe um ID que fique na regiao pretendida.
            if posicao == 0:
                valor = base[0] - 1
            elif posicao == len(base):
                valor = base[-1] + 1
            else:
                valor = (base[posicao - 1] + base[posicao]) // 2
                if valor in base:
                    valor = base[posicao - 1] + 0.5

            for estrategia in ("A - inserir e ordenar", "B - inserir na posicao"):
                tempos = []
                correto = True
                for _ in range(repeticoes):
                    copia = base.copy()
                    inicio = time.perf_counter_ns()
                    if estrategia.startswith("A"):
                        copia.append(valor)
                        copia.sort()
                    else:
                        indice = bisect.bisect_left(copia, valor)
                        copia.insert(indice, valor)
                    tempos.append(time.perf_counter_ns() - inicio)
                    correto = correto and copia == sorted(base + [valor])
                media, mediana, desvio = estatisticas(tempos)
                saida.append([
                    n, regiao, estrategia, repeticoes,
                    media, mediana, desvio, correto
                ])

    salvar_csv(
        "resultados_insercao.csv",
        ["quantidade", "regiao", "estrategia", "repeticoes",
         "tempo_medio_ns", "tempo_mediano_ns", "desvio_padrao_ns", "resultado_correto"],
        saida
    )



# EXPERIMENTO 8: REMOCAO
# Mede separadamente localizacao, remocao e tempo total.


def testar_remocao(repeticoes):
    print("\nTestando remocao...")
    saida = []
    regioes = [("inicio", 0.0), ("meio", 0.5), ("final", 1.0)]
    for n in TAMANHOS:
        base = carregar_ids(DADOS / f"base_{n}_ordenada.csv")
        for regiao, fracao in regioes:
            indice = min(int((len(base) - 1) * fracao), len(base) - 1)
            valor = base[indice]
            tempos_localizacao, tempos_remocao, tempos_totais = [], [], []
            for _ in range(repeticoes):
                copia = base.copy()
                inicio_total = time.perf_counter_ns()
                inicio = time.perf_counter_ns()
                posicao = copia.index(valor)
                tempos_localizacao.append(time.perf_counter_ns() - inicio)
                inicio = time.perf_counter_ns()
                copia.pop(posicao)
                tempos_remocao.append(time.perf_counter_ns() - inicio)
                tempos_totais.append(time.perf_counter_ns() - inicio_total)

            loc = estatisticas(tempos_localizacao)
            rem = estatisticas(tempos_remocao)
            total = estatisticas(tempos_totais)
            saida.append([
                n, regiao, valor, repeticoes,
                loc[0], rem[0], total[0],
                loc[1], rem[1], total[1],
                loc[2], rem[2], total[2]
            ])

    salvar_csv(
        "resultados_remocao.csv",
        ["quantidade", "regiao", "id_removido", "repeticoes",
         "localizacao_media_ns", "remocao_media_ns", "total_medio_ns",
         "localizacao_mediana_ns", "remocao_mediana_ns", "total_mediano_ns",
         "localizacao_desvio_ns", "remocao_desvio_ns", "total_desvio_ns"],
        saida
    )

# EXPERIMENTO 9: MUITAS CONSULTAS EM 100.000 REGISTROS
# Sistema A: lista desordenada + buscas lineares.
# Sistema B: custo de ordenar uma vez + buscas binarias.

def testar_muitas_consultas():
    print("\nTestando muitas consultas (100.000 registros)...")
    n = 100_000
    desordenada = carregar_ids(DADOS / f"base_{n}_desordenada.csv")
    quantidades = [1, 10, 100, 1_000, 10_000]
    rng = random.Random(SEMENTE)
    consultas = [rng.choice(desordenada) for _ in range(max(quantidades))]

    inicio = time.perf_counter_ns()
    ordenada = sorted(desordenada)
    tempo_ordenacao = time.perf_counter_ns() - inicio

    saida = []
    for quantidade in quantidades:
        chaves = consultas[:quantidade]

        inicio = time.perf_counter_ns()
        for chave in chaves:
            busca_linear(desordenada, chave)
        tempo_a = time.perf_counter_ns() - inicio

        inicio = time.perf_counter_ns()
        for chave in chaves:
            busca_binaria(ordenada, chave)
        tempo_buscas_b = time.perf_counter_ns() - inicio
        tempo_b_total = tempo_ordenacao + tempo_buscas_b

        saida.append([
            n, quantidade, tempo_a, tempo_ordenacao,
            tempo_buscas_b, tempo_b_total,
            "Sistema A" if tempo_a < tempo_b_total else "Sistema B"
        ])

    salvar_csv(
        "resultados_muitas_consultas.csv",
        ["quantidade_registros", "numero_consultas",
         "sistema_a_linear_ns", "ordenacao_inicial_b_ns",
         "buscas_binarias_b_ns", "sistema_b_total_ns", "mais_rapido"],
        saida
    )

# GRAFICOS OBRIGATORIOS (5

def gerar_graficos():
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("Matplotlib nao instalado. Execute: python -m pip install matplotlib")
        return

    GRAFICOS.mkdir(parents=True, exist_ok=True)

    def ler_resultado(nome):
        caminho = RESULTADOS / nome
        if not caminho.exists():
            print(f"Arquivo ainda nao encontrado: {caminho.name}")
            return []
        with caminho.open(encoding="utf-8-sig", newline="") as arquivo:
            return list(csv.DictReader(arquivo))

    buscas = ler_resultado("resultados_busca.csv")
    if buscas:
        # Grafico 1: tamanho x tempo medio de busca (buscas no meio).
        plt.figure(figsize=(9, 5))
        for algoritmo in sorted({r["algoritmo"] for r in buscas}):
            pontos = [
                r for r in buscas
                if r["algoritmo"] == algoritmo
                and r["estado"] == "ordenada"
                and r["posicao"] == "meio"
            ]
            pontos.sort(key=lambda r: int(r["quantidade"]))
            if pontos:
                plt.plot(
                    [int(r["quantidade"]) for r in pontos],
                    [float(r["tempo_medio_ns"]) / 1000 for r in pontos],
                    marker="o", label=algoritmo
                )
        plt.xscale("log")
        plt.xlabel("Numero de registros")
        plt.ylabel("Tempo medio (microssegundos)")
        plt.title("Numero de registros x tempo de busca")
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.tight_layout()
        plt.savefig(GRAFICOS / "01_tempo_busca.png", dpi=150)
        plt.close()

        # Grafico 2: tamanho x comparacoes.
        plt.figure(figsize=(9, 5))
        for algoritmo in sorted({r["algoritmo"] for r in buscas}):
            pontos = [
                r for r in buscas
                if r["algoritmo"] == algoritmo
                and r["estado"] == "ordenada"
                and r["posicao"] == "nao encontrado"
            ]
            pontos.sort(key=lambda r: int(r["quantidade"]))
            if pontos:
                plt.plot(
                    [int(r["quantidade"]) for r in pontos],
                    [int(r["comparacoes"]) for r in pontos],
                    marker="o", label=algoritmo
                )
        plt.xscale("log")
        plt.yscale("log")
        plt.xlabel("Numero de registros")
        plt.ylabel("Comparacoes")
        plt.title("Numero de registros x numero de comparacoes")
        plt.grid(True, which="both", alpha=0.3)
        plt.legend()
        plt.tight_layout()
        plt.savefig(GRAFICOS / "02_comparacoes_busca.png", dpi=150)
        plt.close()

    ordenacoes = ler_resultado("resultados_ordenacao.csv")
    if ordenacoes:
        # Grafico 3: tamanho x tempo de ordenacao (uma linha por algoritmo).
        plt.figure(figsize=(9, 5))
        for algoritmo in sorted({r["algoritmo"] for r in ordenacoes}):
            pontos = [
                r for r in ordenacoes
                if r["algoritmo"] == algoritmo
                and r["estado_inicial"] == "aleatorio"
                and r["tempo_medio_ms"] not in ("", None)
            ]
            pontos.sort(key=lambda r: int(r["quantidade"]))
            if pontos:
                plt.plot(
                    [int(r["quantidade"]) for r in pontos],
                    [float(r["tempo_medio_ms"]) for r in pontos],
                    marker="o", label=algoritmo
                )
        plt.xscale("log")
        plt.yscale("log")
        plt.xlabel("Numero de registros")
        plt.ylabel("Tempo medio (ms)")
        plt.title("Numero de registros x tempo de ordenacao")
        plt.grid(True, which="both", alpha=0.3)
        plt.legend()
        plt.tight_layout()
        plt.savefig(GRAFICOS / "03_tempo_ordenacao.png", dpi=150)
        plt.close()

    consultas = ler_resultado("resultados_muitas_consultas.csv")
    if consultas:
        # Grafico 4: numero de consultas x tempo total dos sistemas.
        plt.figure(figsize=(9, 5))
        x = [int(r["numero_consultas"]) for r in consultas]
        plt.plot(x, [int(r["sistema_a_linear_ns"]) / 1e6 for r in consultas],
                 marker="o", label="Sistema A - linear")
        plt.plot(x, [int(r["sistema_b_total_ns"]) / 1e6 for r in consultas],
                 marker="o", label="Sistema B - ordenar + binaria")
        plt.xscale("log")
        plt.xlabel("Quantidade de buscas")
        plt.ylabel("Tempo total (ms)")
        plt.title("Quantidade de buscas x tempo total")
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.tight_layout()
        plt.savefig(GRAFICOS / "04_muitas_consultas.png", dpi=150)
        plt.close()

    insercoes = ler_resultado("resultados_insercao.csv")
    if insercoes:
        # Grafico 5 adicional: estrategias de insercao.
        dados = [r for r in insercoes if int(r["quantidade"]) == 100_000]
        regioes = ["inicio", "25%", "meio", "75%", "final"]
        estrategias = ["A - inserir e ordenar", "B - inserir na posicao"]
        plt.figure(figsize=(10, 5))
        largura = 0.35
        posicoes = list(range(len(regioes)))
        for indice, estrategia in enumerate(estrategias):
            valores = []
            for regiao in regioes:
                item = next(
                    (r for r in dados if r["regiao"] == regiao
                     and r["estrategia"] == estrategia), None
                )
                valores.append(float(item["tempo_medio_ns"]) / 1e6 if item else 0)
            deslocamento = (indice - 0.5) * largura
            plt.bar([p + deslocamento for p in posicoes], valores,
                    width=largura, label=estrategia)
        plt.xticks(posicoes, regioes)
        plt.xlabel("Regiao de insercao")
        plt.ylabel("Tempo medio (ms)")
        plt.title("Comparacao das estrategias de insercao - 100.000 registros")
        plt.legend()
        plt.tight_layout()
        plt.savefig(GRAFICOS / "05_estrategias_insercao.png", dpi=150)
        plt.close()

    print(f"Graficos salvos em: {GRAFICOS}")

def gerar_resumo():
    RESULTADOS.mkdir(parents=True, exist_ok=True)
    linhas = [
        "RESUMO DOS EXPERIMENTOS",
        "=======================",
        "",
        "Arquivos CSV gerados:",
        "- resultados_busca.csv",
        "- resultados_ordenacao.csv",
        "- resultados_insercao.csv",
        "- resultados_remocao.csv",
        "- resultados_muitas_consultas.csv",
        "",
        "Observacao: Bubble, Selection e Insertion Sort foram registrados como",
        "pulados nas bases a partir de 10.000 itens devido ao custo quadratico.",
        "A busca linear recursiva usa recursao por blocos para respeitar o limite",
        "de pilha do Python sem deixar de percorrer toda a base.",
        "",
    ]
    (RESULTADOS / "resumo_experimentos.txt").write_text(
        "\n".join(linhas), encoding="utf-8"
    )
    print("\n".join(linhas))


def executar_experimentos(completo=False):
    repeticoes = 30 if completo else 3
    testar_buscas(repeticoes)
    testar_ordenacoes(repeticoes)
    testar_insercao(repeticoes)
    testar_remocao(repeticoes)
    testar_muitas_consultas()
    salvar_ambiente(repeticoes)
    gerar_resumo()
    gerar_graficos()
    print("\nTodos os experimentos foram finalizados.")


def menu():
    while True:
        print("\n========================================")
        print("       LABORATORIO DE ALGORITMOS")
        print("========================================")
        print("1. Executar todos os testes (rapido - 3 repeticoes)")
        print("2. Executar todos os testes (completo - 30 repeticoes)")
        print("3. Preparar as bases de dados")
        print("4. Gerar os graficos")
        print("5. Ver resumo dos resultados")
        print("0. Sair")
        opcao = input("\nEscolha uma opcao: ").strip()

        try:
            if opcao == "1":
                preparar_bases()
                executar_experimentos(completo=False)
            elif opcao == "2":
                preparar_bases()
                executar_experimentos(completo=True)
            elif opcao == "3":
                preparar_bases()
            elif opcao == "4":
                gerar_graficos()
            elif opcao == "5":
                caminho = RESULTADOS / "resumo_experimentos.txt"
                print(caminho.read_text(encoding="utf-8") if caminho.exists()
                      else "Ainda nao existe resumo. Execute os testes primeiro.")
            elif opcao == "0":
                print("Programa encerrado.")
                break
            else:
                print("Opcao invalida.")
        except Exception as erro:
            print(f"\nOcorreu um problema: {erro}")

        input("\nPressione ENTER para continuar...")


if __name__ == "__main__":
    menu()
