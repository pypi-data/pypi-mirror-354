import json
from pathlib import Path

import litellm
from litellm import get_max_tokens, token_counter

from src.logger import get_project_logger
from src.settings import settings

logger = get_project_logger("summarizer")


def make_llm_request(
    content: str,
    model: str,
    prompt: str,
) -> tuple[str, dict]:
    """Execute a summarization request to the LLM"""

    try:
        response = litellm.completion(
            model=model,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": content},
            ],
            temperature=0.9,
            num_retries=2,
        )

        # Get token usage
        usage = response.usage
        usage_info = {
            "prompt_tokens": usage.prompt_tokens,
            "completion_tokens": usage.completion_tokens,
            "total_tokens": usage.total_tokens,
            "total_cost": response._hidden_params["response_cost"],
        }

        return response.choices[0].message.content.strip(), usage_info

    except Exception as e:
        logger.error(f"LLM request failed: {e}")
        raise


def _load_pr_data(filepath: Path) -> dict:
    """Load PR data from a JSON file"""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Failed to load {filepath}: {e}")
        raise


def _save_summary(summary: str, output_path: Path) -> None:
    """Save summary to a file"""
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(summary)
        logger.info(f"Summary saved to {output_path.name}")
    except Exception as e:
        logger.error(f"Failed to save summary to {output_path}: {e}")
        raise


def create_summary(
    repo_name: str,
    pr_files: list[Path],
    batch_num: int,
    model: str,
    custom_prompt: str,
    language: str,
) -> tuple[bool, dict]:
    """Generate a summary by batch processing multiple PR files"""
    try:
        # Load and merge multiple PR data
        pr_data_list = []
        pr_numbers = []

        for pr_file in pr_files:
            pr_data = _load_pr_data(pr_file)
            pr_numbers.append(pr_data.get("number", "unknown"))
            pr_data_list.append(pr_data)

        logger.info(f"Summarizing batch {batch_num} with PRs: {pr_numbers}")

        # Split processing considering token limits
        def process_pr_batch(
            pr_list: list[dict], sub_batch_id: str
        ) -> tuple[str, dict]:
            """Process a PR list and generate a summary"""
            batch_content = json.dumps(
                {"batch_id": sub_batch_id, "pr_count": len(pr_list), "prs": pr_list},
                ensure_ascii=False,
                indent=2,
            )

            summary, usage = make_llm_request(
                content=batch_content,
                model=model,
                prompt=custom_prompt
                if custom_prompt
                else settings.summary_system_prompt.format(language=language),
            )
            return summary, usage

        def split_and_process(
            pr_list: list[dict], batch_id: str
        ) -> tuple[list[str], dict]:
            """Split and process if token limit is exceeded"""
            max_tokens = get_max_tokens(model)

            # Check token count for the current batch
            batch_content = json.dumps(
                {"batch_id": batch_id, "pr_count": len(pr_list), "prs": pr_list},
                ensure_ascii=False,
                indent=2,
            )

            # Count tokens in message format
            messages = [
                {
                    "role": "system",
                    "content": custom_prompt
                    if custom_prompt
                    else settings.summary_system_prompt.format(language=language),
                },
                {"role": "user", "content": batch_content},
            ]
            count = token_counter(model=model, messages=messages)
            logger.info(
                f"Batch {batch_id} token count: {count} max_tokens: {max_tokens} model: {model}"
            )

            # If within token limit, process as is
            if count <= max_tokens:
                summary, usage = process_pr_batch(pr_list, batch_id)
                return [summary], usage

            # If a single PR exceeds the token limit
            if len(pr_list) == 1:
                logger.warning(
                    f"Single PR (#{pr_list[0].get('number', 'unknown')}) exceeds token limit: {count} tokens"
                )
                # Try processing with only simplified information
                simplified_pr = {
                    "number": pr_list[0].get("number"),
                    "title": pr_list[0].get("title"),
                    "body": pr_list[0].get("body", "")[:1000] + "..."
                    if len(pr_list[0].get("body", "")) > 1000
                    else pr_list[0].get("body", ""),
                    "files_count": len(pr_list[0].get("files", [])),
                    "simplified": True,
                }
                summary, usage = process_pr_batch([simplified_pr], batch_id)
                return [summary], usage

            # If multiple PRs, split
            mid = len(pr_list) // 2
            left_batch = pr_list[:mid]
            right_batch = pr_list[mid:]

            logger.info(
                f"Batch {batch_id} is split due to token limit: {len(pr_list)} -> {len(left_batch)} + {len(right_batch)}"
            )

            # Recursively process each split batch
            left_summaries, left_usage = split_and_process(left_batch, f"{batch_id}_L")
            right_summaries, right_usage = split_and_process(
                right_batch, f"{batch_id}_R"
            )

            # Merge usage
            total_usage = {
                "prompt_tokens": left_usage["prompt_tokens"]
                + right_usage["prompt_tokens"],
                "completion_tokens": left_usage["completion_tokens"]
                + right_usage["completion_tokens"],
                "total_tokens": left_usage["total_tokens"]
                + right_usage["total_tokens"],
                "total_cost": left_usage["total_cost"] + right_usage["total_cost"],
            }

            return left_summaries + right_summaries, total_usage

        # Execute split processing
        summaries, total_usage = split_and_process(pr_data_list, str(batch_num))

        # If there are multiple summaries, combine them
        if len(summaries) > 1:
            combined_summary = f"# Batch {batch_num} Combined Summary\n\n"
            for i, summary in enumerate(summaries, 1):
                combined_summary += f"## Sub-batch {i}\n{summary}\n\n"
            final_summary = combined_summary
        else:
            final_summary = summaries[0]

        # Save batch summary
        output_filename = (
            f"batch_summary_{batch_num:03d}_PRs_{'-'.join(map(str, pr_numbers))}.md"
        )
        output_dir = settings.base_dir / repo_name / "summaries"
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / output_filename

        _save_summary(final_summary, output_path)
        logger.info(f"Batch summary saved to {output_path.name}")
        logger.info(f"Usage: {total_usage}")

        return True, total_usage

    except Exception as e:
        logger.error(f"Failed to process batch {batch_num}: {e}")
        return False, {
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0,
            "total_cost": 0,
        }


def summarize_prs(
    repo_name: str, model: str, custom_prompt: str, language: str, batch_size: int = 10
):
    """Batch process all PR files in the input directory in groups of 10"""
    pr_files = sorted(Path(settings.base_dir / repo_name / "raws").glob("*.json"))
    if not pr_files:
        logger.info(
            f"No PR files found: {settings.base_dir / repo_name / 'raws'}"
        )
        return {
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0,
            "total_cost": 0,
        }

    processed_batches = 0
    failed_batches = 0
    total_usage = {
        "prompt_tokens": 0,
        "completion_tokens": 0,
        "total_tokens": 0,
        "total_cost": 0,
    }

    # Create summary directory
    (settings.base_dir / repo_name / "summaries").mkdir(parents=True, exist_ok=True)

    # Split PR files by batch size
    for i in range(0, len(pr_files), batch_size):
        batch_files = pr_files[i : i + batch_size]
        batch_num = (i // batch_size) + 1

        logger.info(
            f"Processing batch {batch_num}/{(len(pr_files) + batch_size - 1) // batch_size} ({len(batch_files)} PRs)"
        )

        success, usage = create_summary(
            repo_name=repo_name,
            pr_files=batch_files,
            batch_num=batch_num,
            model=model,
            custom_prompt=custom_prompt,
            language=language,
        )

        if success:
            processed_batches += 1
            # Accumulate token usage
            for key in total_usage:
                total_usage[key] += usage[key]
        else:
            failed_batches += 1

    logger.info(f"Processing complete: {processed_batches} batches succeeded, {failed_batches} batches failed")
    logger.info(f"Total usage: {total_usage}")

    return total_usage


def create_final_summary(
    repo_name: str, model: str, custom_prompt: str, language: str
) -> dict:
    """Read all .md files in the summary directory and generate the final summary"""
    # Search for .md files
    summary_files = sorted(
        Path(settings.base_dir / repo_name / "summaries").glob("*.md")
    )
    if not summary_files:
        logger.info(
            f"No summary files found: {settings.base_dir / 'summaries'}"
        )
        return {
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0,
            "total_cost": 0,
        }

    # Combine all summaries
    combined_summaries = ""
    for file in summary_files:
        content = file.read_text(encoding="utf-8")
        combined_summaries += f"\n\n## {file.stem}\n{content}"

    # Generate the final summary
    try:
        summary, summary_usage = make_llm_request(
            content=combined_summaries,
            model=model,
            prompt=custom_prompt
            if custom_prompt
            else settings.summary_system_prompt.format(language=language),
        )

        # Save the final summary
        output_path = settings.base_dir / repo_name / "RULES_FOR_AI.md"
        output_path.write_text(summary, encoding="utf-8")

        issue_templates, issue_templates_usage = make_llm_request(
            content=combined_summaries,
            model=model,
            prompt=custom_prompt
            if custom_prompt
            else settings.issue_template_system_prompt.format(language=language),
        )

        for key in summary_usage:
            summary_usage[key] += issue_templates_usage[key]

        # Save the issue templates
        output_path = settings.base_dir / repo_name / "ISSUE_TEMPLATES.md"
        output_path.write_text(issue_templates, encoding="utf-8")
        logger.info(f"Final summary saved to {output_path.name} and issue templates saved to {output_path.name}")
        logger.info(f"Usage: {summary_usage}")
        return summary_usage
    except Exception as e:
        raise
