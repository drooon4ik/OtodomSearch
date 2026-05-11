import importlib.util, sys
from pathlib import Path


def load_profile(name: str):
    """Загружает profiles/{name}/config.py и возвращает (модуль, Path к data/)."""
    path = Path(__file__).parent / "profiles" / name / "config.py"
    if not path.exists():
        raise SystemExit(f"Profile not found: {path}")
    spec = importlib.util.spec_from_file_location(f"profile_{name}", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    data_dir = path.parent / "data"
    data_dir.mkdir(exist_ok=True)
    (data_dir / "snapshots").mkdir(exist_ok=True)
    return mod, data_dir


def profile_arg() -> str:
    """Читает --profile=NAME из sys.argv, по умолчанию warsaw-buy."""
    for a in sys.argv:
        if a.startswith("--profile="):
            return a.split("=", 1)[1]
    return "warsaw-buy"
