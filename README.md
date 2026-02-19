# Sample Tool Plugin

## 插件功能说明
该插件用于演示 NowChat 插件最小可用能力，包含以下功能：

1. 工具能力：`sample_echo`
- 接收参数 `text`，返回回显结果与文本长度。
- 用于验证模型工具调用链路是否正常。

2. Hook 能力：`app_start`
- 应用启动后触发。
- 返回简要调试信息，便于确认 Hook 已生效。

3. Hook 能力：`chat_after_send`
- 会话请求结束后触发。
- 当本次回复成功且未中断时，返回 `appendAssistantSuffix`，在助手消息末尾追加“喵”。

4. 插件配置页能力
- 提供输入框、开关、下拉和保存按钮。
- 点击保存后将当前配置写入 `ui/config.json`。

## 目录结构
```text
sample_tool_plugin/
  plugin.json
  tools/
    echo.py
  hooks/
    app_start.py
    chat_after_send.py
  ui/
    __init__.py
    base.py
    schema.py
```

## 结构说明
- `tools/`：模型可调用的工具脚本。
- `hooks/`：订阅宿主事件后自动触发的脚本。
- `ui/`：插件配置页面 DSL（基础类 + 页面实现）。

## plugin.json 字段说明
`plugin.json` 是标准 JSON，不支持注释。字段含义如下：

- `id`：插件唯一 ID，建议小写下划线。
- `name`：插件显示名称。
- `author`：插件作者。
- `description`：插件描述。
- `version`：插件版本号。
- `type`：插件类型（示例为 `python`）。
- `providesGlobalPythonPaths`：是否把本插件路径暴露为“全局共享 Python 路径”。
  - `false`：默认隔离，仅当前插件自身使用。
  - `true`：其他插件执行 Python 时也会自动追加本插件路径（适合基础库插件）。
- `permissions`：权限声明（示例用 `tool:*`、`hook:*`）。
- `packages`：插件包配置（解压目录、Python 路径等）。
- `tools`：工具定义（名称、runtime、参数 schema）。
- `hooks`：Hook 定义（事件名、脚本路径、优先级）。

## 文件说明
- `tools/echo.py`：工具入口 `main(payload)`，返回结构化 JSON。
- `hooks/app_start.py`：启动事件 Hook 示例。
- `hooks/chat_after_send.py`：聊天后置 Hook 示例。
- `ui/base.py`：UI DSL 基类与组件协议。
- `ui/schema.py`：插件配置页面实现。
- `ui/__init__.py`：UI DSL 导出入口。

## 使用方式
1. 将 `sample_tool_plugin` 目录压缩为 zip（zip 根目录需直接包含 `plugin.json`）。
2. 在应用中进入“插件中心”并导入该 zip。
3. 安装后进入插件详情页，验证工具、Hook、插件配置页面是否正常。
