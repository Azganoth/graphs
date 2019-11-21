from typing import Hashable, Tuple

from textwrap import dedent
from copy import deepcopy
from time import sleep
from ast import literal_eval
from re import compile as re_compile

from graph import BaseGraph, Graph, dijkstra, dijkstra_to
from utils import ask_true_false_br


def add_pin_in_map(graph_map: BaseGraph, pin: Hashable,
                   pin_coords: Tuple[Hashable, Hashable, float]):
    """Adds a pin (vertex) in the map (graph).

    Args:
        graph_map: The map (graph) to insert the pin (vertex).
        pin: The pin (vertex).
        pin_coords:
            The coordinates of the pin (vertex) in the map (graph).
            The coordinates must be composed of a tuple with 3 values:
            1th interchange (vertex u), 2nd interchange (vertex v)
            and a percentage indicating where in the street between the
            1th and 2nd interchange the pin (vertex) must be inserted.

    Raises:
        VertexError:
            Raises when a interchange (vertex) isn't in the map (graph).
        EdgeError:
            Raises when an street (edge) isn't in the map (graph).
    """
    graph_map.add_vertex(pin)

    coord_u, coord_v, coord_percentage = pin_coords

    # normalize percentage
    coord_percentage = (coord_percentage == 0 and .001
                        or coord_percentage == 1 and .999
                        or coord_percentage)

    street_distance = graph_map.pop_edge(coord_u, coord_v)['distance']

    street_distance_u = street_distance * coord_percentage
    street_distance_v = street_distance - street_distance_u

    graph_map.add_edge(coord_u, pin, distance=street_distance_u)
    graph_map.add_edge(pin, coord_v, distance=street_distance_v)


client_info_re = re_compile(r'([^,]+)(?:,)([^,]+)(?:,)([^,]+)(?:,)([^,]+)(?:,)([^,]+)(?:,)([^,]+)')

if __name__ == '__main__':
    print(dedent("""
    ...
    """))

    sleep(1)

    graph = Graph('Mapa da região')

    # TEMPLATE DATA (INTERCHANGES AND STREETS OF THE MAP)

    # interchanges
    interchanges = set(range(1, 56))  # {1, 2, 3, ... 54, 55}

    # streets
    streets = [
        # the street's distance is represented in kilometers
        # horizontal
        (1, 2, {'distance': .112}), (2, 3, {'distance': .115}), (3, 4, {'distance': .120}),
        (4, 5, {'distance': .145}), (5, 6, {'distance': .055}),

        (7, 8, {'distance': .112}),

        (9, 10, {'distance': .114}), (10, 11, {'distance': .112}), (11, 12, {'distance': .115}),
        (12, 13, {'distance': .120}), (13, 14, {'distance': .145}), (14, 15, {'distance': .055}),
        (15, 16, {'distance': .18}),

        (17, 18, {'distance': .114}), (18, 19, {'distance': .112}), (19, 20, {'distance': .115}),
        (20, 21, {'distance': .120}), (21, 22, {'distance': .145}), (22, 23, {'distance': .055}),
        (23, 24, {'distance': .180}),

        (25, 26, {'distance': .114}), (26, 27, {'distance': .112}), (27, 28, {'distance': .115}),
        (28, 29, {'distance': .120}), (29, 30, {'distance': .145}), (30, 31, {'distance': .055}),
        (31, 32, {'distance': .180}),

        (33, 34, {'distance': .114}), (34, 35, {'distance': .112}), (35, 36, {'distance': .115}),
        (36, 37, {'distance': .120}), (37, 38, {'distance': .200}),
        (38, 39, {'distance': .180}),

        (45, 46, {'distance': .140}), (46, 47, {'distance': .093}),

        (48, 49, {'distance': .114}), (49, 50, {'distance': .112}), (50, 52, {'distance': .115}),
        (52, 53, {'distance': .120}), (53, 54, {'distance': .145}), (54, 55, {'distance': .140}),

        # vertical
        (9, 17, {'distance': .110}), (17, 25, {'distance': .112}), (25, 33, {'distance': .111}),
        (33, 48, {'distance': .190}),

        (1, 7, {'distance': .045}), (7, 10, {'distance': .045}), (10, 18, {'distance': .110}),
        (18, 26, {'distance': .112}), (26, 34, {'distance': .111}), (34, 41, {'distance': .095}),
        (41, 49, {'distance': .095}),

        (2, 8, {'distance': .045}), (8, 11, {'distance': .045}), (11, 19, {'distance': .110}),
        (19, 27, {'distance': .112}), (27, 35, {'distance': .111}), (35, 50, {'distance': .190}),

        (3, 12, {'distance': .090}), (12, 20, {'distance': .110}), (20, 28, {'distance': .112}),
        (28, 36, {'distance': .111}),

        (4, 13, {'distance': .090}), (13, 21, {'distance': .110}), (21, 29, {'distance': .112}),
        (29, 37, {'distance': .111}), (37, 53, {'distance': .190}),

        (5, 14, {'distance': .090}), (14, 22, {'distance': .110}), (22, 30, {'distance': .112}),
        (45, 54, {'distance': .086}),

        (6, 15, {'distance': .090}), (15, 23, {'distance': .110}), (23, 31, {'distance': .112}),
        (46, 55, {'distance': .086}),

        (16, 24, {'distance': .110}), (24, 32, {'distance': .112}), (31, 38, {'distance': .111}),
        (32, 39, {'distance': .111}), (39, 47, {'distance': .190}),

        # lose-ends
        (40, 41, {'distance': .033}), (36, 42, {'distance': .047}), (51, 52, {'distance': .047}),
        (43, 45, {'distance': .040}), (44, 46, {'distance': .040}),
    ]

    # INSERT TEMPLATE DATA IN THE GRAPH
    for interchange in interchanges:
        graph.add_vertex(interchange)

    for street_u, street_v, street_data in streets:
        graph.add_edge(street_u, street_v, **street_data)

    # CLIENTS REQUESTS
    while ask_true_false_br("Alguma solicitação de viagem nova? (s/n) "):
        client_graph = deepcopy(graph)

        client = None
        while client is None:
            # noinspection PyTypeChecker,PyRedeclaration
            if (not (client_info := client_info_re.fullmatch(
                    input("\nInforme as coordenadas da localização do cliente e destino da viagem\n"
                          "no seguinte formato: u,v,porcentagem,x,y,porcentagem;\n"
                          "e.g. u,v,.5,x,y,.1\n")))
                    or len(client_info := tuple(map(literal_eval, client_info.groups()))) != 6
                    or 0 > client_info[2] or client_info[2] > 1
                    or 0 > client_info[5] or client_info[5] > 1):

                print("\nFormato inválido.")

            # verify if each interchange exists
            elif (not client_graph.has_vertex(arg := client_info[0])
                    or not client_graph.has_vertex(arg := client_info[1])
                    or not client_graph.has_vertex(arg := client_info[3])
                    or not client_graph.has_vertex(arg := client_info[4])):

                print(f"\nO cruzamento {arg} não existe no mapa.")

            # verify if each street exists
            elif (not client_graph.has_edge((edge := (client_info[0], client_info[1]))[0], edge[1])
                  or not client_graph.has_edge((edge := (client_info[3], client_info[4]))[0],
                                               edge[1])):

                print(f"\nNão existe uma rua entre os cruzamentos {{{edge[0]}, {edge[1]}}}")

            elif ask_true_false_br("\nEstes são os dados do cliente? (s/n)"
                                   "\nCoordenadas de localização: "
                                   f"{', '.join(map(str, client_info[:3]))}"
                                   "\nCoordenadas de destino: "
                                   f"{', '.join(map(str, client_info[3:]))}\n"):

                client = {'location': client_info[:3], 'destination': client_info[3:]}

        # insert client's location in the graph
        add_pin_in_map(client_graph, 'CLIENTE', client['location'])

        # available drivers
        drivers = {
            # the driver's location is composed of: vertex u, vertex v and
            # the percentage (0-1) indicating where he's located in the street (edge := {u, v})
            'A': {'location': (17, 18, .5)},
            'B': {'location': (27, 28, .75)},
            'C': {'location': (12, 13, .1)},
            'D': {'location': (37, 38, .9)},
        }

        driver = None
        while driver is None:
            drivers_graph = deepcopy(client_graph)
            for driver_v, driver_data in drivers.items():
                add_pin_in_map(drivers_graph, driver_v, driver_data['location'])

            if drivers:
                distance, parents = dijkstra(drivers_graph, 'CLIENTE', lambda s: s['distance'])
                temp_driver = driver_id = min(drivers, key=lambda d: distance[d])

                if ask_true_false_br(f"\nO motorista {driver_id} aceita a viagem do cliente de "
                                     f"{client['location']} para {client['destination']}\ncom uma "
                                     f"distância de {distance[temp_driver]:.3f} km ? (s/n) "):
                    driver = {
                        'client_distance': distance[temp_driver],
                        'client_path': [temp_driver]
                    }

                    # backtracking path from driver to client
                    while temp_driver != 'CLIENTE':
                        driver['client_path'].append(temp_driver := parents[temp_driver])

                    print(f"\nO motorista {driver_id} fez o menor trajeto para chegar ao cliente:"
                          f"\n{' -> '.join(map(str, driver['client_path']))};"
                          f"\ncom uma distância total percorrida de "
                          f"{driver['client_distance']:.3f} km.")
                else:
                    del drivers[temp_driver]
            else:
                print("\nNão há motoristas na àrea do cliente que possam atendê-lo.\n")
                break
        else:
            add_pin_in_map(client_graph, 'DESTINO', client['destination'])

            # calculate the shortest path from the client's location to his destination
            cost, path = dijkstra_to(client_graph, 'CLIENTE', 'DESTINO', lambda s: s['distance'])

            print("\nO menor caminho entre a localização atual do cliente e seu destino é:\n"
                  f"{' -> '.join(map(str, path))}\n"
                  f"com uma distância total de {sum(cost.values()):.3f} km.\n")
