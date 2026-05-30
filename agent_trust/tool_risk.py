"""Constants for local non-executing tool/MCP risk attestations."""

RISK_ORDER = {"LOW": 0, "MEDIUM": 1, "HIGH": 2, "BLOCK": 3}
RISK_LABELS = tuple(RISK_ORDER)
NETWORK_KEYS = {"url", "base_url", "endpoint", "server_url", "transport", "network", "host"}
AUTH_KEYS = {"auth", "auth_type", "api_key", "token", "bearer", "secret", "credentials", "env", "env_vars"}
FS_KEYS = {"filesystem", "fs", "path", "paths", "roots", "workspace", "write", "delete"}
EXEC_KEYS = {"shell", "exec", "execute", "subprocess", "command", "commands", "python", "node", "docker"}
DANGEROUS_WORDS = {"shell", "subprocess", "exec", "execute", "delete", "write", "wallet", "private key", "credential", "browser", "network", "http", "sse", "websocket", "docker", "filesystem"}
