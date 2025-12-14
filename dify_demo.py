import requests
import json

# ================= 配置区域 =================
# 1. 替换为你的 Dify API Key
API_KEY = "app-5Yr8fCQjgtXSVvdUFbbAdygu" 

# 2. 如果是私有部署，请替换为你的域名；如果是云端版，保持不变
BASE_URL = "https://api.dify.ai/v1"

# ================= 调用函数 =================
def generate_seed(protocol, implementation, initial_seed):
    """
    调用 Dify 工作流生成丰富后的种子 (修正解析版)
    """
    url = f"{BASE_URL}/workflows/run"
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "inputs": {
            "protocol": protocol,
            "protocol_inplem": implementation,
            "seed": initial_seed
        },
        "response_mode": "blocking",
        "user": "fuzzing-bot-001"
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        
        result_json = response.json()
        
        # --- 核心修改点 START ---
        # 1. status 字段藏在 data 里面，不在最外层
        workflow_data = result_json.get("data", {})
        run_status = workflow_data.get("status")
        
        if run_status == "succeeded":
            # 2. 获取输出
            outputs = workflow_data.get("outputs", {})
            
            # 3. 这里的键名取决于你的 End 节点配置
            # 如果你还没有接 Python 节点，通常是 'text'
            # 如果你接了 Python 节点并发布了，应该是 'result'
            final_seed = outputs.get("result") or outputs.get("text")
            return final_seed
        # --- 核心修改点 END ---
        
        else:
            print(f"Workflow 状态异常: {run_status}")
            print(f"完整响应: {result_json}")
            return None

    except Exception as e:
        print(f"请求发生错误: {e}")
        return None

# ================= 主程序测试 =================
if __name__ == "__main__":
    # 测试数据
    proto = "FTP"
    implem = "ProFTPD 1.3.3"
    with open("D:\enrich_agent\seeds\in-proftpd\seed_1.raw", "r", encoding="utf-8") as f:
        raw_seed = f.read()

    print("正在请求 Dify 生成种子...")
    new_seed = generate_seed(proto, implem, raw_seed)

    if new_seed:
        print("-" * 20)
        print("生成成功！")
        # 使用 repr() 打印，以便看清 \r\n 是否存在
        print(f"原始内容 (Repr): {repr(new_seed)}")
        
        # 写入文件演示（Fuzzing 常用操作）
        with open("new_seed.txt", "wb") as f:
            f.write(new_seed.encode('utf-8'))
        print("已保存到 new_seed.txt")
        print("-" * 20)
    else:
        print("生成失败。")