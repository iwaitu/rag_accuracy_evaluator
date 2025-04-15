# rag_accuracy_evaluator/uploaders.py
import requests
import os

def default_uploader(file_path: str, filename: str, system_config: dict):
    """
    默认上传逻辑：
    - 使用 multipart/form-data
    - 支持附加字段（tags, section 等）
    - 用户可根据实际接口结构重写此函数
    """
    url = system_config['rag']['upload_url']
    extra = system_config['rag'].get('extra_fields', {})
    
    with open(file_path, 'rb') as f:
        files = {'file': (filename, f.read())}
        response = requests.post(url, files=files, data=extra)
        response.raise_for_status()
        return response.text or response.status_code


def json_uploader(file_path: str, filename: str, system_config: dict):
    """
    可选 JSON 上传方式
    - 文件内容 base64 编码 + json 提交
    """
    import base64
    with open(file_path, 'rb') as f:
        file_data = base64.b64encode(f.read()).decode('utf-8')

    payload = {
        'filename': filename,
        'content': file_data,
        **system_config['rag'].get('extra_fields', {})
    }
    headers = {'Content-Type': 'application/json'}
    url = system_config['rag']['upload_url']
    res = requests.post(url, json=payload, headers=headers)
    res.raise_for_status()
    return res.text or res.status_code