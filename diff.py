import yaml

POLICY = yaml.safe_load(open("policy.yaml"))

def manifest_diff(task: str, perms: dict) -> list[str]:
    allowed = POLICY[task]
    return [k for k, ok in allowed.items() if perms.get(k) and not ok]