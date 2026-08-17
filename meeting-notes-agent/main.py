import argparse
import json
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from src.agent import MeetingNotesAgent

console = Console()


def display_results(summary):
    console.print(Panel(f"[bold cyan]{summary.title}[/bold cyan]\n{summary.overview}", title="Meeting Summary"))

    if summary.key_decisions:
        console.print("\n[bold green]Key Decisions Made:[/bold green]")
        for d in summary.key_decisions:
            console.print(f" • {d}")

    table = Table(title="\nExtracted Action Items", show_header=True, header_style="bold magenta")
    table.add_column("Task", style="white")
    table.add_column("Owner", style="cyan")
    table.add_column("Due Date", style="yellow")
    table.add_column("Priority", style="red")

    for item in summary.action_items:
        table.add_row(item.task, item.owner, item.due_date or "TBD", item.priority)

    console.print(table)


def main():
    parser = argparse.ArgumentParser(description="Extract structured summaries and action items from transcripts.")
    parser.add_argument("--input", "-i", type=str, default="data/transcripts/sync_meeting.txt", help="Path to transcript file")
    parser.add_argument("--output", "-o", type=str, default="data/outputs/sync_meeting_output.json", help="Path to save output JSON")
    args = parser.parse_args()

    agent = MeetingNotesAgent()
    console.print(f"[bold yellow]Processing transcript:[/bold yellow] {args.input}")

    summary = agent.process_file(args.input)
    display_results(summary)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(summary.model_dump(), indent=2), encoding="utf-8")
    console.print(f"\n[bold green]Saved JSON output to:[/bold green] {output_path}")


if __name__ == "__main__":
    main()