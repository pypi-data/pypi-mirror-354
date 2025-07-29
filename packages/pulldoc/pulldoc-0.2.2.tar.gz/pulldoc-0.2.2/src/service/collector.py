import json

from github import Github

from src.logger import get_project_logger
from src.settings import settings

logger = get_project_logger("collector")


def fetch_prs(
    org_repo: str,
    start: int | None = None,
    end: int | None = None,
) -> None:
    try:
        gh = Github(settings.github_token)
        try:
            repo = gh.get_repo(org_repo)
        except Exception as e:
            logger.error(f"Error fetching repository {org_repo}")
            raise

        pulls = repo.get_pulls(state="all", sort="created")
        if not pulls.totalCount:
            logger.info(f"No PRs found for {org_repo}")
            return
        out_dir = settings.base_dir / org_repo / "raws"
        out_dir.mkdir(parents=True, exist_ok=True)

        processed_count = 0
        saved_files = []


        fixed_start = max(0, start - 1) if start else None
        for pr in pulls[fixed_start:end]:
            logger.info(f"Processing PR #{pr.number}")
            try:
                # Get list of modified files
                files = pr.get_files()
                modified_files = [
                    {
                        "filename": file.filename,
                        "status": file.status,
                        "changes": file.changes,
                        "patch": file.patch,
                    }
                    for file in files
                ]

                # Get review comments (code-level comments)
                review_comments = []
                try:
                    for comment in pr.get_review_comments():
                        review_comments.append({
                            "id": comment.id,
                            "body": comment.body,
                            "diff_hunk": comment.diff_hunk
                        })
                except Exception as e:
                    logger.warning(f"Error fetching review comments for PR #{pr.number}: {e}")

                # Get issue comments (general PR comments)
                issue_comments = []
                try:
                    for comment in pr.get_issue_comments():
                        issue_comments.append({
                            "id": comment.id,
                            "body": comment.body,
                            "user": comment.user.login if comment.user else None,
                            "created_at": comment.created_at.isoformat() if comment.created_at else None,
                            "updated_at": comment.updated_at.isoformat() if comment.updated_at else None,
                        })
                except Exception as e:
                    logger.warning(f"Error fetching issue comments for PR #{pr.number}: {e}")


                # Extract only necessary information
                pr_info = {
                    "title": pr.title,
                    "body": pr.body,
                    "modified_files": modified_files,
                    "review_comments": review_comments,
                    "issue_comments": issue_comments,
                    "number": pr.number,
                    "created_at": pr.created_at.isoformat() if pr.created_at else None,
                    "updated_at": pr.updated_at.isoformat() if pr.updated_at else None,
                }

                # Save each PR as a separate file
                path = out_dir / f"pr_{pr.number:04d}.json"
                path.write_text(json.dumps(pr_info, ensure_ascii=False, indent=2))
                saved_files.append(path)
                processed_count += 1

            except Exception as e:
                logger.error(f"Error occurred while processing PR #{pr.number}: {e}")
                continue

        logger.info(f"Finished fetching PRs: {processed_count} PRs have been fetched and saved.")

    except Exception as e:
        logger.error(f"An error occurred while fetching PRs: {e}")
        raise
