from importlib.metadata import version

from nonebot import logger, require
from nonebot.plugin import PluginMetadata, inherit_supported_adapters

from .config import Config, config

require("nonebot_plugin_alconna")
require("nonebot_plugin_chatrecorder")
require("nonebot_plugin_htmlrender")
require("nonebot_plugin_orm")
require("nonebot_plugin_uninfo")
if config.enable_scheduler:
    try:
        require("nonebot_plugin_apscheduler")
    except ImportError:
        config.enable_scheduler = False
        logger.warning("nonebot_plugin_apscheduler 插件未安装, 已禁用定时任务功能")
    else:
        from . import scheduler as scheduler

from . import matcher as matcher

try:
    __version__ = version("nonebot-plugin-talk-stats")
except Exception:
    __version__ = None

__plugin_meta__ = PluginMetadata(
    name="Talk Stats",
    description="群聊活跃度统计",
    usage="talk_stats -h",
    type="application",
    homepage="https://github.com/wyf7685/nonebot-plugin-talk-stats",
    config=Config,
    supported_adapters=inherit_supported_adapters(
        "nonebot_plugin_alconna",
        "nonebot_plugin_chatrecorder",
        "nonebot_plugin_uninfo",
    ),
    extra={
        "author": "wyf7685",
        "version": __version__,
    },
)
