"""工具示例：回显用户输入。

该脚本用于演示最常见的工具模式：
1. 接收模型传入的 JSON 参数。
2. 执行业务逻辑（这里是简单回显）。
3. 返回结构化结果给宿主，再由宿主回填给模型。
"""


def main(payload):
    """工具入口函数。

    参数:
        payload: 工具参数字典，示例期望字段 `text`。

    返回:
        dict: 可序列化结果对象。
    """
    # 统一转为字符串，避免 None/数字等类型导致序列化含义不一致。
    text = str(payload.get("text", ""))
    return {
        "ok": True,
        "tool": "sample_echo",
        "echo": text,
        "length": len(text),
    }
