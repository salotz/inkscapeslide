from copy import deepcopy

import xml.etree.ElementTree as xml_parser

INK_GROUPMODE = '{http://www.inkscape.org/namespaces/inkscape}groupmode'
INK_LABEL = '{http://www.inkscape.org/namespaces/inkscape}label'

W3C_SVG_TAG = '{http://www.w3.org/2000/svg}g'

LAYER_KEY = 'layer'


def parse_inkscape_svg(svg_str):

    return xml_parser.fromstring(svg_str)

def get_layers(svg_etree):
    """Return a list of tuples (layer_id, layer_name, etree.Element) in
    order of the inkscape layer stacking."""

    # get the layers by iterating over the elements with the W3C SVG
    # tag and that have the grouping attribute for the layer.

    # they are in reverse order of the layer ordering in inkscape, so
    # we reverse them
    layers = list(reversed([(layer.attrib['id'], layer.attrib[INK_LABEL], layer)
                            for layer in svg_etree.iter(tag=W3C_SVG_TAG)
                            if layer.attrib.get(INK_GROUPMODE, False) == LAYER_KEY]))

    return layers

def get_layers(svg_etree):
    """Return a list of tuples (layer_id, layer_name, etree.Element) in
    order of the inkscape layer stacking."""

    # get the layers by iterating over the elements with the W3C SVG
    # tag and that have the grouping attribute for the layer.

    # they are in reverse order of the layer ordering in inkscape, so
    # we reverse them
    layers = list(reversed([(layer.attrib['id'], layer.attrib[INK_LABEL], layer)
                            for layer in svg_etree.iter(tag=W3C_SVG_TAG)
                            if layer.attrib.get(INK_GROUPMODE, False) == LAYER_KEY]))

    return layers


def get_layer(svg_etree, layer_id):

    for layer in svg_etree.iter(tag=W3C_SVG_TAG):
        if layer.attrib.get(INK_GROUPMODE, False) == LAYER_KEY:
            if layer.attrib['id'] == layer_id:
                return layer

def isolate_layer(svg_etree, layer_id):
    """Given an svg doc and a single layer, remove all other layer
    elements from the document."""

    keep_layer_id = layer_id

    layer_svg_etree = deepcopy(svg_etree)

    layers = [layer_id for layer_id, layer_label, layer_element
              in get_layers(layer_svg_etree)]

    # get a list of the layers to exclude
    exclude_layer_ids = [layer_id for layer_id in layers
                      if layer_id != keep_layer_id]

    # remove all layer elements that are not this layer
    for exclude_layer_id in exclude_layer_ids:
        exclude_layer = get_layer(layer_svg_etree, exclude_layer_id)
        layer_svg_etree.remove(exclude_layer)

    return layer_svg_etree

def separate_layers(svg_etree):
    """Given an SVG etree doc, make a list of docs each with only a single
    layer in order of the layer stack in inkscape."""

    layer_ids = [layer_id for layer_id, layer_label, layer_element
              in get_layers(svg_etree)]

    single_layer_etrees = []
    for layer_id in layer_ids:
        layer_svg = isolate_layer(svg_etree, layer_id)
        single_layer_etrees.append(layer_svg)

    return single_layer_etrees
