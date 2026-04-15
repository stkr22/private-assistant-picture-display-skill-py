"""CLI entrypoint for the Picture Display Skill."""

import asyncio
import pathlib
from typing import Annotated

import jinja2
import typer
from private_assistant_commons import (
    MqttConfig,
    create_skill_engine,
    mqtt_connection_handler,
    skill_config,
    skill_logger,
)

from private_assistant_picture_display_skill.config import PictureSkillConfig
from private_assistant_picture_display_skill.picture_skill import PictureSkill

app = typer.Typer(help="Picture Display Skill for Inky e-ink devices")


@app.command()
def main(config_path: Annotated[pathlib.Path, typer.Argument(envvar="PRIVATE_ASSISTANT_CONFIG_PATH")]) -> None:
    """Run the Picture Display Skill.

    Args:
        config_path: Path to YAML configuration file or directory

    """
    asyncio.run(start_skill(config_path))


async def start_skill(config_path: pathlib.Path) -> None:
    """Start the Picture Display Skill with all required services.

    Args:
        config_path: Path to YAML configuration file or directory

    """
    logger = skill_logger.SkillLogger.get_logger("Private Assistant PictureSkill")

    config_obj = skill_config.load_config(config_path, PictureSkillConfig)

    # Database engine for GlobalDevice registry (managed by BaseSkill/commons)
    db_engine_async = create_skill_engine()

    template_env = jinja2.Environment(
        loader=jinja2.PackageLoader("private_assistant_picture_display_skill", "templates"),
        autoescape=True,
    )

    mqtt_config = MqttConfig()  # ty: ignore[missing-argument]
    await mqtt_connection_handler.mqtt_connection_handler(
        PictureSkill,
        config_obj,
        mqtt_config=mqtt_config,
        retry_interval=5,
        logger=logger,
        template_env=template_env,
        engine=db_engine_async,
    )


if __name__ == "__main__":
    app()
