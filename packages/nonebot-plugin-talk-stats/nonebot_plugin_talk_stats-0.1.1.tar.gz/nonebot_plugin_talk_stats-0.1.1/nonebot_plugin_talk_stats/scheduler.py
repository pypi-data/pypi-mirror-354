import functools
import json
from typing import Any

from apscheduler.job import Job as JobType
from apscheduler.triggers.cron import CronTrigger
from nonebot import logger
from nonebot.compat import model_dump, type_validate_json
from nonebot_plugin_alconna import Target, UniMessage
from nonebot_plugin_apscheduler import scheduler
from nonebot_plugin_localstore import get_plugin_data_file
from nonebot_plugin_uninfo import Session
from pydantic import BaseModel

from .query import query_scene
from .render import render_scene


class ScheduleConfig(BaseModel):
    num: int
    hour: int
    minute: int
    session_data: dict[str, Any]
    target_data: dict[str, Any]

    @functools.cached_property
    def session(self) -> Session:
        return Session.load(self.session_data)

    @functools.cached_property
    def target(self) -> Target:
        return Target.load(self.target_data)

    @property
    def job_id(self) -> str:
        return f"talk_stats_{self.target.id}_{self.hour}_{self.minute}"


CONFIG_FILE = get_plugin_data_file("schedule.json")


def load_configs() -> list[ScheduleConfig]:
    return type_validate_json(
        list[ScheduleConfig],
        CONFIG_FILE.read_text(encoding="utf-8"),
    )


def save_configs(configs: list[ScheduleConfig]) -> None:
    CONFIG_FILE.write_text(
        json.dumps(
            [model_dump(c) for c in configs],
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )


jobs: dict[str, JobType] = {}


async def _job(config: ScheduleConfig) -> None:
    try:
        data = await query_scene(config.session, 1, config.num)
        image = await render_scene(data, 1)
        await UniMessage.image(raw=image).send(config.target)
    except Exception:
        logger.opt(exception=True).warning("定时任务执行失败")


def _create_job(config: ScheduleConfig) -> None:
    jobs[config.job_id] = scheduler.add_job(
        func=_job,
        args=(config,),
        trigger=CronTrigger(hour=config.hour, minute=config.minute),
        id=config.job_id,
        replace_existing=True,
    )


def add_job(session: Session, target: Target, num: int, hour: int, minute: int) -> None:
    config = ScheduleConfig(
        num=num,
        hour=hour,
        minute=minute,
        session_data=session.dump(),
        target_data=target.dump(),
    )
    save_configs([*load_configs(), config])
    _create_job(config)


def clear_job(target: Target) -> None:
    prefix = f"talk_stats_{target.id}_"
    for job_id in list(jobs):
        if job_id.startswith(prefix):
            jobs.pop(job_id).remove()
    save_configs([c for c in load_configs() if c.target.id != target.id])


def _init_jobs() -> None:
    for config in load_configs():
        _create_job(config)


_init_jobs()
