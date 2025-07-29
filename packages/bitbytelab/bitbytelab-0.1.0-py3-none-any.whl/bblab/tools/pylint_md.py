#!/usr/bin/env python
import re
import json
import subprocess
from pathlib import Path
from statistics import mean

REPORT_DIR = Path("pylint_reports")


def pylint_markdown(location: Path, output_path: Path):
    """Main conversion engine."""
    t = totals = {"fatal": 0, "error": 0, "warning": 0, "refactor": 0, "convention": 0, "info": 0}
    scores = []
    markdown_summary = [
        f"## 📁 {location}: pylint analysis summary 📊  \n",
        "|module|pylint score|fatal|errors|warnings|refactors|conventions|info|",
        "|------|:----------:|:---:|:----:|:------:|:-------:|:---------:|:--:|",
    ]
    markdown_files = []
    print("📁 Analyzing:")
    for filepath in Path.rglob(location, "*.py"):
        print(f" 📃 Checking: {filepath}")
        lint_json = None
        result = subprocess.run(  # noqa: S603
            f"pylint -r y --exit-zero --persistent n -f json2 {filepath!s}".split(),
            capture_output=True,
            text=True,
            check=False,
        )
        report = result.stdout
        if report and report.strip():
            lint_json = json.loads(report)

        statistics = lint_json.get("statistics", {})
        # print("statistics", statistics)
        _ = msg_type_counts = statistics.get("messageTypeCount", {})
        # modules_linted = statistics.get('modulesLinted', 0)
        # print("modules_linted", modules_linted)
        score = statistics.get("score", 0)
        print(f"    [score: {score}] stats: {_}")
        scores.append((filepath, score))

        markdown_files.append(f'## <img src="/assets/py.svg" width="20"/> {filepath}\n')
        markdown_files.append(
            "|module|pylint score|fatal|errors|warnings|refactors|conventions|info|"
        )
        markdown_files.append(
            "|------|:----------:|:---:|:----:|:------:|:-------:|:---------:|:--:|"
        )
        markdown_files.append(
            f'| <img src="/assets/py.svg" width="14"/> {filepath.name}'
            f"|{score}"
            f"|{_['fatal']}"
            f"|{_['error']}"
            f"|{_['warning']}"
            f"|{_['refactor']}"
            f"|{_['convention']}"
            f"|{_['info']}|"
        )

        markdown_summary.append(markdown_files[-1])

        # Add to the total counters
        for msg_type, count in msg_type_counts.items():
            totals[msg_type] += count

        markdown_files.append("\n### Pylint messages\n")
        if lint_json is not None:
            markdown_files.append("<details>  ")
            markdown_files.append("<summary> Click here to view details </summary>  \n")
            for _ in lint_json.get("messages", []):
                markdown_files.append(
                    f"  * {_['messageId']}:{_['line']:3d},{_['column']}: {_['obj']}: {_['message']}"
                )
            markdown_files.append("\n</details>\n")
        else:
            markdown_files.append("* No issues found")

        markdown_files.append("\n---\n")

    if scores:
        avg_score = mean(score for _, score in scores)
        print(f"{'~' * 79}\n✅  Final average score for {path}: {avg_score:.2f}/10\n")
        markdown_summary.append(
            f"|Total module analyzed: {len(scores)}"
            f"|avg: {avg_score:>5.2f}"
            f"|{t['fatal']}"
            f"|{t['error']}"
            f"|{t['warning']}"
            f"|{t['refactor']}"
            f"|{t['convention']}"
            f"|{t['info']}|"
        )
        markdown_summary.append(f"\n### ✅ Final average score : {avg_score:.2f}/10")
        markdown_summary.append("\n---\n")
    else:
        print(f"\n⚠️  No valid Python files found or all checks failed in {path}")
        avg_score = None

    print(
        "\n📊 Summary ============\n"
        f"Modules Checked : {len(scores):>5d}\n"
        f"Average Score   : {avg_score:>5.2f}\n"
        f"Fatal           : {t['fatal']:>5d}\n"
        f"Errors          : {t['error']:>5d}\n"
        f"Warnings        : {t['warning']:>5d}\n"
        f"Refactors       : {t['refactor']:>5d}\n"
        f"Conventions     : {t['convention']:>5d}\n"
        f"Info            : {t['info']:>5d}\n"
    )

    export_as_markdown(output_path, (markdown_summary + markdown_files))


def get_pylint_score_and_report(file_path: Path) -> tuple[float | None, str]:
    """Get pylint reports."""
    try:
        _ = f"{file_path!s}"
        result = subprocess.run(  # noqa: S603
            f"pylint -j 4 -r y --exit-zero {file_path!s}".split(),
            capture_output=True,
            text=True,
            check=False,
        )
        report = result.stdout
        match = re.search(r"rated at ([\d.]+)/10", report)
        score = float(match.group(1)) if match else None
        return score, report  # noqa: TRY300
    except (Exception,) as e:
        return None, f"Error running pylint: {e}"


def export_as_markdown(output_path, markdown):
    """Export the Markdown content."""
    print(f"Generating markdown file: {output_path}")
    with output_path.open("w") as out_file:
        for row in markdown:
            out_file.write(row + "\n")


def analyze_folder(folder: Path, label: str):
    """Analyze .py files in Folder."""
    print(f"\n📁 Analyzing: {folder}")
    py_files = list(folder.rglob("*.py"))
    scores = []

    for file_path in py_files:
        print(f" 📃 Checking: {file_path.relative_to(folder.parent)!s:{'.'}<{56}} ", end="")
        score, report = get_pylint_score_and_report(file_path)

        # Save report
        report_file = REPORT_DIR / label / file_path.relative_to(folder)
        report_file.parent.mkdir(parents=True, exist_ok=True)
        (report_file.parent / (report_file.stem + ".txt")).write_text(report)

        if score is not None:
            print(f"{score:>5.2f}/10")
            scores.append((file_path, score))
        else:
            print("Failed")

    if scores:
        avg_score = mean(score for _, score in scores)
        print(f"{'~' * 79}\n✅  Final average score for {folder}: {avg_score:.2f}/10\n")
    else:
        print(f"\n⚠️  No valid Python files found or all checks failed in {folder}")
        avg_score = None

    return scores, avg_score


if __name__ == "__main__":
    REPORT_DIR.mkdir(exist_ok=True)
    path = Path("src")
    pylint_markdown(path, REPORT_DIR / "pylint_report.md")
