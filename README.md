# 🌲 AI Resume & Portfolio Builder

> **Google Gemini AI와 Python Flask 기반의 맞춤형 이력서 및 포트폴리오 초안 자동 생성 웹 애플리케이션**

자연의 편안함을 담은 싱그러운 **포레스트 그린(Forest Green)** 테마와 함께, 지원자의 정보와 경력 사항을 분석하여 맞춤형 이력서와 포트폴리오 초안을 단 5초 만에 완성해 줍니다.

---

## ✨ 주요 기능 (Key Features)

1. **맞춤형 이력서 스타일 3종 선택**
   - **🏛️ 클래식 / 전통형 (Standard Classic)**: 대기업, 공기업, 금융권 맞춤의 정갈하고 격식 있는 개조식(Bullet points) 서식
   - **🚀 테크 & 스타트업형 (Tech & Impact)**: IT 기업, 개발자 맞춤으로 사용 기술 스택과 STAR 기법 기반의 수치화된 성과(Impact) 강조
   - **🎨 크리에이티브 / 스토리텔링형 (Storytelling & Branding)**: 기획자, 마케터 맞춤으로 문제 해결 여정과 창의적 인사이트 중심 서술

2. **프롬프트 모드 2종 지원**
   - **Mode A (일반 모드)**: 기본에 충실하고 읽기 편한 표준 초안
   - **Mode B (심화 모드)**: 전문 헤드헌터 관점의 역량 극대화 컨설팅 서식

3. **스마트한 프론트엔드 기능**
   - **원클릭 클립보드 복사**: 마우스 드래그 없이 전체 내용을 한 번에 복사
   - **Markdown (.md) 파일 즉시 다운로드**: 내 컴퓨터에 문서 파일로 바로 저장
   - **로딩 스피너 애니메이션**: 생성 대기 중 상태를 시각적으로 안내

4. **철저한 보안 및 안정성**
   - API Key는 `.env` 파일에서만 안전하게 관리 (Git 저장소 노출 원천 차단)
   - 프론트엔드와 백엔드 양방향 입력값 검증 (Validation)
   - 초보자 친화적 한국어 오류 안내 메시지

5. **모바일 반응형 웹 디자인 (Responsive Web)**
   - 데스크톱의 2단 카드 레이아웃과 스마트폰 환경의 1단 수직 정렬 완벽 대응

---

## 🛠️ 기술 스택 (Tech Stack)

| 구분 | 기술 / 라이브러리 | 설명 |
| :--- | :--- | :--- |
| **Backend** | Python 3.10+ | 주 프로그래밍 언어 |
| | Flask | 경량 웹 프레임워크 & REST API 라우팅 |
| | google-generativeai | Google Gemini 최신 모델 (`gemini-3.6-flash`) 연동 |
| | python-dotenv | 환경변수(`.env`) 안전 로드 |
| **Frontend** | HTML5 | 시맨틱 웹 구조 |
| | CSS3 | 포레스트 테마, Flexbox 2단 레이아웃, 미디어 쿼리 반응형 디자인 |
| | JavaScript (ES6+) | 비동기 `fetch` 통신, DOM 제어, 파일 다운로드 |
| **Version Control** | Git & GitHub | 버전 관리 및 세이브포인트 구축 |

---

## 📁 프로젝트 폴더 구조 (Project Structure)

```text
resume-builder/
├── app.py                  # Flask 백엔드 서버 및 Gemini API 연동 로직
├── requirements.txt        # 프로젝트 필수 의존성 패키지 목록
├── .env                    # 실제 비밀 API Key 보관 (Git 제외)
├── .env.example            # 환경변수 설정 가이드 템플릿
├── .gitignore              # Git 제외 파일 목록 (venv, .env 등)
├── README.md               # 프로젝트 문서 (현재 파일)
├── templates/
│   └── index.html          # 메인 입력 폼 및 결과 화면 템플릿
└── static/
    ├── css/
    │   └── style.css       # 포레스트 테마 및 반응형 스타일시트
    └── js/
        └── app.js          # 프론트엔드 비동기 요청 및 버튼 이벤트 스크립트
```

---

## 🚀 빠른 시작 가이드 (Quick Start)

### 1. 가상환경 생성 및 활성화 (Windows PowerShell)

```powershell
# 프로젝트 폴더로 이동
cd C:\AI-study\resume-builder

# 가상환경 생성
py -m venv venv

# 스크립트 실행 권한 허용 (필요 시)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process

# 가상환경 활성화 (프롬프트 맨 앞에 (venv) 확인)
.\venv\Scripts\Activate.ps1
```

### 2. 패키지 설치

```powershell
py -m pip install -r requirements.txt
```

### 3. Gemini API Key 설정

1. [Google AI Studio](https://aistudio.google.com/)에서 무료 API Key 발급
2. `.env.example`을 복사하여 `.env` 생성 후 본인의 키 입력:
```powershell
Copy-Item .env.example .env
notepad.exe .env
```
```text
# .env 내용 예시
GEMINI_API_KEY=AIzaSy...본인의_실제_키...
```

### 4. 웹 서버 실행

```powershell
py app.py
```

### 5. 웹 브라우저 접속

브라우저 주소창에 아래 URL을 입력합니다:
👉 **`http://127.0.0.1:5000`**

---

## 💡 사용 방법 (How to Use)

1. **기본 정보 입력**: 이름과 지원 직무를 입력합니다.
2. **문체 및 모드 선택**: 원하는 톤앤매너(신뢰감, 자신감 등)와 생성 모드(Mode A/B)를 고릅니다.
3. **이력서 스타일 선택**: 본인의 전형에 맞는 스타일(클래식 / 테크 / 크리에이티브)을 클릭합니다.
4. **경력 및 프로젝트 입력**: 담당했던 업무와 문제 해결 경험을 자유롭게 작성합니다.
5. **[✨ AI 이력서 & 포트폴리오 생성하기] 클릭**: 약 5초 후 완성된 초안을 확인합니다.
6. **복사 및 다운로드**: **[📋 내용 복사]** 또는 **[💾 Markdown 다운로드]** 버튼으로 결과물을 가져옵니다.

---

## 📄 라이선스 (License)

This project is created for study and portfolio demonstration purposes. Powered by Flask & Google Gemini.
