import sys
from scan import infer_permissions
from diff import manifest_diff
from review import explain

def vet(path: str, task: str):
    code = open(path).read()
    perms = infer_permissions(code)
    violations = manifest_diff(task, perms)

    print(f"\n=== Vetting {path} (task: {task}) ===")
    print("Inferred:", perms)

    if not violations:
        print("✅ APPROVED — within task permissions")
        return

    print("🛑 REJECTED — exceeds task permissions:", violations)
    print("\nNemotron review:\n" + explain(code, violations))

if __name__ == "__main__":
    vet(sys.argv[1], sys.argv[2])