# rag_accuracy_evaluator/uploaders.py
import requests
import os

def default_uploader(file_path: str, filename: str, system_config: dict):
    """
    默认上传逻辑（支持 Authorization Token + 额外 URL 参数）
    """
    rag_cfg = system_config['rag']
    url = rag_cfg['upload_url']
    extra = rag_cfg.get('extra_fields', {})
    token = rag_cfg.get('auth_token')
    headers = {}

    if token:
        headers['Authorization'] = f"bearer {token}"

    # 将 extra_fields 中的 key 拼成 URL 参数
    if extra:
        from urllib.parse import urlencode
        url += '?' + urlencode(extra)

    with open(file_path, 'rb') as f:
        files = {'file': (filename, f.read())}
        response = requests.post(url, files=files, headers=headers)
        response.raise_for_status()
        return response.text or response.status_code



def search_interface(keyword: str, system_config: dict, limit: int = 5):
    """
    支持 GET 请求调用 search 接口，从 extra_fields 中获取查询参数（如 name）
    """
    rag_cfg = system_config['rag']
    url = rag_cfg['search_url']
    token = rag_cfg.get('auth_token')
    extra = rag_cfg.get('extra_fields', {})

    # 构造查询参数：keyword + extra_fields + limit
    params = {**extra, "keyword": keyword}

    headers = {}
    if token:
        headers['Authorization'] = f"bearer {token}"

    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()
    return response.json()