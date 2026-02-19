"""聊天结束 Hook 示例。

目的：
1. 演示如何消费 `chat_after_send` 的 payload 字段。
2. 演示如何通过返回值驱动宿主执行消息后处理动作。

当前约定：
- 返回 `{"appendAssistantSuffix": "<文本>"}` 时，宿主会把文本追加到助手消息末尾。
"""


def main(payload):
    """处理 `chat_after_send` 事件并按条件返回追加动作。

    参数:
        payload: Hook 上下文字典，业务字段位于 `payload["payload"]`。

    返回:
        dict | None:
            - dict: 触发后置动作（追加“喵”）。
            - None: 不执行任何变更。
    """
    info = payload.get("payload", {}) or {}
    # 没有正文输出时不追加，避免空消息被无意义修改。
    if not bool(info.get("responseStarted")):
        return None
    # 用户手动中断时不追加，保持中断语义清晰。
    if bool(info.get("interrupted")):
        return None
    # 返回宿主可识别的动作对象。
    return {"appendAssistantSuffix": "喵"}
