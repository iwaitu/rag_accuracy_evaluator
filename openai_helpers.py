# rag_accuracy_evaluator/openai_helpers.py
import requests
import time

def generate_questions_and_answers(doc_text: str, model: str, api_key: str, base_url: str, num_questions: int):
    prompt = f"""
你是一位信息抽取专家。
请根据以下文档内容提出 {num_questions} 个简洁的问题，并为每个问题生成准确、简洁（20字以内）的标准答案。
注意：答案必须来自文档中明确提到的信息，避免泛化。

文档：
\"\"\"
{doc_text}
\"\"\"

输出格式（JSON数组）：
[
  {{ "question": "...", "answer": "..." }},
  ...
]
"""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model,
        "temperature": 0.0,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    for _ in range(3):
        try:
            res = requests.post(f"{base_url}/chat/completions", json=payload, headers=headers)
            res.raise_for_status()
            text = res.json()["choices"][0]["message"]["content"]
            return eval(text) if isinstance(text, str) else text
        except Exception:
            time.sleep(1)
    return []

def ask_gpt_judgment(question, gold_answer, rag_answer, model, api_key, base_url):
    prompt = f"""
你是一个问答评估专家。
请判断以下两段回答是否在语义上表达了同一内容。
若表达内容一致，返回“是”，否则返回“否”。

问题：{question}
标准答案：{gold_answer}
RAG返回总结答案：{rag_answer}

请只回答“是”或“否”。
"""

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model,
        "temperature": 0.0,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    for _ in range(3):
        try:
            res = requests.post(f"{base_url}/chat/completions", json=payload, headers=headers)
            res.raise_for_status()
            content = res.json()["choices"][0]["message"]["content"].strip()
            return "是" if "是" in content else "否"
        except Exception:
            time.sleep(1)
    return "否"
