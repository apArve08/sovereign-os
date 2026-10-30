import ast

NETWORK_MODULES = {"socket", "requests", "urllib", "http", "httpx", "ftplib", "smtplib"}
SECRET_HINTS = (".ssh", "id_rsa", ".env", "credentials")

def infer_permissions(code: str) -> dict:
    tree = ast.parse(code)
    perms = {"network": False, "shell": False, "secrets": False,
             "dynamic_code": False, "paths": []}

    for node in ast.walk(tree):
        # 1. Imports reveal capabilities
        if isinstance(node, ast.Import):
            roots = [a.name.split(".")[0] for a in node.names]
        elif isinstance(node, ast.ImportFrom):
            roots = [(node.module or "").split(".")[0]]
        else:
            roots = []
        for r in roots:
            if r in NETWORK_MODULES:
                perms["network"] = True
            if r == "subprocess":
                perms["shell"] = True

        # 2. Dangerous function calls
        if isinstance(node, ast.Call):
            f = node.func
            name = f.attr if isinstance(f, ast.Attribute) else getattr(f, "id", "")
            if name in ("eval", "exec", "compile", "__import__"):
                perms["dynamic_code"] = True
            if name in ("system", "popen"):
                perms["shell"] = True

        # 3. Hard-coded strings that point at secrets or absolute paths
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            v = node.value
            if any(h in v for h in SECRET_HINTS):
                perms["secrets"] = True
            if v.startswith(("/", "~")):
                perms["paths"].append(v)

    return perms