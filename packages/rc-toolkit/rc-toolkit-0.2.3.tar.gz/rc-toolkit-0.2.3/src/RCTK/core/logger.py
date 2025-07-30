
import typing
from typing import Optional
from logging import config, Logger, getLogger

from .io import file
from .env import is_debug


def get_log(logger_name: typing.Optional[str] = None) -> Logger:
    """
    Get the logging object

    Args:
        logger_name (str): If no name is specified, return the root logger.

    Returns:
        Logger: logging object
    """

    if logger_name is None:
        logger_name = "Main"
    return getLogger(logger_name)

# region trans

def dump_format(format_name: str = "default", **kw: typing.Mapping[str, typing.Optional[str]]) -> typing.Dict[str, typing.Dict[str, str]]:
    """
    dump formatters

    Args:
        format_name (str): format name. Defaults to format.

    Keyword Args:
        format (str, optional): format.
        datefmt (str, optional): data format.

    Returns:
        dict[str, dict[str, str]]: logging dict config format
    """

    back_format = {}
    if format_name == "default":
        back_format["format"] = "<%(asctime)s>[%(levelname)s]%(name)s:%(message)s"
        back_format["datefmt"] = "%Y-%m-%d %H:%M:%S"
    else:
        back_format["format"] = kw["format"]
        back_format["datefmt"] = kw["datefmt"]
    return back_format


def dump_handler(
    handler_class: str, formatter: str = "default", level: Optional[str] = None, **kw
) -> "dict[str, str]":
    """
    dump handlers

    Args:
        handler_class (str): log handler class
        formatter (str): log formatter. Defaults to "default".
        level (str | None): log level. Defaults to None.

    Keyword Args:
        filename (str, optional): log file name. Defaults to None.
        maxBytes (int, optional): log file max size. Defaults to None.
        backupCount (int, optional): log file backup count. Defaults to None.
        encoding (str, optional): log file encoding. Defaults to "utf8".

    Returns:
        dict[str, str]: logging dict config handler
    """
    back_handler = {}

    # region trans handlers
    if handler_class == "Console":
        handler_class = "logging.StreamHandler"
        back_handler["stream"] = "ext://sys.stdout"
    if handler_class == "File":
        handler_class = "logging.handlers.RotatingFileHandler"
    # endregion

    # region dump handlers
    back_handler["class"] = handler_class
    if handler_class == "logging.NullHandler":
        return back_handler

    back_handler["formatter"] = formatter
    if level is not None:
        back_handler["level"] = level
    if back_handler["class"] == "logging.handlers.RotatingFileHandler":
        if kw["filename"] is not None:
            back_handler["filename"] = kw["filename"]
            # if file mkdir
            file.mkdir(back_handler["filename"])

        back_handler["maxBytes"] = kw["maxBytes"]
        back_handler["backupCount"] = kw["backupCount"]
        back_handler["encoding"] = kw["encoding"]
        back_handler["encoding"] = "utf8"
    # endregion

    return back_handler


def trans_config(handlers: list, formats: Optional[list] = None, exist_loggers: bool = True, **kw) -> typing.Dict[str, typing.Any]:
    """
    trans config

    Args:
        handlers (list): _description_
        formats (list, optional): _description_. Defaults to [ "default", ].
        exist_loggers (bool, optional): _description_. Defaults to True.

    Keyword Args:
        "{format_name}_format" (str, optional): _description_.
            Defaults to "<%(asctime)s>[%(levelname)s]%(name)s:%(message)s".
        "{format_name}_datefmt" (str, optional): _description_. Defaults to "%Y-%m-%d %H:%M:%S".
        "{handler_name}_class" (str, optional): _description_. Defaults to "Console".
        "{handler_name}_formatter" (str, optional): _description_. Defaults to "default".
        "{handler_name}_level" (str, optional): _description_. Defaults to None.
        "{handler_name}_filename" (str, optional): _description_. Defaults to None.
        "{handler_name}_maxBytes" (int, optional): _description_. Defaults to None.
        "{handler_name}_backupCount" (int, optional): _description_. Defaults to None.
        "{handler_name}_encoding" (str, optional): _description_. Defaults to "utf8".

    Returns:
        dict[str, Any]: _description_
    """

    # init config
    config = {}
    config["version"] = 1
    config["formatters"] = {}
    config["handlers"] = {}
    config["loggers"] = {}
    config["loggers"][""] = {}
    config["loggers"][""]["handlers"] = []
    config["loggers"][""]["level"] = kw.get("root_level", "INFO")

    # exist loggers
    if exist_loggers is True:
        config["disable_existing_loggers"] = "False"
    else:
        config["disable_existing_loggers"] = "True"

    # default formats
    if formats is None:
        formats = [
            "default",
        ]

    # formatters
    for format_name in formats:
        config["formatters"][format_name] = dump_format(
            format_name=format_name,
            format=kw.get(f"{format_name}_format","default"),
            datefmt=kw.get(f"{format_name}_datefmt") # type: ignore
        )

    # handlers
    for handler_name in handlers:
        config["handlers"][handler_name] = dump_handler(
            handler_class=kw.get(f"{handler_name}_class","Console"),
            formatter=kw.get(f"{handler_name}_formatter", "default"),
            level=kw.get(f"{handler_name}_level", "INFO"),
            filename=kw.get(f"{handler_name}_filename", "log.log"),
            maxBytes=kw.get(f"{handler_name}_maxBytes", 1048576),
            backupCount=kw.get(f"{handler_name}_backupCount", 3),
            encoding=kw.get(f"{handler_name}_encoding", "utf8"),
        )
        config["loggers"][""]["handlers"].append(handler_name)

    return config

# endregion

def set_log(config_dict,*, builtin:bool = False) -> None:
    """
    日志配置根文件

        Args:
        config_dict (dict): 配置字典
    """
    try:
        config.dictConfig(trans_config(**config_dict))
        if builtin == True:
            from .tk_api import tk_1
            tk_1.tk_100000("get_log", get_log)
    except Exception as e:  # pylint: disable=broad-exception-caught
        logger = get_log("RCTK.Log")
        logger.error("Failed to set logging config: {error}\nData: {data}".format(
            error=e,data=(str(config_dict) )))
        if is_debug():raise
