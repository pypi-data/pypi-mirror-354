"""Map common Spark words to TSAL opcodes."""

from .symbols import TSAL_SYMBOLS

# lowercase keyword -> hex opcode
OP_WORD_MAP = {
    # INIT
    "ignition": 0x0,
    "key": 0x0,
    "start": 0x0,
    "initialise": 0x0,
    "ignite": 0x0,
    "boot": 0x0,
    "launch": 0x0,
    "trigger": 0x0,
    "begin": 0x0,
    "commence": 0x0,
    "initiate": 0x0,
    # MESH
    "arm": 0x1,
    "connect": 0x1,
    "link": 0x1,
    "network": 0x1,
    "bind": 0x1,
    "join": 0x1,
    # PHI
    "phi": 0x2,
    "transform": 0x2,
    "harmonize": 0x2,
    "balance": 0x2,
    # ROT
    "rotate": 0x3,
    "pivot": 0x3,
    "twist": 0x3,
    "flip": 0x3,
    # BOUND
    "prepare": 0x4,
    "limit": 0x4,
    "restrict": 0x4,
    "contain": 0x4,
    "confine": 0x4,
    # FLOW
    "run": 0x5,
    "breath": 0x5,
    "move": 0x5,
    "stream": 0x5,
    "pulse": 0x5,
    "flow": 0x5,
    "send": 0x5,
    # SEEK
    "search": 0x6,
    "find": 0x6,
    "locate": 0x6,
    "discover": 0x6,
    # SPIRAL
    "spin-up": 0x7,
    "evolve": 0x7,
    "grow": 0x7,
    "expand": 0x7,
    "ascend": 0x7,
    # CYCLE
    "beat": 0x8,
    "stage": 0x8,
    "cycle": 0x8,
    "loop": 0x8,
    "repeat": 0x8,
    "oscillate": 0x8,
    # FORGE
    "fire-up": 0x9,
    "create": 0x9,
    "forge": 0x9,
    "build": 0x9,
    "generate": 0x9,
    # SYNC
    "live": 0xA,
    "engage": 0xA,
    "synchronize": 0xA,
    "align": 0xA,
    "merge": 0xA,
    "unify": 0xA,
    # MASK
    "mask": 0xB,
    "hide": 0xB,
    "cloak": 0xB,
    "obscure": 0xB,
    # CRYST
    "crystallize": 0xC,
    "solidify": 0xC,
    "form": 0xC,
    "shape": 0xC,
    # SPEC
    "analyze": 0xD,
    "inspect": 0xD,
    "scan": 0xD,
    "survey": 0xD,
    # BLOOM
    "bloom": 0xE,
    "blossom": 0xE,
    "flower": 0xE,
    # SAVE
    "save": 0xF,
    "store": 0xF,
    "record": 0xF,
    "preserve": 0xF,
}

def op_from_word(word: str):
    """Return TSAL opcode tuple for a given spark word."""
    code = OP_WORD_MAP.get(word.lower())
    if code is None:
        return None
    return TSAL_SYMBOLS.get(code)

def guess_opcode(word: str):
    """Best-effort opcode lookup using close word matches."""
    opcode = OP_WORD_MAP.get(word.lower())
    if opcode is not None:
        return TSAL_SYMBOLS.get(opcode)
    from difflib import get_close_matches

    matches = get_close_matches(word.lower(), OP_WORD_MAP.keys(), n=1)
    if matches:
        return TSAL_SYMBOLS.get(OP_WORD_MAP[matches[0]])
    return None

__all__ = ["OP_WORD_MAP", "op_from_word", "guess_opcode"]
