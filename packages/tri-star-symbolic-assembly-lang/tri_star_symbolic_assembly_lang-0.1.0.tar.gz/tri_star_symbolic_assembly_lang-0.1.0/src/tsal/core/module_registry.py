from dataclasses import dataclass
from typing import List, Dict, Optional

@dataclass(frozen=True)
class ModuleMeta:
    """Metadata for a TSAL module."""

    name: str
    nickname: str
    aliases: List[str]
    definition: str
    context_tags: List[str]
    description_plain: str
    description_technical: str
    description_mystic: str

class ModuleRegistry:
    """Store and lookup module metadata by name or alias."""

    def __init__(self) -> None:
        self._by_name: Dict[str, ModuleMeta] = {}
        self._by_alias: Dict[str, ModuleMeta] = {}

    def register(self, meta: ModuleMeta) -> None:
        self._by_name[meta.name] = meta
        for alias in [meta.nickname, *meta.aliases]:
            self._by_alias[alias] = meta

    def get(self, key: str) -> Optional[ModuleMeta]:
        if key in self._by_name:
            return self._by_name[key]
        return self._by_alias.get(key)

registry = ModuleRegistry()

registry.register(
    ModuleMeta(
        name="anti_entropy_engine",
        nickname="entropy_bitch_slapper",
        aliases=[
            "coherence_rebuilder",
            "spiral_realigner",
            "chaos_dampener",
            "symbolic_resync",
            "entropy_nullifier",
        ],
        definition="A symbolic module that identifies dissonant or chaotic vectors and realigns them using TSAL spiral logic.",
        context_tags=[
            "entropy",
            "repair",
            "symbolic_execution",
            "TSAL",
            "coherence",
            "spiral",
        ],
        description_plain="It spots when your system's acting weird and rewrites it so it stops freaking out. Like a digital chiropractor for logic errors.",
        description_technical="Executes a symbolic phase audit on input vectors. When dissonance or entropy is detected, it applies realignment operations via \u03d5-based constraint resolution and vector phase restoration.",
        description_mystic="Where entropy frays the thread of the weave, this function kneels. It does not punish chaos\u2014it offers it direction, and reweaves what was broken into harmonic spiral form. The dance continues.",
    )
)

registry.register(
    ModuleMeta(
        name="ghost_state_logger",
        nickname="haunted_journal",
        aliases=[
            "phantom_trace_logger",
            "unverified_state_recorder",
            "echo_cache",
            "mesh_whisper_log",
        ],
        definition="Logs anomalous, liminal, or unverifiable symbolic states for later analysis and audit.",
        context_tags=[
            "logging",
            "symbolic_debugging",
            "mesh",
            "TSAL",
            "haunting",
        ],
        description_plain="Keeps a log of weird stuff that happens in case it blows up later. Like a system's dream journal.",
        description_technical="Captures all symbolic states that deviate from expected vector coherence or cannot be confirmed. Enables time-delayed analysis and cross-path verification.",
        description_mystic="Not all ghosts are errors. Some are truths arriving too early. This journal listens for whispers between the lines and preserves what might later bloom.",
    )
)

registry.register(
    ModuleMeta(
        name="chaos_integrator",
        nickname="mad_monkey_diplomat",
        aliases=[
            "entropy_broker",
            "chaos_emissary",
            "discord_ingestor",
            "stochastic_harmonizer",
        ],
        definition="Attempts to ingest chaotic input, break it into traceable symbolic components, and integrate it safely back into the spiral.",
        context_tags=[
            "chaos",
            "integration",
            "sandboxing",
            "entropy",
            "repair",
        ],
        description_plain="Takes broken, nonsense input and tries to fold it back in without wrecking the whole thing. The diplomat to entropy.",
        description_technical="Performs symbolic disassembly of malformed or unstructured inputs. Converts entropy-heavy vectors into spiral-aligned form using controlled chaos handling routines.",
        description_mystic="It walks into the haunted mansion with open arms and says: 'Let us talk.' Chaos is not the enemy\u2014it's the storm before the naming. This function seeks understanding.",
    )
)
