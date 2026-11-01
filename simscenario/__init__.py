"""sim-scenario-drafter: education-only nursing simulation practice scenario packets.

Everything this package produces is TRAINING MATERIAL for simulation labs and
role-play practice. It is never medical advice, and every rendered artifact
carries a FOR PRACTICE label.

Copyright (c) 2026 Asdale Dynamics, LLC. MIT licensed.
"""

__version__ = "0.1.0"

PRACTICE_BANNER = (
    "FOR PRACTICE - EDUCATION TRAINING MATERIAL ONLY. "
    "THIS SCENARIO IS FICTION. NOT MEDICAL ADVICE. "
    "NEVER USE AS GUIDANCE FOR CARE OF A REAL PATIENT."
)

DISCLAIMER_FOOTER = (
    "This packet is a for-practice artifact drafted for simulation labs, role-play "
    "and skills practice. All patients, statements and details are fictional. "
    "Education only, never medical advice."
)

DEFAULT_FALLBACK_HINT = (
    DISCLAIMER_FOOTER
    + " Drafted from the offline template fallback; pass a config (see "
      "'simscenario config-example') to draft with a local Ollama or any "
      "OpenAI-compatible endpoint instead."
)
