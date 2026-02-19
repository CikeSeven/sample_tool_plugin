"""聊天结束 Hook 示例。

目的：
1. 演示如何消费 `chat_after_send` 的 payload 字段。
2. 演示如何通过返回 `message` 补丁改写助手消息。
"""


def main(payload):
    """处理 `chat_after_send` 事件并按条件改写消息。

    参数:
        payload: Hook 上下文字典，业务字段位于 `payload["payload"]`。

    返回:
        dict | None:
            - dict: 返回 `message` 补丁，让宿主覆写助手消息。
            - None: 不执行任何变更。
    """
    info = payload.get("payload", {}) or {}
    # 没有正文输出时不改写，避免空消息被无意义修改。
    if not bool(info.get("responseStarted")):
        return None
    # 用户手动中断时不改写，保持中断语义清晰。
    if bool(info.get("interrupted")):
        return None
    message = info.get("message")
    if not isinstance(message, dict):
        return None

    content = str(message.get("content", ""))
    return {"message": {"role": "assistant", "content": f"{content}喵"}}
