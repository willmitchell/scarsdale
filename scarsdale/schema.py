"""
Build Cerberus schema for SCDL.
"""
from cerberus import Validator

# Global patterns and types

TS = {'type': 'string'}
TB = {'type': 'boolean'}
TD = {'type': 'dict'}
TL = {'type': 'list'}
RX_EMAIL = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
TS_EMAIL = {'type': 'string', 'regex': RX_EMAIL}

STS = {'schema': TS}

TLS = {**TL, **STS}

RX_ANY_CRN = r'/+[\w\-\_]+/[/\w\-\_]*|crn:\w+:\w*:[\w\-\_]+:\d*:[\-\_/\:\w]+'
TCRN = {
    'schema': {
        'type': 'string',
        'regex': RX_ANY_CRN,
    }
}
TLCRN = {
    **TL,
    **TCRN
}


def dods(d):
    "Constrain the schema of mappings within a mapping"
    return {
        **TD,
        'valueschema': {
            **TD,
            'schema': d
        }
    }


def dolcrn(d):
    "Constrain the schema of mappings within a mapping"
    return {
        **TD,
        'schema': {
            'type': 'string',
            'regex': RX_ANY_CRN,
        }
    }


def lods(d):
    "Constrain the schema of mappings within a list"
    return {
        **TL,
        'schema': {
            **TD,
            'schema': d
        }
    }


def gen_core_validator():
    TMETA = {
        **TD,
        'schema': {
            'author': TS,
            'org': TS,
            'email': TS_EMAIL,
            'version': TS,
            'dependencies': TLS,
            'hash': TS,
        },
    }

    TMODULE = {
        **TD,
        'schema': {
            'name': TS,
            'description': TS,
            'readonly': TB,
            'elements': TLCRN,
        },
    }

    TWHO = dods({
        'name': TS,
        'roles': TLCRN,
        'wants': TLCRN,
        'has': TLCRN,
        'behaviors': TLCRN
    })

    TWHAT = {
        **TD,
        'schema': {
            'summary': TS,
            'categories': TLCRN,
        }
    }

    TWHERE = {
        **TD,
        'schema': {
            'jurisdiction': TS,
            'who': {
                **TD,
                'valueschema': TLCRN
            }
        }
    }

    TWHEN = lods({
        'name': TS,
        'who': lods({
            'name': TS,
            'actions': TLCRN,
        })
    })

    TCONTRACT = {
        **TD,
        'schema': {
            'name': TS,
            'description': TS,
            'who': TWHO,
            'what': TWHAT,
            'where': TWHERE,
            'when': TWHEN,
            'why': TLCRN,
            'how': TLCRN,
        },
    }

    schema = {'meta': TMETA, 'module': TMODULE, 'contract': TCONTRACT, }
    v = Validator(
        schema,
        allow_unknown=False

    )

    return v
