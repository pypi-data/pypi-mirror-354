from openai import OpenAI



def run():
    from openai import OpenAI

    client = OpenAI(
        base_url="https://ark.cn-beijing.volces.com/api/v3",
        api_key="e5a2fafe-a448-483f-964c-1a08e470dfb1",
    )
    # 提示用户输入问题（支持多行）
    print("请输入您的问题（按Ctrl+D或Ctrl+Z结束输入）:")
    user_input = []
    try:
        while True:
            # 逐行读取输入
            line = input()
            user_input.append(line)
    except EOFError:
        # 合并所有输入行
        user_content = "\n".join(user_input)

    # 调用API
    resp = client.chat.completions.create(
        model="doubao-pro-256k-241115",
        messages=[{"content": user_content, "role": "user"}],
        stream=True,
    )

    # 流式输出响应
    for chunk in resp:
        if chunk.choices and chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="", flush=True)