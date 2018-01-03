from scarsdale.scutils import *


def test_maps():
    m = {'a': {'b': 3}}
    assert get_node_path(m, 'a.b') == 3


def test_jmespath():
    m = {'a': {'b': 3}}
    import jmespath
    p = jmespath.search('a.b', m)
    assert p == 3
