import json
import os
import sys

# lambda 디렉토리를 path에 추가하여 모듈을 임포트할 수 있게 설정
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'lambda'))
from orchestrator import lambda_handler

def run_local_test():
    # 가상의 GitHub PR Webhook 이벤트 데이터
    mock_event = {
        "headers": {
            "X-GitHub-Event": "pull_request"
        },
        "body": json.dumps({
            "action": "opened",
            "pull_request": {
                "number": 42,
                "title": "✨ feat: Add impressive AI features"
            },
            "repository": {
                "full_name": "developer/codebuddy-agent"
            }
        })
    }
    
    mock_context = {}  # Lambda 컨텍스트 객체 모의(Mock)

    print("\n" + "="*60)
    print(" 🤖 CodeBuddy Agent Local Simulation ".center(60, "="))
    print("="*60 + "\n")
    
    response = lambda_handler(mock_event, mock_context)
    
    print("\n" + "="*60)
    print(" ✅ [최종 결과] ".center(60, "="))
    print(f" 🔹 Status Code : {response.get('statusCode')}")
    print(f" 🔹 Response Body : {response.get('body')}")
    print("="*60 + "\n")

if __name__ == "__main__":
    run_local_test()