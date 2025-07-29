from pathlib import Path
from decouple import config


class AppConfig:
    """Configuration for app."""

    CONFIG_PREFIX: str = "AWESOME_COMMIT_"

    SRC_DIR: Path = Path(__file__).parent
    PROMPTS_DIR: Path = config(
        f"{CONFIG_PREFIX}PROMPTS_DIR", default=Path(__file__).parent / "prompts"
    )
    DEFAULT_PROMPT_TEMPLATE: Path = PROMPTS_DIR / "generate_commit_message.txt.jinja2"
    GEMINI_API_KEY: str = config(f"{CONFIG_PREFIX}GEMINI_API_KEY")
    PROMPT_TEMPLATE: str | None = config(
        f"{CONFIG_PREFIX}PROMPT_TEMPLATE", default=None
    )
    NUM_PREVIOUS_COMMITS: int = config(
        f"{CONFIG_PREFIX}NUM_PREVIOUS_COMMITS", default=3, cast=int
    )
    RUN_PRE_COMMIT = config(f"{CONFIG_PREFIX}RUN_PRE_COMMIT", default=True, cast=bool)
    AI_MODEL: str = config(
        f"{CONFIG_PREFIX}LLM_MODEL", default="gemini-2.5-flash-preview-04-17"
    )
    COMMIT_EDITOR: str = config(f"{CONFIG_PREFIX}COMMIT_EDITOR", default="vi")
