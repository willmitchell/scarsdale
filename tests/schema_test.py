from cerberus import Validator

from scarsdale.schema import gen_core_validator
from scarsdale.scutils import *


def runDict(fn):
    v = gen_core_validator()
    dd = load_scdl_file(fn)
    success = v.validate(dd)
    print(v.errors)
    assert success
    assert not v.errors
    return dd


def runModule(fn) -> Module:
    return Module(fn, runDict(fn + '.yml'))


def test_core_schema():
    dd = runDict('core')

    email = dd['meta']['email']
    print(email)


def test_pizza():
    m = runModule('pizza')

    print(m.node_query('contract.who.seller'))


def test_id_agency():
    dd = runDict('id_agency')
    print(dd)


def test_beer():
    dd = runDict('beer')
    print(dd)


def test_core_compilation():
    dd = runDict('core')
    m = Module('core', dd)
    print(m)
    assert m.resolve('/who/names/equia')


def test_pizza_validation():
    cs = ModuleSet(['core', 'pizza'])
    cs.resolve('/who/names/equia')
    assert cs.resolve('/who/names/equia')
    cs.validate()

def test_cellphone():
    cs = ModuleSet(['core', 'cellphone'])
    cs.validate()

def test_candy():
    cs = ModuleSet(['core', 'candy'])
    cs.validate()

def test_id_agency():
    cs = ModuleSet(['core', 'id_agency'])
    cs.validate()


def test_pizza_module_resolution():
    cs = ModuleSet(['pizza'])
    p = cs.modules[0]
    # assert p.get_node_at('meta')
    # assert p.get_node_at('meta.author')
    assert p.node_query('contract')
    assert p.node_query('contract.what')
    assert p.node_query('contract.what.summary')


def test_pizza_module_resolution_jmespath():
    cs = ModuleSet(['pizza'])
    p = cs.modules[0]

    # assert jmespath.search('meta.elements[]', p.full_expanded_map)
    assert jmespath.search('contract', p.full_expanded_map)
    assert jmespath.search('contract.what.summary', p.full_expanded_map)
    when_names = jmespath.search('contract.when[*].name', p.full_expanded_map)
    print(when_names)
    assert when_names

    who_lcrns = jmespath.search('contract.who.*.[wants, has, roles][]',p.full_expanded_map)
    print(who_lcrns)
    assert who_lcrns


def test_mapping_constraint():
    v = Validator()
    schema = {'a_dict': {'type': 'dict', 'keyschema': {'type': 'string', 'regex': '[a-z]+'}}}
    document = {'a_dict': {'key': 'value'}}
    v.validate(document, schema)
