# 🤖 CodeBuddy Agent

CodeBuddy Agent는 GitHub PR 생성 시 자동으로 코드를 리뷰하고 피드백을 제공하는 **서버리스 기반 AI 에이전트**입니다. 
GitHub Webhook을 통해 이벤트를 감지하고, 변경된 코드(Diff)를 분석하여 PR 코멘트로 즉각적인 피드백을 남깁니다.

## ✨ 주요 기능

- **자동화된 코드 리뷰**: PR 생성 및 업데이트 시 자동으로 변경된 코드를 수집합니다.
- **GitHub API 연동**: `PyGithub`를 활용하여 원활하고 안정적인 GitHub 데이터 조회 및 코멘트 작성을 지원합니다.
- **로컬 시뮬레이션 환경**: 실제 배포 전 `local_test.py`를 통해 안전하게 로컬에서 에이전트의 동작을 테스트할 수 있습니다.
- **서버리스 1클릭 배포**: AWS CloudFormation(SAM)을 통해 인프라 관리에 대한 부담 없이 손쉽게 클라우드에 배포할 수 있습니다.

## 📂 프로젝트 구조

- **`template.yaml`**: AWS 인프라 구축 및 배포를 위한 CloudFormation(SAM) 템플릿입니다.
- **`orchestrator.py`**: GitHub Webhook 이벤트를 수신하고, 전체 프로세스(코드 추출 -> 분석 -> 리뷰 작성)를 조율하는 메인 핸들러입니다.
- **`github_pr.py`**: GitHub API와 통신하여 PR Diff를 가져오고 코멘트를 등록하는 핵심 모듈입니다.
- **`local_test.py`**: AWS 환경 없이 로컬에서 웹훅 이벤트를 모의(Mock)로 발생시켜 에이전트를 테스트하는 스크립트입니다.

## 🚀 로컬 환경 설정 및 테스트

### 1. 패키지 설치
원활한 GitHub API 통신을 위해 `PyGithub` 라이브러리를 설치합니다.
```bash
pip install PyGithub
```

### 2. 환경 변수 설정
실제 PR에 코멘트를 남기려면 GitHub Personal Access Token이 필요합니다.
```bash
# Windows (CMD)
set GITHUB_TOKEN=your_personal_access_token

# Mac / Linux
export GITHUB_TOKEN="your_personal_access_token"
```
> **💡 참고**: `GITHUB_TOKEN`이 설정되지 않은 경우 코멘트 작성은 건너뛰고 안전한 모의(Mock) 모드로 실행됩니다.

### 3. 로컬 테스트 실행
로컬 환경에서 가상의 PR 이벤트를 발생시켜 에이전트의 동작을 확인합니다.
```bash
python local_test.py
```

## ☁️ AWS 배포 및 연동 방법

1. AWS Management Console에 접속하여 **CloudFormation** 서비스로 이동합니다.
2. **스택 생성**을 클릭하고 `template.yaml` 파일을 업로드합니다.
3. 파라미터 입력 단계에서 발급받은 `GITHUB_TOKEN`을 입력하여 스택 생성을 완료합니다.
4. 배포가 완료되면 생성된 **API Gateway 엔드포인트 URL**을 복사합니다.
5. 연동하고자 하는 GitHub 리포지토리의 `Settings` > `Webhooks`에 해당 URL을 등록합니다.
   - **Payload URL**: 복사한 엔드포인트 URL
   - **Content type**: `application/json`
   - **Events**: `Pull requests`