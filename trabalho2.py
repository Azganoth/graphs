from collections import deque
from textwrap import dedent
from time import sleep
from re import compile as re_compile

from graph import Graph, Digraph, dijkstra


def true_false_input(message: str) -> bool:
    response = ''
    while response not in ('s', 'n'):
        response = input(message).strip().lower()
    return {'s': True, 'n': False}[response]


vertices_re = re_compile(r'[^,]+')
edges_weightless_re = re_compile(r'([^,])+(?:,)([^,])(?:;)')
edges_weighted_re = re_compile(r'([^,])+(?:,)([^,])(?:,)([^;]+)(?:;)')

if __name__ == '__main__':
    print(dedent("""
    Este programa tem como objetivo mostrar uma tabela demonstrando as
    distâncias e os caminhos entre o vértice de origem e os demains vértices,
    este resultado é gerado pelo algoritmo Dijkstra.

    Para isso é requerido as seguintes informações do grafo pelo usuário:
    se o grafo é orientado, se o grafo é valorado (apenas arestas),
    as vértices do grafo e as arestas do grafo, assim como o vértice de origem.
    """))

    sleep(1)

    directed = true_false_input("O grafo é orientado? (s/n): ")
    # directed = True
    weighted = true_false_input("O grafo é valorado (apenas arestas)? (s/n): ")
    # weighted = True

    graph = Digraph() if directed else Graph()

    # set v
    set_v = None
    while not set_v:
        temp_set_v = set(vertices_re.findall(input(dedent("""
        Informe o conjunto V do grafo, e.g. 'u,v,x,y' (sem aspas):
        """))))
        # temp_set_v = set(vertices_re.findall('s,u,x,v,y'))
        if true_false_input(f"Conjunto V := {{{', '.join(temp_set_v)}}}? (s/n): "):
            set_v = temp_set_v

    for vertex in set_v:
        graph.add_vertex(vertex)

    # set e
    edges_re = edges_weighted_re if weighted else edges_weightless_re
    set_e = None
    while not set_e:
        temp_set_e = set(edges_re.findall(input(dedent("""
        Informe o conjunto E do grafo, e.g. 'u,v,valor;x,y,valor;' OU 'u,v;x,y;' (sem aspas):
        """))))
        # temp_set_e = set(edges_re.findall(
        #     's,x,5;s,u,10;x,u,3;x,y,2;u,x,2;u,v,1;v,y,4;y,v,6;y,s,7;'))
        if true_false_input(f"Conjunto E := {{"
                            f"{', '.join(map(lambda e: f'({e[0]}, {e[1]})', temp_set_e))}"
                            f"}}? (s/n): "):
            set_e = temp_set_e

    for edge in set_e:
        if weighted:
            graph.add_edge(edge[0], edge[1], valor=edge[2])
        else:
            graph.add_edge(edge[0], edge[1])

    start_vertex = None
    while not start_vertex:
        temp_start_vertex = input(dedent(f"""
        Escolha um dos seguintes vértices para ser o vértice de origem (inicial):
        Conjunto V := {{{', '.join(str(v) for v in graph.vertices)}}};
        """))
        # temp_start_vertex = 's'
        if temp_start_vertex in graph.vertices:
            start_vertex = temp_start_vertex

    def dijkstra_repr():
        distance, parents = dijkstra(graph, start_vertex,
                                     lambda data: int(data['valor']) if weighted else 1)
        dijkstra_str = dedent("""
          Vértices   |  Distância  |    Path
        -----------------------------------------
        """)

        vertices = deque(v for v in graph.vertices if v != start_vertex)
        vertices.appendleft(start_vertex)
        for v in vertices:
            dijkstra_str += (f"\n{v:^13}|{distance[v]:^13}"
                             f"|{parents[v] if parents[v] else '-':^13}")

        return dijkstra_str

    print(dijkstra_repr())
