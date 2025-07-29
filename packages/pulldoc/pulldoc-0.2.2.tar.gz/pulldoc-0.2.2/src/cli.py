import typer

from src.logger import get_project_logger
from src.service.collector import fetch_prs
from src.service.summarizer import create_final_summary, summarize_prs

logger = get_project_logger("cli")
app = typer.Typer(
    add_completion=False,
)


@app.command(
    help="Collect PR data and save to file",
    context_settings={
        "allow_extra_args": True,
        "ignore_unknown_options": True,
    },
)
def collect(
    ctx: typer.Context,
    repo: str = typer.Argument(..., help="org/repo format"),
    start: int = typer.Option(None, "--start", help="Start PR number"),
    end: int = typer.Option(None, "--end", help="End PR number"),
):
    """Collect PR data and save to file"""
    try:
        fetch_prs(
            org_repo=repo,
            start=start,
            end=end,
        )

    except Exception:
        raise typer.Exit(1)


@app.command(
    help="Summarize PR data",
    context_settings={
        "allow_extra_args": True,
        "ignore_unknown_options": True,
    },
)
def summarize(
    ctx: typer.Context,
    repo: str = typer.Argument(..., help="org/repo format"),
    model: str = typer.Option("gpt-4o-mini", "--model", help="LLM model name to use"),
    custom_prompt: str = typer.Option("", "--custom-prompt", help="Custom prompt"),
    language: str = typer.Option("en", "--lang", help="Summary language"),
    only_total: bool = typer.Option(
        False, "--only-total", help="Generate only the final summary"
    ),
) -> dict:
    """Summarize PR data"""
    try:
        if only_total:
            usage = create_final_summary(
                repo_name=repo,
                model=model,
                custom_prompt=custom_prompt,
                language=language,
            )
        else:
            usage = summarize_prs(
                repo_name=repo,
                model=model,
                custom_prompt=custom_prompt,
                language=language,
                batch_size=10,
            )
            final_usage = create_final_summary(
                repo_name=repo,
                model=model,
                custom_prompt=custom_prompt,
                language=language,
            )
            for key in usage:
                usage[key] += final_usage[key]

        return usage

    except Exception as e:
        logger.error(f"Error occurred during summarization: {e}")
        raise typer.Exit(1)



@app.command(
    help="Execute PR data collection and summarization in one go (individual summaries + final summary)",
    context_settings={
        "allow_extra_args": True,
        "ignore_unknown_options": True,
    },
)
def run(
    ctx: typer.Context,
    repo: str = typer.Argument(..., help="org/repo format"),
    start: int = typer.Option(None, "--start", help="Start PR number"),
    end: int = typer.Option(None, "--end", help="End PR number"),
    model: str = typer.Option("gpt-4o-mini", "--model", help="LLM model name to use"),
    custom_prompt: str = typer.Option("", "--custom-prompt", help="Custom prompt"),
    language: str = typer.Option("en", "--lang", help="Summary language"),
):
    """Execute PR data collection and summarization in one go (individual summaries + final summary)"""
    logger.info("Starting batch execution command")

    try:
        # Collect PRs
        collect(
            ctx=ctx,
            repo=repo,
            start=start,
            end=end,
        )

        # Generate summaries
        usage = summarize(
            ctx=ctx,
            repo=repo,
            model=model,
            custom_prompt=custom_prompt,
            language=language,
            only_total=False,
        )
        logger.info(f"Usage: {usage}")

    except Exception as e:
        logger.error(f"Error occurred during batch execution: {e}")
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
