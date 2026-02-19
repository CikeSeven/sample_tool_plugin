"""应用启动 Hook 示例。

该脚本用于演示 Hook 的最小实现：
1. 导出 `main(payload)` 作为入口。
2. 读取统一事件上下文（event/payload/timestamp）。
3. 返回可序列化对象，便于在 Hook 日志中观察执行结果。
"""


def main(payload):
    """处理 `app_start` 事件。

    参数:
        payload: Hook 上下文字典，结构由宿主注入。

    返回:
        dict: 简要执行结果，不会影响主流程。
    """
    # 仅返回调试信息，避免在 app_start 执行重逻辑影响启动速度。
    return {
        "ok": True,
        "hook": "app_start",
        "event": payload.get("event"),
    }
