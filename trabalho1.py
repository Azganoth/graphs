from textwrap import dedent
from math import inf
from time import sleep
from re import compile as re_compile

from graph import Graph, Digraph
from utils import ask_true_false_br


vertices_re = re_compile(r'[^,]+')
edges_weightless_re = re_compile(r'([^,]+)(?:,)([^,]+)(?:;)')
edges_weighted_re = re_compile(r'([^,]+)(?:,)([^,]+)(?:,)([^;]+)(?:;)')

if __name__ == '__main__':
    print(dedent("""
    Este programa tem como objetivo mostrar quatro representações de um grafo:
    lista de arestas, lista de adjacência, matriz de adjacência, matriz de incidência.

    Para isso é requerido as seguintes informações do grafo pelo usuário:
    se o grafo é orientado, se o grafo é valorado (apenas arestas),
    as vértices do grafo e as arestas do grafo.
    """))

    sleep(1)

    directed = ask_true_false_br("O grafo é orientado? (s/n) ")
    # directed = True
    weighted = ask_true_false_br("O grafo é valorado (apenas arestas)? (s/n) ")
    # weighted = True

    graph = Digraph() if directed else Graph()

    # set v
    set_v = None
    while not set_v:
        temp_set_v = set(vertices_re.findall(input(dedent("""
        Informe o conjunto V do grafo, e.g. 'u,v,x,y' (sem aspas):
        """))))
        # temp_set_v = set(vertices_re.findall('s,u,x,v,y'))
        if ask_true_false_br(f"Conjunto V := {{{', '.join(temp_set_v)}}}? (s/n) "):
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
        if ask_true_false_br(f"Conjunto E := {{"
                             f"{', '.join(map(lambda e: f'({e[0]}, {e[1]}, {e[2]})', temp_set_e))}"
                             f"}}? (s/n) "):
            set_e = temp_set_e

    for edge in set_e:
        if weighted:
            graph.add_edge(edge[0], edge[1], valor=edge[2])
        else:
            graph.add_edge(edge[0], edge[1])

    def edges_list():
        edges_list_str = dedent("""
        >> Lista de arestas

                Aresta        | Dados/Valor
        """)
        for u, v, d in graph.edges_list():
            formated_e = f"{{{u},{v}}}"
            edges_list_str += f"\n{formated_e:^22}| {d}"
        return edges_list_str

    def adjacency_list():
        _adjacency_list = graph.adjacency_list()
        adjacency_list_str = ">> Lista de adjacência\n"
        for u in _adjacency_list:
            adjacency_list_str += f"\n{u} --> " \
                                  f"{' -> '.join(str(v) for v in _adjacency_list[u])}"
        return adjacency_list_str

    def adjacency_matrix():
        _adjacency_matrix = graph.adjacency_matrix(
            lambda data: int(data['valor'] if weighted else 1))
        adjacency_matrix_str = dedent(f"""
        >> Matriz de adjacência

                   {"".join(f"{str(v):^11}" for v in _adjacency_matrix)}
        """)
        for u in _adjacency_matrix:
            adjacency_matrix_str += f"\n{str(u):^11}"
            for v in _adjacency_matrix[u]:
                adjacency_matrix_str += ("{:^11}".format('∞'
                                                         if _adjacency_matrix[u][v] == inf
                                                         and weighted
                                                         else _adjacency_matrix[u][v]))
        return adjacency_matrix_str

    def incidency_matrix():
        _incidency_matrix = {}
        _edges_list = graph.edges_list()
        incidency_matrix_str = dedent(f"""
        >> Matriz de incidência

                   {"".join(f'{f"{{{u},{v}}}":^22}' for u, v, _ in _edges_list)}
        """)
        for x in sorted(graph.vertices):
            incidency_matrix_str += f"\n{str(x):^11}"
            for u, v, d in _edges_list:
                if directed:
                    incidency_matrix_str += \
                        f"{1 if x == u else -1 if x == v else 0:^22}"
                else:
                    incidency_matrix_str += f"{1 if x == u or x == v else 0:^22}"
        return incidency_matrix_str

    print(edges_list(), adjacency_list(), adjacency_matrix(), incidency_matrix(), sep='\n')
