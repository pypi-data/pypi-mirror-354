import yaml

import sys
import os
from collections


SIMPLE_TYPES = (str, int, float, type(None))
COMPLEX_TYPES = (list, dict)

try:
    from yaml import CSafeLoader as SafeLoader, CSafeDumper as SafeDumper
except ImportError:
    from yaml import SafeLoader, SafeDumper


## Ensure that there are no collision with legacy OrderedDict
## that could be used for omap for instance.
class MyOrderedDict(collections.OrderedDict):
    pass


SafeDumper.add_representer(
    MyOrderedDict,
    lambda cls, data: cls.represent_dict(data.items()))


def construct_omap(cls, node):
    ## Force unfolding reference and merges
    ## otherwise it would fail on 'merge'
    cls.flatten_mapping(node)
    return MyOrderedDict(cls.construct_pairs(node))


SafeLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    construct_omap)


def yaml_dump(value):
    """Returns a representation of values directly usable by bash.

    Literal types are quoted and safe to use as YAML.

    """
    return yaml.dump(value, default_flow_style=False,
                     Dumper=SafeDumper)


load = lambda source: yaml.load(source, Loader=SafeLoader)


class YamlCodec(object):
    encode = yaml_dump
    decode = load