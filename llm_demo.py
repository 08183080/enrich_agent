from openai import OpenAI

client = OpenAI(
    api_key="sk-u9cz1IP6akgZlvFI0bILSOqGkDSp5hEo4O7RcTKZDXiXlADs",
    base_url="https://www.dmxapi.com/v1"
)

response = client.chat.completions.create(
    model="gpt-5-mini",
    messages=[{"role": "user", "content": "请帮我对ftp的消息序列进行丰富，它的消息序列是：USER ubuntu PASS ubuntu SYST ACCT REIN SMNT FEAT NOOP HELP STAT STRU QUIT 同时确保消息序列的逻辑流是正确的。我想要扩充后的消息序列高质量，可以被待测server处理。我只要消息序列。"}]
)

print(response.choices[0].message.content)