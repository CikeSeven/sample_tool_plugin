"""示例插件内置 UI DSL 父类。

用途：
1. 给插件作者提供稳定的“页面协议”封装，避免手写 dict 出错。
2. 给编辑器提供类定义，获得补全、跳转与静态检查能力。

页面协议（UiPage.to_page 返回）：
- title: str                      页面标题
- subtitle: str                   页面副标题
- components: List[dict]          组件列表（由 UiComponent 子类序列化）
- state: dict                     插件业务状态（会在交互时回传）
- message: str                    可选提示文案（Flutter 会弹提示）

交互协议（Flutter -> on_event）：
- type: str                       事件类型，如 button_click / input_submit
- componentId: str                触发事件的组件 ID
- value: Any                      组件当前值
- state: dict                     当前页面状态
- payload: dict                   可选上下文负载
开发建议：
- 新增组件时优先继承 `UiComponent`，并在 `to_dict` 中补充必要字段。
- 尽量保持字段名稳定，避免宿主与插件协议不一致。
"""

from typing import Any, Dict, Iterable, List, Optional


class UiComponent:
    """通用组件基类。

    所有组件都必须包含：
    - id: 组件唯一标识（用于事件回调定位）
    - type: 组件类型（button/text_input/switch/select）
    - label/description: 展示文本
    - enabled/visible: 控制交互和可见性
    """

    def __init__(
        self,
        component_id: str,
        component_type: str,
        label: str = "",
        description: str = "",
        enabled: bool = True,
        visible: bool = True,
    ) -> None:
        # 统一在基类完成基础字段清洗，减少子类重复逻辑。
        self.id = str(component_id).strip()
        self.type = str(component_type).strip()
        self.label = str(label).strip()
        self.description = str(description).strip()
        self.enabled = bool(enabled)
        self.visible = bool(visible)

    def to_dict(self) -> Dict[str, Any]:
        """序列化为 Flutter 侧可消费的协议结构。"""
        return {
            "id": self.id,
            "type": self.type,
            "label": self.label,
            "description": self.description,
            "enabled": self.enabled,
            "visible": self.visible,
        }


class UiButton(UiComponent):
    """按钮组件。

    style 是可选样式提示，不同客户端可按需映射：
    - primary（默认）
    - secondary
    - danger
    """

    def __init__(
        self,
        component_id: str,
        label: str,
        description: str = "",
        style: str = "primary",
        enabled: bool = True,
        visible: bool = True,
    ) -> None:
        super().__init__(
            component_id=component_id,
            component_type="button",
            label=label,
            description=description,
            enabled=enabled,
            visible=visible,
        )
        self.style = str(style).strip() if str(style).strip() else "primary"

    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data["style"] = self.style
        return data


class UiTextInput(UiComponent):
    """文本输入组件。

    说明：
    - value: 当前值（字符串）
    - placeholder: 占位提示
    - multiline: 是否多行输入
    """

    def __init__(
        self,
        component_id: str,
        label: str,
        description: str = "",
        value: Any = "",
        placeholder: str = "",
        multiline: bool = False,
        enabled: bool = True,
        visible: bool = True,
    ) -> None:
        super().__init__(
            component_id=component_id,
            component_type="text_input",
            label=label,
            description=description,
            enabled=enabled,
            visible=visible,
        )
        self.value = "" if value is None else str(value)
        self.placeholder = str(placeholder).strip()
        self.multiline = bool(multiline)

    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data["value"] = self.value
        data["placeholder"] = self.placeholder
        data["multiline"] = self.multiline
        return data


class UiSwitch(UiComponent):
    """开关组件（布尔值）。"""

    def __init__(
        self,
        component_id: str,
        label: str,
        description: str = "",
        value: bool = False,
        enabled: bool = True,
        visible: bool = True,
    ) -> None:
        super().__init__(
            component_id=component_id,
            component_type="switch",
            label=label,
            description=description,
            enabled=enabled,
            visible=visible,
        )
        self.value = bool(value)

    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data["value"] = self.value
        return data


class UiSelect(UiComponent):
    """下拉选择组件。

    options 支持两种写法：
    1. dict: {"label": "...", "value": "..."}
    2. 基础类型（str/int/...）：会自动转为 label=value=字符串形式

    注意：
    - 会过滤 label 为空的选项，避免渲染异常。
    """

    def __init__(
        self,
        component_id: str,
        label: str,
        options: Optional[Iterable[Any]],
        description: str = "",
        value: Any = "",
        enabled: bool = True,
        visible: bool = True,
    ) -> None:
        super().__init__(
            component_id=component_id,
            component_type="select",
            label=label,
            description=description,
            enabled=enabled,
            visible=visible,
        )
        self.options: List[Dict[str, str]] = []
        for item in options or []:
            if isinstance(item, dict):
                option_label = str(item.get("label", "")).strip()
                option_value = str(item.get("value", ""))
            else:
                option_label = str(item).strip()
                option_value = str(item)
            if not option_label:
                continue
            self.options.append({"label": option_label, "value": option_value})
        self.value = str(value)

    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data["options"] = self.options
        data["value"] = self.value
        return data


class UiPage:
    """插件页面基类。

    子类通常需要重写：
    - build(payload): 构建首次进入页面时的 UI
    - on_event(event): 处理交互事件并返回下一帧页面
    """

    def build(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """返回默认空页面，便于子类按需覆盖。"""
        return {
            "title": "插件页面",
            "subtitle": "",
            "components": [],
            "state": {},
        }

    def on_event(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """默认交互处理：忽略事件，按 build 重新返回页面。"""
        payload = event.get("payload", {}) if isinstance(event, dict) else {}
        return self.build({"payload": payload})

    def to_page(
        self,
        title: str = "",
        subtitle: str = "",
        components: Optional[Iterable[UiComponent]] = None,
        state: Optional[Dict[str, Any]] = None,
        message: str = "",
    ) -> Dict[str, Any]:
        """统一组装页面协议。

        参数:
            title: 页面标题。
            subtitle: 页面副标题。
            components: 组件对象列表。
            state: 页面状态字典，会在后续事件里透传回来。
            message: 可选提示文案（通常用于操作结果反馈）。
        """
        return {
            "title": str(title).strip(),
            "subtitle": str(subtitle).strip(),
            "components": [item.to_dict() for item in (components or [])],
            "state": state or {},
            "message": str(message).strip(),
        }
