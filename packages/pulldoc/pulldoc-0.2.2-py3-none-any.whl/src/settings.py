"""Project settings management module

Centrally manages environment variables and fixed values using pydantic-settings,
providing type safety and configuration validation features.
"""

from pathlib import Path

from pydantic import Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class ProjectSettings(BaseSettings):
    """Project settings class with validation and type safety"""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
        validate_assignment=True
    )

    github_token: str | None = Field(
        default=None,
        env="GITHUB_TOKEN",
        description="GitHub API token (optional)"
    )

    summary_system_prompt: str = Field(
        default="""You are a Senior Engineer and your task is to
- Extract from the provided text a pattern of modifications that “would happen” and “would be modified in this way”.

Compliance
- Summarize in {language}
- If you determine that the modification will not function as future knowledge, do not output it (e.g., first time setup)
- Please include a templated fix along with specific file paths
- Please also summarize any points that the team should note from your comments on the review

Translated with www.DeepL.com/Translator (free version)
""",
        description="System prompt for final summary"
    )

    issue_template_system_prompt: str = Field(
        default="""You are a senior engineer. Your task is as follows:
- Create an issue template based on the provided text, extracting patterns such as "if this happens" and "modify like this".

Compliance:
- Write the template in {language}.
- Do not include modifications that are not useful as future knowledge (e.g., initial setup).
- Refer to the diff of modifications in modified_files[number].patch in the provided JSON.
- Always include specific file paths and templated sample modifications in your output.

Format:

``` feature_request.md
---
name: ✨ Feature Request / Improvement
about: Suggest a new feature or request an improvement to an existing one.
title: "[Feature/Improvement] "
labels: "enhancement"
assignees: ""

---

## Feature Summary
A concise description of the feature or improvement you want to implement.

## Goal
The problem this feature/improvement solves or the objective it aims to achieve.

## Details
- Specific changes or required steps.
- Which parts are affected, such as new API endpoints, CLI commands, backend processes, etc.
- Required data model or schema changes.
- How to integrate with external services.
- Expected inputs, outputs, and error scenarios.
- (Optional) Links to supplementary materials such as screen images or UML diagrams.

## Technical Considerations
- Libraries or frameworks to be used.
- Requirements for asynchronous processing, error handling, retries, or specific design patterns.
- Concerns about performance, scalability, or security.
- Compatibility with the existing codebase.

## Test Requirements
- What layers and types of tests (unit, integration, edge cases, etc.) are needed.
- Any specific test data or environment setup required.

## Related Issues/PRs
- Links to related existing issues or pull requests.

## TODO List (Optional)
- Breakdown of tasks required for implementation (as concrete instructions for implementers).
```

``` bug_report.md
---
name: 🐛 Bug Report
about: Report a reproducible bug or unexpected behavior.
title: "[Bug] "
labels: "bug"
assignees: ""

---

## Problem Summary
A concise description of the problem that occurred.

## Steps to Reproduce
Specific steps required to reproduce the problem.
1. ...
2. ...
3. ...

## Expected Behavior
What should ideally happen when the problem occurs.

## Actual Behavior
What actually happens when the problem occurs.

## Environment

## Error Message / Logs
Error messages or related log outputs that occurred.
(Provide as code blocks or file links as needed.)

## Related Code / Configuration
Links or excerpts of code files or configuration files related to the problem.

## Technical Considerations (Optional)
Considerations about the cause of the problem or possible solutions.

## Related Issues/PRs
- Links to related existing issues or pull requests.
```

``` refactoring.md

---
name: 🧹 Refactoring / Technical Debt
about: Address code structure, performance, or maintainability issues.
title: "[Refactoring/Tech Debt] "
labels: "refactoring, tech-debt"
assignees: ""

---

## Problem
Problems present in the current code (e.g., low readability, duplication, inefficiency, deviation from certain patterns, etc.).

## Goal
What will be improved by this refactoring/technical debt resolution (e.g., maintainability, performance, development efficiency, etc.).

## Proposed Solution
Specific modification methods or new design policies.

## Scope
- Files, modules, or components affected.
- Whether there are any functional changes.

## Technical Considerations
- Impact on existing features or tests.
- Impact on integration with external services.
- Whether phased refactoring is necessary.

## Test Requirements
- Whether existing tests need to be modified or new tests added.
- Test perspectives to pay special attention to (e.g., preventing regression of existing features).

## Related Issues/PRs
- Links to issues related to this refactoring or other issues resolved by this refactoring.

```

""",
        description="System prompt for generating issue templates"
    )

    @computed_field
    @property
    def base_dir(self) -> Path:
        """Project base directory"""
        return Path.cwd() / ".pulldoc_result"


# Global settings instance
_settings = None

def get_settings():
    """Get settings instance (allows for testing with dependency injection)"""
    global _settings
    if _settings is None:
        _settings = ProjectSettings()
    return _settings

# For backward compatibility
settings = get_settings()

