# rag_accuracy_evaluator/report.py
import os
import matplotlib.pyplot as plt
from jinja2 import Template
from datetime import datetime
from collections import defaultdict

plt.style.use('dark_background')

def generate_html_report(results: list, output_path: str):
    # 按系统分组统计准确率
    system_doc_scores = defaultdict(lambda: defaultdict(list))

    for entry in results:
        system = entry['system']
        doc = entry['filename']
        system_doc_scores[system][doc].append(entry['final_score'])

    # 每系统每文档准确率 & 系统平均准确率
    doc_avg = defaultdict(dict)
    system_avg = {}

    for system, docs in system_doc_scores.items():
        total_score = 0
        count = 0
        for doc, scores in docs.items():
            avg = sum(scores) / len(scores)
            doc_avg[system][doc] = avg
            total_score += avg
            count += 1
        system_avg[system] = total_score / count if count > 0 else 0

    # 绘图（系统准确率对比）
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(system_avg.keys(), system_avg.values(), color='skyblue')
    ax.set_title('System Average Accuracy')
    ax.set_ylabel('Accuracy')
    ax.set_ylim(0, 1)
    plt.xticks(rotation=20)
    plt.tight_layout()

    chart_path = os.path.join(os.path.dirname(output_path), 'accuracy_chart.png')
    plt.savefig(chart_path)
    plt.close()

    # HTML 模板
    html_template = Template("""
    <html style="background-color:#111;color:#eee;font-family:sans-serif;">
    <head><meta charset="utf-8"><title>RAG Accuracy Report</title></head>
    <body>
        <h1>📊 RAG 检索准确率评估报告</h1>
        <p>生成时间：{{ time }}</p>
        <h2>系统平均准确率</h2>
        <img src="accuracy_chart.png" style="max-width:100%;">

        {% for system in system_names %}
        <h3>系统：{{ system }}</h3>
        <table border="1" cellspacing="0" cellpadding="4" style="border-collapse:collapse;width:100%;color:#ccc;">
            <tr style="background-color:#333;">
                <th>文件</th><th>问题</th><th>标准答案</th><th>RAG回答</th>
                <th>GPT判断</th><th>相似度</th><th>得分</th>
            </tr>
            {% for r in results if r.system == system %}
            <tr>
                <td>{{ r.filename }}</td>
                <td>{{ r.question }}</td>
                <td>{{ r.standard_answer }}</td>
                <td>{{ r.rag_summary_answer }}</td>
                <td>{{ r.llm_judgment }}</td>
                <td>{{ '%.4f'|format(r.cosine_score) }}</td>
                <td>{{ r.final_score }}</td>
            </tr>
            {% endfor %}
        </table>
        {% endfor %}
    </body>
    </html>
    """)

    html_content = html_template.render(
        time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        system_names=list(system_avg.keys()),
        results=results
    )

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)