import ast
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
FEATURE_ROOT = PROJECT_ROOT / "app" / "features"


def imported_modules(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    modules: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            modules.add(node.module)
            modules.update(f"{node.module}.{alias.name}" for alias in node.names)
    return modules


def dependency_modules(path: Path, visited: set[Path] | None = None) -> set[str]:
    visited = set() if visited is None else visited
    if path in visited:
        return set()
    visited.add(path)
    modules = imported_modules(path)
    dependencies = set(modules)
    for module in modules:
        if not module.startswith("app."):
            continue
        dependency = PROJECT_ROOT.joinpath(*module.split(".")).with_suffix(".py")
        if dependency.is_file():
            dependencies.update(dependency_modules(dependency, visited))
    return dependencies


def test_business_services_do_not_import_web_or_database_libraries() -> None:
    forbidden = {"fastapi", "starlette", "sqlalchemy", "sqlite3"}
    for service_file in FEATURE_ROOT.glob("*/service.py"):
        dependencies = dependency_modules(service_file)
        assert {module.split(".")[0] for module in dependencies}.isdisjoint(forbidden), service_file
        assert not any(module.startswith("app.db") for module in dependencies), service_file


def test_domain_does_not_import_delivery_or_persistence_libraries() -> None:
    forbidden = {"fastapi", "starlette", "sqlalchemy", "pydantic"}
    for domain_file in (PROJECT_ROOT / "app" / "domain").glob("*.py"):
        assert {m.split(".")[0] for m in dependency_modules(domain_file)}.isdisjoint(forbidden)


def test_repositories_do_not_import_web_framework() -> None:
    forbidden = {"fastapi", "starlette"}
    for repository_file in FEATURE_ROOT.glob("*/repository.py"):
        assert {m.split(".")[0] for m in dependency_modules(repository_file)}.isdisjoint(forbidden)


def test_routers_do_not_import_orm_or_repository_adapters_directly() -> None:
    for api_file in FEATURE_ROOT.glob("*/api.py"):
        imports = imported_modules(api_file)
        assert not any(
            module.startswith(("sqlalchemy", "app.db")) or ".repository" in module
            for module in imports
        ), api_file


def test_features_do_not_import_each_other() -> None:
    for feature_directory in FEATURE_ROOT.iterdir():
        if not feature_directory.is_dir() or feature_directory.name.startswith("_"):
            continue
        for module_file in feature_directory.glob("*.py"):
            for module in imported_modules(module_file):
                if module.startswith("app.features."):
                    assert module.split(".")[2] == feature_directory.name, module_file
