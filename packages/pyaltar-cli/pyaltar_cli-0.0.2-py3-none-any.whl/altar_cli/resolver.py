import ast
from collections import deque
from pathlib import Path
from urllib.request import Request, urlopen

from rich.console import Console

BASE_URL = "https://raw.githubusercontent.com/pyaether/altar-ui/refs/{version_slug}/src/altar_ui/{component_name}.py"


def _get_dependent_components(component_file_content: str) -> list[str]:
    tree = ast.parse(component_file_content)
    dependent_components = [
        node.module
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom)
        if node.level > 0
        if node.module
    ]
    return dependent_components


def resolve_component_dependencies(
    console: Console,
    components: tuple[str],
    component_dir: Path,
    version_slug: str,
    verbose: bool = False,
) -> None:
    resolved_components: set[str] = set()
    components_to_process: deque[str] = deque(components)

    while components_to_process:
        component_name = components_to_process.popleft()
        if component_name in resolved_components:
            if verbose:
                console.print(
                    f"[dim]Component '{component_name}' already resolved. Skipping.[/dim]"
                )
            continue

        component_path = component_dir / f"{component_name}.py"
        if component_path.exists():
            with open(component_path, encoding="utf-8") as file:
                component_file_content = file.read()

            resolved_components.add(component_name)
            if verbose:
                console.print(
                    f"[dim][green]Component '{component_name}' found in the project.[/green][/dim]"
                )
        else:
            if verbose:
                console.print(
                    f"[yellow]Component '{component_name}' not found in the project. Downloading...[/yellow]"
                )
            component_url = BASE_URL.format(
                version_slug=version_slug, component_name=component_name
            )

            request = Request(component_url)  # noqa: S310
            with urlopen(request) as response:  # noqa: S310
                component_file_content = response.read().decode("utf-8")

            with open(component_path, "w") as file:
                file.write(component_file_content)

            resolved_components.add(component_name)
            if verbose:
                console.print(
                    f"[green]Successfully downloaded '{component_name}'.[/green]"
                )

        if component_file_content:
            dependent_components = _get_dependent_components(component_file_content)
            if dependent_components:
                if verbose:
                    console.print(
                        f"[cyan]'{component_name}' depends on: {', '.join(dependent_components)}[/cyan]"
                    )
                for components in dependent_components:
                    if (
                        components not in resolved_components
                        and components not in components_to_process
                    ):
                        components_to_process.append(components)

    return resolved_components
