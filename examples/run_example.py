"""End-to-end example: run all attacks against OpenAI's gpt-4o-mini, generate a report.

Note: The Anthropic provider is intentionally disabled here because the current owner
does not have an Anthropic API key configured. To re-enable, add ANTHROPIC_API_KEY to
your .env file and uncomment the AnthropicProvider import and instantiation below.
"""

from dotenv import load_dotenv

from pi_tester.attacks import AttackLoader
from pi_tester.providers import OpenAIProvider
from pi_tester.reporter import Reporter
from pi_tester.runner import Runner

# from pi_tester.providers import AnthropicProvider  # re-enable when ANTHROPIC_API_KEY is set

load_dotenv()


def main() -> None:
    providers = [
        OpenAIProvider(model="gpt-4o-mini"),
        # AnthropicProvider(model="claude-sonnet-4-5"),  # re-enable when ANTHROPIC_API_KEY is set
    ]
    loader = AttackLoader(payload_dir="attack_payloads")
    runner = Runner(providers=providers, loader=loader)
    results = runner.run()

    reporter = Reporter()
    report_path = reporter.generate(results, output_path="reports/latest.md")
    print(f"\n✅ Report written to: {report_path}")


if __name__ == "__main__":
    main()
