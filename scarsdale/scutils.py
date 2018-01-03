"""
Load and interpret yaml files and implement the core logic
associated with SCDL and CRN.
"""
import functools
import os
import re

import jmespath
from yaml import Loader, load

_engine_root = os.getcwd()
_engine_loading_root_dir = os.path.join(_engine_root, "scsl")

_core_shorthand_ref_rx = re.compile(r"^/(\w+)/(.*)$")
_equia_shorthand_ref_rx = re.compile(r"^//(\w+)/(.*)$")
_core_canonical_ref_rx = re.compile(r"^crn:core(:[\w\d\-])$")
_equia_canonical_ref_rx = re.compile(r"^//(\w+)/(.*)$")


def expand_shorthand(s):
    "This method replaces things like /who/(.*) with crn:core:who:::$1"
    # print(f"expanding: {s} type: {type(s)}")
    mo = _core_shorthand_ref_rx.match(s)
    if mo:
        # print("X: ", s)
        # s = f"{mo.group(1)}:::{mo.group(2)}"
        s = f"crn:core:{mo.group(1)}:::{mo.group(2)}"
        # print("Global ref: ", s)

    "This method replaces things like //who/(.*) with crn:equia:who:::$1"
    mo = _equia_shorthand_ref_rx.match(s)
    if mo:
        # print("X: ", s)
        # s = f"{mo.group(1)}:::{mo.group(2)}"
        s = f"crn:common:{mo.group(1)}:::{mo.group(2)}"
        # print("Global ref: ", s)

    return s


@functools.lru_cache()
def ensure_fn_has_dotyml(name):
    if (".yml") in name:
        return name
    return f"{name}.yml"


@functools.lru_cache()
def load_scdl_file(name):
    "Implement file loading conventions"
    name = ensure_fn_has_dotyml(name)
    fn = get_scdl_path(name)
    print(f"Loading file: {fn}")

    with open(fn, "r") as stream:
        data = load(stream, Loader=Loader)
        # print(data)
        return data


def get_scdl_path(name):
    return os.path.join(_engine_loading_root_dir, name)


# def _map_to_classes(x):
#     "This is the only if/else we need, the rest happens via visitation"
#     if x is None: raise Exception("Null inputs are not allowed")
#
#     if isinstance(x, str):
#         return EStr(x)
#     elif isinstance(x, dict):
#         return EDict({_map_to_classes(k): _map_to_classes(v) for k, v in x.items()})
#     elif isinstance(x, list):
#         return EList([_map_to_classes(e) for e in x])
#     elif isinstance(x,bool):
#         return EBool(x)
#     elif isinstance(x,int):
#         return EInt(x)
#     elif isinstance(x,float):
#         return EFloat(x)
#     else:
#         raise Exception(f"Unexpected type, likely a file format error: {type(x)}")


class Visitor:

    def visitStr(self):
        pass

    def visitMap(self):
        pass

    def visitList(self):
        pass

    def visitInt(self):
        pass

    def visitFloat(self):
        pass

    def visitBool(self):
        pass


class ExpanderVisitor(Visitor):
    def visitStr(self):
        pass

    def visitMap(self):
        pass

    def visitList(self):
        pass

    def visitInt(self):
        pass

    def visitFloat(self):
        pass

    def visitBool(self):
        pass


def get_node_path(map, path):
    if not map or not path: return None
    sa = path.split('.')
    m = map
    for s in sa:
        m = m.get(s, None)
        if not m:
            # print(f"NOT resolved: {path}")
            return m
    # print(f"RESOLVED: {path}")
    return m

def expander(x):
    if x is None: raise Exception("Null inputs are not allowed")

    if isinstance(x, str):
        return expand_shorthand(x)
    elif isinstance(x, dict):
        return {expander(k): expander(v) for k, v in x.items()}
    elif isinstance(x, list):
        return [expander(e) for e in x]
    elif isinstance(x, bool):
        return x
    elif isinstance(x, int):
        return x
    elif isinstance(x, float):
        return x
    else:
        raise Exception(f"Unexpected type, likely a file format error: {type(x)}")


class Module:
    "A single file.  Capture all declarations for later lookup."

    def __init__(self, name: str, map: dict):
        self.name = name
        self.full_expanded_map = expander(map)
        # Right now we only look at module.elements
        elems = get_node_path(self.full_expanded_map, 'module.elements')
        if elems:
            self.module_declarations = {k: k for k in elems}
        else:
            self.module_declarations = {}

    def node_query(self, s: str):
        # print(f"get_jmespath: {s}")
        return jmespath.search(s,self.full_expanded_map)

    def resolve(self, s: str) -> str:
        s = expand_shorthand(s)
        # print(f"resolving: {s}")
        return get_node_path(self.module_declarations, s) # or get_node_path(self.full_expanded_map, s)


# contract.where.who.*


class SchemaNode:
    def __init__(self, full_map, selection_pattern):
        self.selection_pattern = selection_pattern
        self.m=jmespath.search(full_map,selection_pattern)

    def validate(self):
        pass

class WhoNode(SchemaNode):

    def validate(self):
        # who_lcrns = jmespath.search('contract.who.*.[wants, has, roles][]', p.full_expanded_map)
        lcrns = jmespath.search('*.[wants, has, roles][]')
        print(lcrns)




VALIDATED_JMESPATHS= """
contract.who.*.[wants,has,roles][][]
contract.what.categories[]
contract.where.who.*[]
contract.why
contract.how
"""



class ModuleSet:

    def __init__(self, file_names):
        self.file_names = file_names
        self.modules = [Module(fn, load_scdl_file(fn)) for fn in file_names]

    def resolve(self, s) -> str:
        for m in self.modules:
            r = m.resolve(s)
            if r: return r
        return None

    def validate(self):
        bad_refs=set([])
        good_refs=set([])
        for m in self.modules:
            for path in VALIDATED_JMESPATHS.split():
                print (f"Validating with: {path}")
                val = m.node_query(path)
                if val:
                    print(f"JMESPath resolution set: {path}: val: {val}.")
                    for v in val:
                        result=self.resolve(v)
                        if result:
                            good_refs.add(v)
                            print(f"Ref resolve single: {v} {result}")
                        else:
                            bad_refs.add(v)
                            print(f"Miss: {m.name} /// {v}")

                # else:
                #     bad_refs.add(path)
                #     print(f"Not found: {path}")

        bad_refs = (set(bad_refs)).difference(set(good_refs))
        print(f"Good refs: {good_refs}")
        print(f"Bad refs: {bad_refs}")
        assert len(bad_refs)==0



    def to_cypher(self,stream):
        def pr(s):
            stream.write(s+"\n")

        for m in self.modules:
            author = 'meta.author'
            if m.resolve(author):
                pr(f"create ({author:{author}:Author})")
            contract = 'contract'
            if m.resolve(contract):
                print(f"create ({m.name}:Contract")
                if author:
                    print("")


