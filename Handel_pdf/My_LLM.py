import openai

def ask_LLMmodel(input, prompt ,model_name = 'gpt4o'):
    if model_name == 'gpt4o':
        return askGPT(input, prompt)


""" 
在下面添加调用模型的函数，并在上方函数添加elif分支
"""
def askGPT(input, prompt):
    q = str(input)
    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": q}
    ]

    # 设置 Azure OpenAI 的 API key 和 Endpoint URL
    api_key = 'd2ca2cab8f0f46da891dec75ae8b38ec'  # 替换为你在 Azure 上创建的 API Key
    endpoint = 'https://coe0522.openai.azure.com/'  # 替换为你的 Endpoint URL

    # 配置 OpenAI 客户端
    openai.api_key = api_key
    openai.api_base = endpoint
    openai.api_type = "azure"
    openai.api_version = "2023-05-15"  # 需要使用 GPT-4 的正确版本

    # 调用 GPT-4o 模型
    response = openai.ChatCompletion.create(
        engine="gpt-4o",  # 使用 GPT-4o 模型
        messages=messages,
        temperature=0
    )
    return response['choices'][0]['message']['content']