import os
from github import Github, GithubException

def get_github_client() -> Github:
    """GitHub 클라이언트 객체를 생성하고 인증합니다."""
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        raise ValueError("GITHUB_TOKEN 환경 변수가 설정되지 않았습니다.")
    return Github(token)

def get_pr_changes(repo_name: str, pr_number: int) -> list:
    """GitHub PR에서 변경된 파일 목록과 코드 Diff를 가져옵니다."""
    try:
        g = get_github_client()
        repo = g.get_repo(repo_name)
        pr = repo.get_pull(pr_number)
        
        changes = []
        for file in pr.get_files():
            changes.append({
                "filename": file.filename,
                "status": file.status,
                "patch": file.patch  # 실제 코드 Diff 데이터
            })
        return changes
    except GithubException as e:
        print(f"❌ [GitHub API Error] PR 정보를 가져오지 못했습니다: {e}")
        return []

def post_review_comment(repo_name: str, pr_number: int, comment_body: str) -> bool:
    """분석 및 리팩토링 결과를 PR 코멘트로 등록합니다."""
    try:
        g = get_github_client()
        repo = g.get_repo(repo_name)
        pr = repo.get_pull(pr_number)
        pr.create_issue_comment(comment_body)
        return True
    except GithubException as e:
        print(f"❌ [GitHub API Error] 코멘트 등록에 실패했습니다: {e}")
        return False