"""UI 包入口。

目的：
1. 将 `sample_tool_ui.base` 中常用 DSL 类显式导出，降低导入心智负担。
2. 让插件作者在 `schema.py` 中可直接 `from sample_tool_ui import UiPage, UiButton`。
"""

from sample_tool_ui.base import UiButton
from sample_tool_ui.base import UiComponent
from sample_tool_ui.base import UiPage
from sample_tool_ui.base import UiSelect
from sample_tool_ui.base import UiSwitch
from sample_tool_ui.base import UiTextInput

__all__ = [
    "UiButton",
    "UiComponent",
    "UiPage",
    "UiSelect",
    "UiSwitch",
    "UiTextInput",
]
