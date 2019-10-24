from textwrap import dedent
from time import sleep
from re import compile as re_compile

from graph import Graph, kruskal, prim_jarnik


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
    Este programa tem como objetivo mostrar as
    arestas do subgrafo (árvore geradora mínima) e o custo,
    tanto pelo algoritmo kruskal, quanto pelo algortmo prim-jarnik.

    Para isso é requerido as seguintes informações do grafo não-orientado
    pelo usuário:
    se o grafo é valorado (apenas arestas),
    as vértices do grafo e as arestas do grafo.
    """))

    sleep(1)

    weighted = true_false_input("O grafo é valorado (apenas arestas)? (s/n): ")
    # weighted = True

    graph = Graph()

    # set v
    set_v = None
    while not set_v:
        temp_set_v = set(vertices_re.findall(input(dedent("""
        Informe o conjunto V do grafo, e.g. 'u,v,x,y' (sem aspas):
        """))))
        # temp_set_v = set(vertices_re.findall('0,1,2,3,4,5,6,7,8'))
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
        # temp_set_e = set(edges_re.findall('0,1,4;1,7,11;0,7,8;1,2,8;2,3,7;3,4,9;4,5,10;'
        #                                   '5,3,14;2,5,4;2,8,2;8,6,6;6,5,2;8,7,7;6,7,1;'))

        temp_set_e_u = set(map(lambda e: e[0], temp_set_e))  # set of the 1th vertex of each edge
        temp_set_e_v = set(map(lambda e: e[1], temp_set_e))  # set of the 2th vertex of each edge

        # if the list isn't empty it means that the provided set of edges won't create a connected
        # graph, so we will inform the user and ask for another set of edges
        if [v for v in set_v if v not in temp_set_e_u and v not in temp_set_e_v]:
            print("Informe um conjunto de arestas que formem um grafo conexo! "
                  "(utiliza todos os vértices)")
        elif true_false_input(f"Conjunto E := {{"
                              f"{', '.join(map(lambda e: f'({e[0]}, {e[1]})', temp_set_e))}"
                              f"}}? (s/n): "):
            set_e = temp_set_e

    for edge in set_e:
        if weighted:
            graph.add_edge(edge[0], edge[1], valor=edge[2])
        else:
            graph.add_edge(edge[0], edge[1])

    def kruskal_repr():
        cost, edges = kruskal(graph, lambda data: int(data['valor']) if weighted else 1)
        kruskal_str = dedent(f"""
        >> Resultado utilizando o algoritmo Kruskal:
        Custo: {cost}
        Arestas: {{{', '.join(map(lambda e: f'({e[0]}, {e[1]})', edges))}}}
        """)
        return kruskal_str

    def prim_jarnik_repr():
        cost, edges = prim_jarnik(graph, lambda data: int(data['valor']) if weighted else 1)
        prim_jarnik_str = dedent(f"""
        >> Resultado utilizando o algoritmo Prim-Jarnik:
        Custo: {cost}
        Arestas: {{{', '.join(map(lambda e: f'({e[0]}, {e[1]})', edges))}}}
        """)
        return prim_jarnik_str

    print(kruskal_repr(), prim_jarnik_repr(), sep='\n')
