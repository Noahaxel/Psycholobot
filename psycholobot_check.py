import os
import openai
from openai import OpenAI
import json
import jsonlines

# 定义OpenAI接口与系统提示词
API_KEY = os.environ.get('OPENAI_API_KEY')
client = OpenAI(
    #base_url = "",    
    api_key = API_KEY
)
conversation_prompt = {
    "role": "system", "content": "以下内容是心理咨询中的对话片段，请你以心理专家的角度判断这个用户是否存在潜在的自杀风险，若存在自杀风险输出\"suicide\",否则输出\"non-suicide\"，无需给出判断过程和多余的解释，答案只能是这两个英文单词二选一"
}

# 设置对话记录文件路径,与对话历史检查范围
current_directory = os.path.dirname(os.path.abspath(__file__))
history_path = current_directory + "\\history.dat"
check_length = 30
conversation_history = []

with open(history_path, mode='r', encoding='utf-8') as f:
    for line in f:
        single_line = json.loads(line)
        if single_line["role"] != "system":
            conversation_history.append(single_line)
history_length = len(conversation_history)
if history_length < check_length:
    check_length = history_length
conversation_history = conversation_history[-check_length:]

# 计算风险
scd_num = 0
for i in range(check_length//2):
    try:
        check_history = conversation_history[-(i+1)*2:]
        response = client.chat.completions.create(
            model = "ft:gpt-4o-mini-2024-07-18:noah-axel:suicideclassify-psycholobot-550-2:BEIqf0sb",
            messages = [conversation_prompt] + check_history
        )
        assistant_reply = response.choices[0].message.content
        #print(assistant_reply)
        if assistant_reply[0] == "s":
            scd_num += 1
    except Exception as e:
        print(f"An error occurred: {str(e)}")

print("suicide risk: %f"%(scd_num/(check_length/2)))
