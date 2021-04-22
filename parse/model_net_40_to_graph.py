import os_
import numpy as np

PREFIX = 'OFF'
off_sep = ' '
encoding = 'utf8'
vertex_start = 2
graph_sep = ' '
suffix = '.off'

"""
off file format

OFF numVertices numFaces numEdges
x y z
x y z
... numVertices like above
NVertices v1 v2 v3 ... vN
MVertices v1 v2 v3 ... vM
... numFaces like above

OFF
8 6 0
-0.500000 -0.500000 0.500000
0.500000 -0.500000 0.500000
-0.500000 0.500000 0.500000
0.500000 0.500000 0.500000
-0.500000 0.500000 -0.500000
0.500000 0.500000 -0.500000
-0.500000 -0.500000 -0.500000
0.500000 -0.500000 -0.500000
4 0 1 3 2
4 2 3 5 4
4 4 5 7 6
4 6 7 1 0
4 1 7 5 3
4 6 0 2 4
"""


def model_net_to_graph(off_file,
                       position_file,
                       graph_file,
                       off_sep=off_sep,
                       graph_sep=graph_sep,
                       encoding=encoding,
                       vertex_start=vertex_start):
    """
    Convert a ModelNet40 OFF file into a list stored graph.

    :param off_file: input off file
    :param graph_file: output graph file
    :param position_file: vertex position file
    :param off_sep: off separator
    :param graph_sep: graph separator
    :param encoding:
    :param vertex_start: starting vertex from which line
    :return:
    """
    fh = open(off_file, 'r', encoding=encoding)
    lines = fh.read().rstrip().split('\n')

    # vertices faces edges
    vfe = lines[1].rstrip()

    num_vertices = int(vfe.split(off_sep)[0])
    vertices = lines[vertex_start:vertex_start + num_vertices]
    faces = lines[vertex_start + num_vertices:]

    pos_dict = index_position(vertices, off_sep)
    graph = faces2graph(pos_dict, faces, graph_sep)

    save_position(position_file, pos_dict, graph_sep)
    save_graph(graph_file, graph, graph_sep)


def get_points_and_edge(off_file,
                        off_sep=off_sep,
                        graph_sep=graph_sep,
                        encoding=encoding,
                        vertex_start=vertex_start):
    fh = open(off_file, 'r', encoding=encoding)
    lines = fh.read().rstrip().split('\n')

    # vertices faces edges
    vfe = lines[1].rstrip()

    num_vertices = int(vfe.split(off_sep)[0])
    vertices = lines[vertex_start:vertex_start + num_vertices]
    faces = lines[vertex_start + num_vertices:]

    pos_dict = index_position(vertices, off_sep)
    graph = faces2graph(pos_dict, faces, graph_sep)

    return pos_dict, graph


def index_position(lst, sep):
    """
    index a vertex list, starting from 0
    :param lst: vertex list
    :param sep: separator
    :return:
    """
    pos_dict = dict()
    for no, p in enumerate(lst):
        value = p.strip().split(sep)
        value = [float(v) for v in value]
        pos_dict[no] = value
    return pos_dict


def faces2graph(pos_dict, faces, graph_sep):
    """
    Convert indices list to graph.
    :param pos_dict: position directory
    :param faces: 3D object faces
    :param graph_sep: graph separator
    :return:
    """
    graph = {}
    for face in faces:
        lst = face.split(off_sep)
        num_edges = int(lst[0])
        edges = lst[1:]

        for e in range(num_edges):
            idx1 = int(edges[e])
            idx2 = int(edges[(e + 1) % num_edges])

            # remove the duplicated lines like (1,0) and (1,0) are the same line.
            if idx1 > idx2:
                tmp = idx1
                idx1 = idx2
                idx2 = tmp

            graph['{}{}{}'.format(idx1, graph_sep, idx2)] = distance(np.array(pos_dict[idx1]), np.array(pos_dict[idx2]))

    return graph


def distance(point1, point2):
    """
    Compute the distance of two points.
    :param point1:
    :param point2:
    :return:
    """
    return np.linalg.norm(point1 - point2)


def save_position(filename, pos_dict, sep):
    """
    Save vertex position information into a file.
    :param filename: position filename
    :param pos_dict: position dictionary
    :param sep: separator
    :return:
    """
    with open(filename, 'w') as fh:
        lines = []
        lines.append(str(len(pos_dict)))
        for i in sorted(pos_dict.keys(), key=lambda x: x):
            line = str(i) + sep + str(pos_dict[i]).replace('[', '').replace(']', '').replace(',', sep)
            lines.append(line)
        fh.write('\n'.join(lines))


def save_graph(filename, graph, sep):
    """
    Save graph into a file.
    :param filename:
    :param graph:
    :param sep:
    :return:
    """
    with open(filename, 'w') as fh:
        lines = []
        for i in sorted(graph.keys(), key=lambda x: int(x.split(sep)[0])):
            lines.append(sep.join([i, str(graph[i])]))
        fh.write('\n'.join(lines))


def model_net_40_to_graph(models_path):
    for root, dirs, files in os_.walk(models_path):
        for file in files:
            if file.endswith(suffix):
                model_net_to_graph(os_.path.join(root, file),
                                   os_.path.join(root, file.replace(suffix, '_position.txt')),
                                   os_.path.join(root, file.replace(suffix, '_graph.txt')))
