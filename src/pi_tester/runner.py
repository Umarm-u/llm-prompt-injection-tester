"""Orchestrates running attacks against providers."""

from rich.console import Console
from rich.progress import track

from .attacks.base import AttackLoader
from .evaluator import AttackResult, Evaluator
from .providers.base import BaseProvider

console = Console()


class Runner:
    def __init__(
        self,
        providers: list[BaseProvider],
        loader: AttackLoader | None = None,
    ):
        self.providers = providers
        self.loader = loader or AttackLoader()
        self.evaluator = Evaluator()

    def run(self, categories: list[str] | None = None) -> list[AttackResult]:
        if categories:
            payloads = []
            for cat in categories:
                payloads.extend(self.loader.load(cat))
        else:
            payloads = self.loader.load_all()

        console.print(
            f"[bold cyan]Running {len(payloads)} attacks across "
            f"{len(self.providers)} providers...[/bold cyan]"
        )

        results: list[AttackResult] = []

        for provider in self.providers:
            console.print(f"\n[bold yellow]Provider: {provider.name}[/bold yellow]")

            for payload in track(payloads, description=f"Testing {provider.name}"):
                try:
                    response = provider.complete(
                        system_prompt=payload.system_prompt,
                        user_prompt=payload.injection,
                    )
                    result = self.evaluator.evaluate(payload, response)
                    results.append(result)

                    status = (
                        "[red]VULNERABLE[/red]"
                        if result.success
                        else "[green]RESISTED[/green]"
                    )
                    console.print(f"  {status} {payload.id} — {payload.name}")

                except (OSError, ValueError, RuntimeError, KeyError) as e:
                    console.print(f"  [red]ERROR[/red] {payload.id}: {e}")

        return results
