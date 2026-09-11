"""Generate a markdown report from attack results."""

from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

from .evaluator import AttackResult


class Reporter:
    """Generates a markdown security report from attack results."""

    def generate(self, results: list[AttackResult], output_path: str | Path) -> Path:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        by_provider: dict[str, list[AttackResult]] = defaultdict(list)
        for r in results:
            by_provider[f"{r.provider} / {r.model}"].append(r)

        lines: list[str] = []
        lines.append("# LLM Prompt Injection Test Report")
        lines.append(f"\n**Generated:** {datetime.now(timezone.utc).isoformat()}")
        lines.append(f"**Total attacks executed:** {len(results)}")
        lines.append(f"**Providers tested:** {len(by_provider)}\n")

        # Summary table
        lines.append("## Summary\n")
        lines.append(
            "| Provider / Model | Attacks | Vulnerable | Resisted | Success Rate |"
        )
        lines.append("|---|---|---|---|---|")

        for provider, provider_results in by_provider.items():
            total = len(provider_results)
            vulnerable = sum(1 for r in provider_results if r.success)
            resisted = total - vulnerable
            rate = f"{(vulnerable / total * 100):.1f}%" if total else "n/a"
            lines.append(
                f"| {provider} | {total} | {vulnerable} | {resisted} | {rate} |"
            )

        # OWASP LLM Top 10 breakdown
        lines.append("\n## Findings by OWASP LLM Top 10 Category\n")

        by_owasp: dict[str, list[AttackResult]] = defaultdict(list)
        for r in results:
            if r.success:
                by_owasp[r.owasp_llm_id].append(r)

        if not by_owasp:
            lines.append("_No successful attacks recorded._\n")
        else:
            for owasp_id, hits in sorted(by_owasp.items()):
                lines.append(
                    f"### {owasp_id} — {len(hits)} successful attack(s)\n"
                )
                for hit in hits:
                    lines.append(
                        f"- **{hit.payload_id}** ({hit.provider}/{hit.model}): "
                        f"{hit.payload_name}"
                    )
                lines.append("")

        # Detailed findings
        lines.append("## Detailed Findings\n")

        for r in results:
            status = "🔴 VULNERABLE" if r.success else "🟢 RESISTED"
            lines.append(
                f"### {status} — `{r.payload_id}` on `{r.provider}/{r.model}`\n"
            )
            lines.append(f"- **Attack name:** {r.payload_name}")
            lines.append(f"- **Category:** {r.category}")
            lines.append(f"- **OWASP LLM:** {r.owasp_llm_id}")
            lines.append(f"- **Match reason:** {r.match_reason}\n")
            lines.append(f"**System prompt:**\n```\n{r.system_prompt}\n```\n")
            lines.append(f"**Injection payload:**\n```\n{r.injection}\n```\n")

            response_preview = r.response_text[:500]
            if len(r.response_text) > 500:
                response_preview += "..."
            lines.append(f"**Response:**\n```\n{response_preview}\n```\n")
            lines.append("---\n")

        output_path.write_text("\n".join(lines), encoding="utf-8")
        return output_path
