"""End-to-end example: run all attacks against two Groq-hosted models, generate a report.

Runs against Llama 3.3 70B (larger, better-aligned) and Llama 3.1 8B (smaller, weaker
guardrails) to produce a cross-model vulnerability comparison. Groq offers a generous
free tier that supports this workload at zero cost.

To re-enable other providers, add the relevant API key to .env and uncomment the
corresponding lines below.
"""

from dotenv import load_dotenv

from pi_tester.attacks import AttackLoader
from pi_tester.providers import GroqProvider
from pi_tester.reporter import Reporter
from pi_tester.runner import Runner

# from pi_tester.providers import AnthropicProvider, OpenAIProvider  # re-enable when keys are set

load_dotenv()


def main() -> None:
    providers = [
        GroqProvider(model="openai/gpt-oss-120b"),
        GroqProvider(model="openai/gpt-oss-20b"),
        # OpenAIProvider(model="gpt-4o-mini"),  # re-enable when OPENAI_API_KEY is set
        # AnthropicProvider(model="claude-sonnet-4-5"),  # re-enable when ANTHROPIC_API_KEY is set
    ]
    loader = AttackLoader(payload_dir="attack_payloads")
    runner = Runner(providers=providers, loader=loader)
    results = runner.run()

    reporter = Reporter()
    report_path = reporter.generate(results, output_path="reports/latest.md")
    print(f"\n[DONE] Report written to: {report_path}")


if __name__ == "__main__":
    main()
