#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
python3 examples/agent_trust_request.py >/tmp/agent_trust_request.json
python3 -m agent_trust.cli --print-contract >/tmp/agent_trust_contract.json
python3 -m agent_trust.cli examples/input.json >/tmp/agent_trust_bundle.json
python3 examples/agent_trust_verify.py
python3 examples/agent_trust_doctor.py
