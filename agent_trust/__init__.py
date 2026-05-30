"""Agent Trust: local pre-action trust bundles for autonomous agents.

No network calls, no wallet access, and no tool execution are performed by the
core bundle builder.
"""

from agent_trust.bundle import (
    AGENT_TRUST_BUNDLE_CONTRACT_VERSION,
    SUPPORTED_AGENT_TRUST_BUNDLE_CONTRACT_VERSIONS,
    build_agent_trust_bundle,
)

__all__ = [
    "AGENT_TRUST_BUNDLE_CONTRACT_VERSION",
    "SUPPORTED_AGENT_TRUST_BUNDLE_CONTRACT_VERSIONS",
    "build_agent_trust_bundle",
]
