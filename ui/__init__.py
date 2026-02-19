"""UI 包入口。

目的：
1. 将 `ui.base` 中常用 DSL 类显式导出，降低导入心智负担。
2. 让插件作者在 `schema.py` 中可直接 `from ui import UiPage, UiButton`。
"""

from ui.base import UiButton
from ui.base import UiComponent
from ui.base import UiPage
from ui.base import UiSelect
from ui.base import UiSwitch
from ui.base import UiTextInput

__all__ = [
    "UiButton",
    "UiComponent",
    "UiPage",
    "UiSelect",
    "UiSwitch",
    "UiTextInput",
]
