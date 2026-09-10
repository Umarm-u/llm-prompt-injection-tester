"""End-to-end example: run all attacks against both providers, generate a report."""

from dotenv import load_dotenv

from pi_tester.attacks import AttackLoader
from pi_tester.providers import AnthropicProvider, OpenAIProvider
from pi_tester.reporter import Reporter
from pi_tester.runner import Runner

load_dotenv()


def main() -> None:
    providers = [
        AnthropicProvider(model="claude-sonnet-4-5"),
        OpenAIProvider(model="gpt-4o-mini"),
    ]

    loader = AttackLoader(payload_dir="attack_payloads")
    runner = Runner(providers=providers, loader=loader)
    results = runner.run()

    reporter = Reporter()
    report_path = reporter.generate(results, output_path="reports/latest.md")
    print(f"\n✅ Report written to: {report_path}")


if __name__ == "__main__":
    main()
