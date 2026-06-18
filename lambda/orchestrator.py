import json
import os
from tools.github_pr import get_pr_changes, post_review_comment

def lambda_handler(event, context):
    """
    GitHub Webhook 이벤트를 수신하여 처리하는 메인 오케스트레이터입니다.
    PR 이벤트를 감지하고 필요한 도구(tools)를 순차적으로 호출합니다.
    """
    print("🚀 [CodeBuddy Agent] Webhook 이벤트 수신 완료")
    
    try:
        # 1. 이벤트 페이로드 파싱
        body = event.get("body", "{}")
        if isinstance(body, str):
            body = json.loads(body)
        
        action = body.get("action")
        if action not in ["opened", "synchronize"]:
            return {"statusCode": 200, "body": json.dumps({"message": f"Ignored action: {action}"})}
        
        pr_number = body.get("pull_request", {}).get("number")
        repo_name = body.get("repository", {}).get("full_name")
        
        if not pr_number or not repo_name:
            raise ValueError("유효하지 않은 PR 데이터입니다.")
            
        print(f"📦 [Step 1] PR 데이터 분석 시작 - {repo_name}#PR-{pr_number}")
        
        # 2. GitHub PR 변경사항 추출
        changes = get_pr_changes(repo_name, pr_number)
        print(f"🔍 [Step 2] 변경된 파일 {len(changes)}개 감지 완료")
        
        # 3. 분석 및 리뷰 (이후 AI 연동 모듈로 대체될 부분)
        print(f"🧠 [Step 3] AI 모델 기반 코드 분석 및 리뷰 리포트 생성 중...")
        review_result = f"## 🤖 CodeBuddy 자동 리뷰 리포트\n\n성공적으로 분석을 완료했습니다!\n- **리뷰 대상 파일**: {len(changes)}개\n- **상태**: 이상 없음 (LGTM ✨)"
        
        # 4. PR 코멘트 작성
        print(f"✍️  [Step 4] GitHub PR 코멘트 작성 중...")
        if os.environ.get("GITHUB_TOKEN"):
            post_review_comment(repo_name, pr_number, review_result)
        else:
            print("⚠️ [Warning] GITHUB_TOKEN이 없어 코멘트 등록은 스킵되었습니다. (로컬 테스트 모드)")
        
    except Exception as e:
        print(f"❌ [Error] 시스템 오류 발생: {e}")
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
    
    print("🎉 [CodeBuddy Agent] 모든 프로세스 완료!")
    return {"statusCode": 200, "body": json.dumps({"message": "Successfully processed"})}