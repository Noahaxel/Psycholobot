# Psycholobot
2025本科毕设-基于大语言模型的心理咨询聊天机器人研究

基于Psy-DT数据集和phr_suicide_prediction_dataset_clean_light数据集，对gpt-4o-mini-2024-07-18预训练模型进行微调，需要本人API-KEY访问；

psycholobot_chat.py 使用 ft:gpt-4o-mini-2024-07-18:noah-axel:psycholobot-100-3:B6EW5zAf 基于Psy-DT数据集的微调模型；
依据理情行为疗法提供心理咨询服务，并生成对话记录与摘要

psycholobot_check.py 使用 ft:gpt-4o-mini-2024-07-18:noah-axel:suicideclassify-psycholobot-550-2:BEIqf0sb 基于pspdcl数据集的微调模型；
用于对psycholobot_chat.py 生成的对话记录文件进行检查，根据最近（默认为30行）的聊天记录文本，判断用户话语中包含的潜在自杀风险

history.dat 为聊天记录文件。
