import warnings
import pandas as pd
import networkx as nx
import os
from urllib.parse import urlparse
import tempfile

import requests

from swmmio.utils import error


def random_alphanumeric(n=6):
    import random
    chars = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    return ''.join(random.choice(chars) for i in range(n))


def model_to_networkx(model, drop_cycles=True):
    '''
    Networkx MultiDiGraph representation of the model
    '''
    from geojson import Point, LineString

    def multidigraph_from_edges(edges, source, target):
        '''
        create a MultiDiGraph from a dataframe of edges, using the row index
        as the key in the MultiDiGraph
        '''
        us = edges[source]
        vs = edges[target]
        keys = edges.index
        data = edges.drop([source, target], axis=1)
        d_dicts = data.to_dict(orient='records')

        G = nx.MultiDiGraph()

        G.add_edges_from(zip(us, vs, keys, d_dicts))

        return G

    # parse swmm model results with swmmio, concat all links into one dataframe
    nodes = model.nodes()
    links = model.links()
    links['facilityid'] = links.index

    # create a nx.MultiDiGraph from the combined model links, add node data, set CRS
    G = multidigraph_from_edges(links, 'InletNode', target='OutletNode')
    G.add_nodes_from(zip(nodes.index, nodes.to_dict(orient='records')))

    # create geojson geometry objects for each graph element
    for u, v, k, coords in G.edges(data='coords', keys=True):
        if coords:
            G[u][v][k]['geometry'] = LineString(coords)
    for n, coords in G.nodes(data='coords'):
        if coords:
            G.nodes[n]['geometry'] = Point(coords[0])

    if drop_cycles:
        # remove cycles
        cycles = list(nx.simple_cycles(G))
        if len(cycles) > 0:
            warnings.warn(f'cycles detected and removed: {cycles}')
            G.remove_edges_from(cycles)

    G.graph['crs'] = model.crs
    return G


def find_invalid_links(inp, node_ids=None, link_type='conduits', drop=False):
    elems = getattr(inp, link_type)
    invalids = elems.index[~(elems.InletNode.isin(node_ids) & elems.OutletNode.isin(node_ids))]
    if drop:
        df = elems.loc[elems.InletNode.isin(node_ids) & elems.OutletNode.isin(node_ids)]
        setattr(inp, link_type, df)
    return invalids.tolist()


def trim_section_to_nodes(inp, node_ids=None, node_type='junctions', drop=True):
    elems = getattr(inp, node_type)
    invalids = elems.index[~(elems.index.isin(node_ids))]
    if drop:
        df = elems.loc[elems.index.isin(node_ids)]
        setattr(inp, node_type, df)
    return invalids.tolist()


# def drop_invalid_model_elements(inp):
#     """
#     Identify references to elements in the model that are undefined and remove them from the
#     model. These should coincide with warnings/errors produced by SWMM5 when undefined elements
#     are referenced in links, subcatchments, and controls.
#     :param model: swmmio.Model
#     :return:
#     >>> import swmmio
#     >>> m = swmmio.Model(MODEL_FULL_FEATURES_INVALID)
#     >>> drop_invalid_model_elements(m.inp)
#     ['InvalidLink2', 'InvalidLink1']
#     >>> m.inp.conduits.index
#     Index(['C1:C2', 'C2.1', '1', '2', '4', '5'], dtype='object', name='Name')
#     """
#     from swmmio.utils.dataframes import create_dataframeINP
#     juncs = create_dataframeINP(inp.path, "[JUNCTIONS]").index.tolist()
#     outfs = create_dataframeINP(inp.path, "[OUTFALLS]").index.tolist()
#     stors = create_dataframeINP(inp.path, "[STORAGE]").index.tolist()
#     nids = juncs + outfs + stors
#
#     # drop links with bad refs to inlet/outlet nodes
#     inv_conds = find_invalid_links(inp, nids, 'conduits', drop=True)
#     inv_pumps = find_invalid_links(inp, nids, 'pumps', drop=True)
#     inv_orifs = find_invalid_links(inp, nids, 'orifices', drop=True)
#     inv_weirs = find_invalid_links(inp, nids, 'weirs', drop=True)
#
#     # drop other parts of bad links
#     invalid_links = inv_conds + inv_pumps + inv_orifs + inv_weirs
#     inp.xsections = inp.xsections.loc[~inp.xsections.index.isin(invalid_links)]
#
#     # drop invalid subcats and their related components
#     invalid_subcats = inp.subcatchments.index[~inp.subcatchments['Outlet'].isin(nids)]
#     inp.subcatchments = inp.subcatchments.loc[~inp.subcatchments.index.isin(invalid_subcats)]
#     inp.subareas = inp.subareas.loc[~inp.subareas.index.isin(invalid_subcats)]
#     inp.infiltration= inp.infiltration.loc[~inp.infiltration.index.isin(invalid_subcats)]
#
#     return invalid_links + invalid_subcats


def rotate_model(m, rads=0.5, origin=None):
    """
    Rotate a model's coordinates by a specified angle around a given origin.

    Parameters
    ----------
    m : swmmio.Model
        The model whose coordinates are to be rotated.
    rads : float, optional
        The angle in radians by which to rotate the model. Default is 0.5 radians.
    origin : tuple of float, optional
        The (x, y) coordinates of the point around which to rotate the model. 
        If not provided, the origin defaults to (0, 0).

    Returns
    -------
    swmmio.Model
        The model with its coordinates rotated.

    Examples
    --------
    >>> from swmmio.tests.data import MODEL_FULL_FEATURES_XY_B
    >>> import swmmio
    >>> mb = swmmio.Model(MODEL_FULL_FEATURES_XY_B)
    >>> mc = rotate_model(mb, rads=0.75, origin=(2748515.571, 1117763.466))
    >>> mc.inp.coordinates
    """
    from swmmio.graphics.utils import rotate_coord_about_point

    origin = (0, 0) if not origin else origin
    rotate_lambda = lambda xy: rotate_coord_about_point(xy, rads, origin)
    coord = m.inp.coordinates.apply(rotate_lambda, axis=1)
    verts = m.inp.vertices.apply(rotate_lambda, axis=1)
    pgons = m.inp.polygons.apply(rotate_lambda, axis=1)

    # retain column names / convert to df
    m.inp.coordinates = pd.DataFrame(data=coord.to_list(),
                                     columns=m.inp.coordinates.columns,
                                     index=m.inp.coordinates.index)
    m.inp.vertices = pd.DataFrame(data=verts.to_list(),
                                  columns=m.inp.vertices.columns,
                                  index=m.inp.vertices.index)
    m.inp.polygons = pd.DataFrame(data=pgons.to_list(),
                                  columns=m.inp.polygons.columns,
                                  index=m.inp.polygons.index)

    return m


def remove_braces(string):
    return string.replace('[', '').replace(']', '')


def format_inp_section_header(string):
    """
    Ensure a string is in the inp section header format: [UPPERCASE],
    except in the case of the [Polygons] section with is capitalized case
    :param string:
    :return: string
    """
    if string == '[Polygons]':
        return string
    s = string.strip().upper()
    if s[0] != '[':
        s = f'[{s}'
    if s[-1] != ']':
        s = f'{s}]'

    return s


def merge_dicts(*dict_args):
    '''
    Given any number of dicts, shallow copy and merge into a new dict,
    precedence goes to key value pairs in latter dicts.
    '''
    result = {}
    for dictionary in dict_args:
        if dictionary:
            result.update(dictionary)
    return result


def trace_from_node(conduits, startnode, mode='up', stopnode=None):
    """
    trace up and down a SWMM model given a start node and optionally a
    stop node.
    """

    traced_nodes = [startnode]  # include the starting node
    traced_conduits = []

    def trace(node_id):
        for conduit, data in conduits.iterrows():
            if mode == 'up' and data.OutletNode == node_id and conduit not in traced_conduits:

                traced_nodes.append(data.InletNode)
                traced_conduits.append(conduit)

                if stopnode and data.InletNode == stopnode:
                    break
                trace(data.InletNode)

            if mode == 'down' and data.InletNode == node_id and conduit not in traced_conduits:
                traced_nodes.append(data.OutletNode)
                traced_conduits.append(conduit)

                if stopnode and data.OutletNode == stopnode:
                    break
                trace(data.OutletNode)

    # kickoff the trace
    print("Starting trace {} from {}".format(mode, startnode))
    trace(startnode)
    print("Traced {0} nodes from {1}".format(len(traced_nodes), startnode))
    return {'nodes': traced_nodes, 'conduits': traced_conduits}


def find_network_trace(model, start_node, end_node,
                       include_nodes=None, include_links=None):
    """
    This function searches for a path between two nodes.  In addition, since
    SWMM allows multiple links (edges) between nodes, the user can specify
    a list of both nodes, and links to include in the path.  It will return a
    single path selection.

    :param model: swmmio.Model object
    :param start_node: string of Node Name
    :param end_node: string of Node Name
    :param include_nodes: list of node name strings
    :param include_links: list of link name strings
    :return: Network Path Trace Tuple
    """
    nodes = model.nodes.dataframe
    links = model.links.dataframe
    model_digraph = model.network

    include_nodes = [] if include_nodes is None else include_nodes
    include_links = [] if include_links is None else include_links

    if str(start_node) not in nodes.index:
        raise(error.NodeNotInInputFile(start_node))
    if str(end_node) not in nodes.index:
        raise(error.NodeNotInInputFile(end_node))
    for node_id in include_nodes:
        if str(node_id) not in nodes.index:
            raise(error.NodeNotInInputFile(node_id))
    for link_id in include_links:
        if str(link_id) not in links.index:
            raise(error.LinkNotInInputFile(link_id))

    simple_paths = nx.all_simple_edge_paths(model_digraph, start_node, end_node)
    path_selection = None
    for path_index, path_info in enumerate(simple_paths):
        included_nodes = {name: False for name in include_nodes}
        included_links = {name: False for name in include_links}
        for selection in path_info:
            us, ds, link = selection
            if us in included_nodes.keys():
                included_nodes[us] = True
            if ds in included_nodes.keys():
                included_nodes[ds] = True
            if link in included_links.keys():
                included_links[link] = True

        if False not in [included_nodes[key] for key in included_nodes.keys()]:
            if False not in [included_links[key] for key in included_links.keys()]:
                path_selection = path_info
                break

    if path_selection is None:
        raise error.NoTraceFound

    return path_selection

def summarize_model(model) -> dict:
    """
    Summarize a SWMM model by calculating various statistics and counts of elements.
    
    Parameters
    ----------
    model : swmmio.core.Model
        An instance of a SWMM model containing input data (inp) and nodes.
    
    Returns
    -------
    dict
        A dictionary containing the summary of the model with the following keys:

        - 'num_subcatchments': int, number of subcatchments in the model.
        - 'num_conduits': int, number of conduits in the model.
        - 'num_junctions': int, number of junctions in the model.
        - 'num_outfalls': int, number of outfalls in the model.
        - 'num_raingages': int, number of raingages in the model.
        - 'catchment_area': float, total area of subcatchments (if subcatchments exist).
        - 'mean_subcatchment_slope': float, mean slope of subcatchments weighted by area (if subcatchments exist).
        - 'total_conduit_length': float, total length of conduits (if conduits exist).
        - 'invert_range': float, range of invert elevations of nodes (if nodes exist).
    """
    model_summary = dict()

    # numbers of elements
    model_summary['num_subcatchments'] = len(model.inp.subcatchments)
    model_summary['num_conduits'] = len(model.inp.conduits)
    model_summary['num_junctions'] = len(model.inp.junctions)
    model_summary['num_outfalls'] = len(model.inp.outfalls)
    model_summary['num_raingages'] = len(model.inp.raingages)

    # calculated values - only calculate if elements exist
    if len(model.inp.subcatchments) != 0:
        model_summary['catchment_area'] = model.inp.subcatchments.Area.sum()
        model_summary['mean_subcatchment_slope'] = ((model.inp.subcatchments.Area / model.inp.subcatchments.Area.sum()) * model.inp.subcatchments.PercSlope).sum()
    
    if len(model.inp.conduits) != 0:
        model_summary['total_conduit_length'] = model.inp.conduits.Length.sum()
    
    if len(model.nodes.dataframe) != 0:
        model_summary['invert_range'] = model.nodes().InvertElev.max() - model.nodes().InvertElev.min()
    return model_summary


def check_if_url_and_download(url):
    """
    Check if a given string is a URL and download the 
    file to a temporary directory if it is.

    Parameters
    ----------
    url : str
        string that may be a URL

    Returns
    -------
    str
        path to the downloaded file in the temporary directory or 
        the original string if it is not a URL
    """

    if url.startswith(('http://', 'https://')):
        r = requests.get(url)

        # get the filename from the url
        parsed_url = urlparse(url)
        filename = parsed_url.path.split('/')[-1]

        temp_path = os.path.join(tempfile.gettempdir(), filename)
        with open(temp_path, 'wb') as f:
            if r.status_code == 200:
                f.write(r.content)
            else:
                raise Exception(f"Failed to download file: {r.status_code}")
        return temp_path
    else:
        return url