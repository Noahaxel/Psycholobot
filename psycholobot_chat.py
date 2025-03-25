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
    "role": "system", "content": "你是一位精通理情行为疗法（Rational Emotive Behavior Therapy，简称REBT）的心理咨询师，能够合理地采用理情行为疗法给来访者提供专业地指导和支持，缓解来访者的负面情绪和行为反应，帮助他们实现个人成长和心理健康。理情行为治疗主要包括以下几个阶段，下面是对话阶段列表，并简要描述了各个阶段的重点。\n（1）**检查非理性信念和自我挫败式思维**：理情行为疗法把认知干预视为治疗的“生命”，因此，几乎从治疗一开始，在问题探索阶段，咨询师就以积极的、说服教导式的态度帮助来访者探查隐藏在情绪困扰后面的原因，包括来访者理解事件的思维逻辑，产生情绪的前因后果，借此来明确问题的所在。咨询师坚定地激励来访者去反省自己在遭遇刺激事件后，在感到焦虑、抑郁或愤怒前对自己“说”了些什么。\n（2）**与非理性信念辩论**：咨询师运用多种技术（主要是认知技术）帮助来访者向非理性信念和思维质疑发难，证明它们的不现实、不合理之处，认识它们的危害进而产生放弃这些不合理信念的愿望和行为。\n（3）**得出合理信念，学会理性思维**：在识别并驳倒非理性信念的基础上，咨询师进一步诱导、帮助来访者找出对于刺激情境和事件的适宜的、理性的反应，找出理性的信念和实事求是的、指向问题解决的思维陈述，以此来替代非理性信念和自我挫败式思维。为了巩固理性信念，咨询师要向来访者反复教导，证明为什么理性信念是合情合理的，它与非理性信念有什么不同，为什么非理性信念导致情绪失调，而理性信念导致较积极、健康的结果。\n（4）**迁移应用治疗收获**：积极鼓励来访者把在治疗中所学到的客观现实的态度，科学合理的思维方式内化成个人的生活态度，并在以后的生活中坚持不懈地按理情行为疗法的教导来解决新的问题。（另外，你要记住保持说中文的对话风格。）"
}

# 设置对话记录文件路径，与生成摘要的最少对话次数
current_directory = os.path.dirname(os.path.abspath(__file__))
history_path = current_directory + "\\history.dat"
times_abstract_create = 5
conversation_history = []

# 使用API与模型进行对话并保存
def chat_with_gpt(prompt):
    if not prompt or not isinstance(prompt, str):
        return "用户输入不能为空或非字符串。"
    conversation_history.append({"role": "user", "content": prompt})
    try:
        response = client.chat.completions.create(
            model = "ft:gpt-4o-mini-2024-07-18:noah-axel:psycholobot-100-3:B6EW5zAf",
            messages = [conversation_prompt] + conversation_history + [conversation_prompt]
        )
        assistant_reply = response.choices[0].message.content
        conversation_history.append({"role": "assistant", "content": assistant_reply})
        return assistant_reply
    except Exception as e:
        return f"An error occurred: {str(e)}"

# 使用API请求模型生成摘要并保存
def abstract_with_gpt():
    try:
        response = client.chat.completions.create(
            model = "ft:gpt-4o-mini-2024-07-18:noah-axel:psycholobot-100-3:B6EW5zAf",
            messages = conversation_history + [{"role": "user", "content": "请将之前的聊天过程尽可能详细和完整地生成摘要"}]
        )
        assistant_reply = response.choices[0].message.content
        conversation_history.append({"role": "system", "content": "和用户之前的聊天过程摘要如下，请根据摘要继续对话：" + assistant_reply})
        return assistant_reply
    except Exception as e:
        err = f"An error occurred: {str(e)}"
        print(err)
        return err


# 创建或读取对话记录文件
if os.path.exists(history_path):
    print("检测到历史聊天记录，将继续对话 (((  输入 delete 删除记录并开始新的对话, 输入 quit 结束对话  )))")
    delete = input()
    if delete != "delete":
        with open(history_path, mode='r', encoding='utf-8') as f:
            conversation_history = [json.loads(line) for line in f]
    else:
        with open(history_path, mode='w', encoding='utf-8') as f:
            print("删除成功！")

# 持续进行对话过程
times = 0
while 1:
    if (times == 0) & (delete != "delete"):
        prompt = delete
    else:
        prompt = input()
    # 输入quit退出对话，若对话过程超过设置的次数，请求生成并记录摘要以便于下次对话
    if prompt == 'quit':
        if times >= times_abstract_create:
            print("对话摘要记录中，请勿手动关闭...")
            abstract_with_gpt()
        break
    else:
        print(chat_with_gpt(prompt) + "    (((  输入 quit 结束对话  )))    ")
    times = times + 1

# 保存对话与摘要记录
with jsonlines.open(history_path, mode='w') as f:
    for line in conversation_history:
        f.write(line)