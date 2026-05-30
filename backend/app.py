import os
import redis
import requests  # 使用自选包
from flask import Flask, jsonify

app = Flask(__name__)

# 连接 Redis
redis_client = redis.Redis(
    host=os.getenv('REDIS_HOST', 'localhost'),
    port=os.getenv('REDIS_PORT', 6379),
    decode_responses=True
)

@app.route('/')
def hello():
    # 增加访问计数
    count = redis_client.incr('visit_count')
    
    # 使用自选包 requests 示例：获取公网 IP（演示用）
    try:
        ip_response = requests.get('https://httpbin.org/ip', timeout=3)
        ip_info = ip_response.json().get('origin', 'unknown')
    except:
        ip_info = 'unavailable'
    
    return jsonify({
        'message': 'Backend is running',
        'student_id': '2023112415',  # 替换为你的学号
        'student_name': '崔新愉',     # 替换为你的姓名
        'visit_count': count,
        'your_ip': ip_info
    })

@app.route('/health')
def health():
    return jsonify({'status': 'ok'})
@app.route('/api/ping', methods=['GET'])
def ping():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)