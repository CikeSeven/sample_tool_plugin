"""示例插件配置页面（UI DSL）。

说明：
1. 该文件定义插件自己的页面行为，不依赖 Flutter 端硬编码组件。
2. 宿主会调用 `create_page()`，并通过 `build/on_event` 驱动页面重渲染。
3. 本示例演示“读取本地配置 -> 修改 -> 保存”的完整闭环。
"""

import json
import os
from typing import Any, Dict

from sample_tool_ui import UiButton
from sample_tool_ui import UiPage
from sample_tool_ui import UiSelect
from sample_tool_ui import UiSwitch
from sample_tool_ui import UiTextInput


class SampleUiPage(UiPage):
    """示例配置页实现。

    页面包含四种组件：
    - 多行输入框：配置文本
    - 开关：功能开关
    - 下拉：语气风格
    - 按钮：持久化保存
    """

    def _default_state(self) -> Dict[str, Any]:
        """返回初始状态，作为配置文件缺失或异常时的兜底。"""
        return {
            "input_text": "",
            "feature_on": False,
            "tone": "neutral",
        }

    def _config_path(self) -> str:
        """返回配置文件路径（与 `schema.py` 同目录）。"""
        current_file = os.path.abspath(__file__)
        current_dir = os.path.dirname(current_file)
        return os.path.join(current_dir, "config.json")

    def _load_saved_state(self) -> Dict[str, Any]:
        """读取本地配置，失败时回退默认值。

        这里对外部文件输入做了类型与枚举校验，防止脏数据导致 UI 状态异常。
        """
        state = self._default_state()
        config_path = self._config_path()
        if not os.path.isfile(config_path):
            return state

        try:
            with open(config_path, "r", encoding="utf-8") as fp:
                loaded = json.load(fp)
            if not isinstance(loaded, dict):
                return state
            state["input_text"] = str(loaded.get("input_text", ""))
            state["feature_on"] = bool(loaded.get("feature_on", False))
            state["tone"] = str(loaded.get("tone", "neutral"))
            if state["tone"] not in ("neutral", "formal", "friendly"):
                state["tone"] = "neutral"
        except Exception:
            # 读取失败时不抛异常，保持页面可用。
            return state
        return state

    def _save_state(self, state: Dict[str, Any]) -> None:
        """将当前状态持久化到 `config.json`。"""
        config_path = self._config_path()
        with open(config_path, "w", encoding="utf-8") as fp:
            json.dump(state, fp, ensure_ascii=False, indent=2)

    def _build_components(self, state: Dict[str, Any]):
        """根据当前状态构建组件列表。"""
        return [
            UiTextInput(
                component_id="input_text",
                label="输入文本",
                placeholder="输入任意内容后点击发送",
                value=state.get("input_text", ""),
                multiline=True,
            ),
            UiSwitch(
                component_id="feature_on",
                label="启用高级模式",
                value=state.get("feature_on", False),
            ),
            UiSelect(
                component_id="tone",
                label="语气风格",
                value=state.get("tone", "neutral"),
                options=[
                    {"label": "中性", "value": "neutral"},
                    {"label": "专业", "value": "formal"},
                    {"label": "活泼", "value": "friendly"},
                ],
            ),
            UiButton(
                component_id="save_config",
                label="保存配置",
                description="将当前配置保存到本地 config.json",
            ),
        ]

    def build(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """首次进入页面时构建 UI。"""
        state = self._load_saved_state()
        return self.to_page(
            title="示例工具插件配置",
            subtitle="修改后点击“保存配置”持久化",
            components=self._build_components(state),
            state=state,
        )

    def on_event(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """处理组件事件并返回下一帧页面。

        事件结构由宿主注入：
        - type: 事件类型（button_click/input_submit/switch_toggle/select_change）
        - componentId: 触发事件的组件 ID
        - value: 组件当前值
        - state: 当前页面状态
        """
        event = event or {}
        state = dict(event.get("state") or {})
        event_type = str(event.get("type", "")).strip()
        component_id = str(event.get("componentId", "")).strip()
        value = event.get("value")

        message = ""
        if event_type == "input_submit" and component_id == "input_text":
            state["input_text"] = "" if value is None else str(value)
            message = "输入已更新"
        elif event_type == "switch_toggle" and component_id == "feature_on":
            state["feature_on"] = bool(value)
            message = "开关状态已更新"
        elif event_type == "select_change" and component_id == "tone":
            state["tone"] = "" if value is None else str(value)
            message = "下拉选项已更新"
        elif event_type == "button_click" and component_id == "save_config":
            try:
                self._save_state(state)
                message = "配置已保存"
            except Exception as error:
                # 保存失败只提示，不中断页面渲染。
                message = f"保存失败: {error}"

        return self.to_page(
            title="示例工具插件配置",
            subtitle="修改后点击“保存配置”持久化",
            components=self._build_components(state),
            state=state,
            message=message,
        )


def create_page() -> UiPage:
    """插件 UI 工厂函数（宿主入口）。"""
    return SampleUiPage()
