# rag_accuracy_evaluator/evaluator.py
import os
import yaml
import requests
import glob
from openai_helpers import generate_questions_and_answers, ask_gpt_judgment
from utils import get_embedding, calculate_cosine_similarity
from report import generate_html_report
from interfacehelper import default_uploader

class RAGEvaluator:
    def __init__(self, config_path: str):
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)

        self.results = []
        self.input_dir = self.config['input_dir']
        self.output_dir = self.config['output_dir']
        self.q_per_doc = self.config.get('questions_per_doc', 10)
        self.mode = self.config.get('mode', 'model-vs-model')
        self.standard_model_name = self.config.get('standard_model')
        self.systems = self.config['systems']

    def run_all(self):
        os.makedirs(self.output_dir, exist_ok=True)

        standard_model_cfg = next(s for s in self.systems if s['name'] == self.standard_model_name)

        for file_path in glob.glob(os.path.join(self.input_dir, '*.*')):
            filename = os.path.basename(file_path)
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()

            qa_pairs = generate_questions_and_answers(
                text,
                standard_model_cfg['openai']['model'],
                standard_model_cfg['openai']['api_key'],
                standard_model_cfg['openai']['base_url'],
                self.q_per_doc
            )

            for system in self.systems:
                system_name = system['name']
                rag_cfg = system['rag']
                model_cfg = system['openai']

                # 使用可替换上传器
                if not system.get("skip_upload", False):
                    default_uploader(file_path, filename, system)

                for qa in qa_pairs:
                    q = qa['question']
                    a = qa['answer']

                    res = requests.get(rag_cfg['search_url'], json={"query": q})
                    res.raise_for_status()
                    search_results = res.json()
                    chunks = search_results[:5] if isinstance(search_results, list) else search_results.get('results', [])[:5]
                    chunk_texts = [c.get(rag_cfg['text_field'], '') for c in chunks]
                    joined = "\n".join(chunk_texts)

                    rag_summary = generate_questions_and_answers(joined, model_cfg['model'], model_cfg['api_key'], model_cfg['base_url'], 1)[0]['answer']
                    judge = ask_gpt_judgment(q, a, rag_summary, model_cfg['model'], model_cfg['api_key'], model_cfg['base_url'])
                    vec_gold = get_embedding(a, model_cfg['api_key'], model_cfg['base_url'])
                    vec_pred = get_embedding(rag_summary, model_cfg['api_key'], model_cfg['base_url'])
                    cos_sim = calculate_cosine_similarity(vec_gold, vec_pred)

                    score = 1.0 if judge == '是' and cos_sim >= 0.8 else 0.5 if judge == '是' or cos_sim >= 0.8 else 0.0

                    self.results.append({
                        'system': system_name,
                        'filename': filename,
                        'question': q,
                        'standard_answer': a,
                        'rag_summary_answer': rag_summary,
                        'llm_judgment': judge,
                        'cosine_score': cos_sim,
                        'final_score': score
                    })

    def generate_html_report(self):
        output_path = os.path.join(self.output_dir, "rag_accuracy_report.html")
        generate_html_report(self.results, output_path)
        print(f"✅ 评估报告已生成: {output_path}")
