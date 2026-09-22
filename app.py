import os
import logging
from flask import Flask, render_template, request, jsonify, send_from_directory, make_response
from dotenv import load_dotenv
import google.generativeai as genai

# 로깅 설정 (Backend Log 출력)
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
)

# .env 파일 로드
load_dotenv()

# Vercel Serverless 및 로컬 환경 모두에서 정적/템플릿 경로를 안전하게 보장
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, 'templates'),
    static_folder=os.path.join(BASE_DIR, 'static')
)

# Gemini API Key 설정
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    logging.warning("⚠️ GEMINI_API_KEY가 .env 파일에 설정되지 않았습니다.")
else:
    genai.configure(api_key=api_key)

def build_prompt(name, job_title, experience, projects, tone, prompt_type, resume_style='classic'):
    """사용자 입력, 선택한 모드(A/B) 및 이력서 스타일(3종)에 맞춰 맞춤형 프롬프트를 구성합니다."""
    
    base_info = f"""
[사용자 기본 정보]
- 이름: {name}
- 지원 직무: {job_title}
- 톤앤매너(어조): {tone}
- 경력 사항:
{experience}
- 프로젝트 경험:
{projects}
"""

    # 1. 스타일에 따른 특화 작성 지침
    if resume_style == 'tech':
        style_guide = """
[선택 스타일: 🚀 테크 & 스타트업형 (Tech & Impact)]
- IT 기업, 개발자, 데이터/엔지니어 직무에 최적화된 형식입니다.
- 사용한 기술 스택(Tech Stack)과 개발 환경을 명확히 명시하세요.
- STAR 기법(상황-과제-행동-결과)을 철저히 적용하고, 수치화된 성과(예: 처리 속도 35% 단축, 트래픽 2배 수용 등)를 강조하여 기술적 문제 해결 역량을 입증하세요.
- 직관적이고 임팩트 있는 액션 위주의 문장으로 작성하세요.
"""
    elif resume_style == 'creative':
        style_guide = """
[선택 스타일: 🎨 크리에이티브 & 스토리텔링형 (Creative Storytelling)]
- 기획자, 마케터, 브랜딩, 크리에이티브 직무에 최적화된 형식입니다.
- 단순 업무 나열을 넘어 "어떤 문제를 발견하고, 어떤 창의적인 아이디어로 솔루션을 도출했는가"에 대한 매력적인 스토리텔링을 구축하세요.
- 지원자만의 시각, 일에 대한 철학, 사용자 중심의 인사이트 및 임팩트를 설득력 있게 풀어내세요.
"""
    else:  # classic
        style_guide = """
[선택 스타일: 🏛️ 클래식 & 전통형 (Standard Classic)]
- 대기업, 공기업, 금융권 등 신뢰와 격식을 중시하는 전형에 최적화된 서식입니다.
- 정갈하고 품격 있는 어휘와 체계적인 개조식(Bullet points) 형식을 적용하세요.
- 조직 내 역할, 업무 수행의 완결성, 성실성과 책임감이 드러나도록 균형 잡힌 구조로 작성하세요.
"""

    # 2. 모드(A/B)에 따른 구조 정의
    if prompt_type == 'B':
        mode_guide = """
[작성 모드: Mode B - 심화 모드 (전문가 컨설팅)]
- 전문 헤드헌터의 시선으로 지원자의 강점을 극대화하세요.
- 포맷 구성:
   - # [이력서] 지원자 이름 - 지원 직무
   - ## 전문 요약 (Executive Summary)
   - ## 핵심 역량 (Core Competencies)
   - ## 경력 및 성과 (Professional Experience)
   - ## 주요 프로젝트 상세 (Key Projects)
   - # [포트폴리오 요약]
   - ## 핵심 프로젝트 하이라이트 (문제 정의, 해결 솔루션, 기여도, 성과 및 러닝포인트)
"""
    else:
        mode_guide = """
[작성 모드: Mode A - 일반 모드 (표준 초안)]
- 친절한 커리어 멘토의 시선으로 읽기 편하고 균형 잡힌 초안을 완성하세요.
- 포맷 구성:
   - # [이력서] 지원자 이름 - 지원 직무
   - ## 자기소개 및 요약
   - ## 주요 기술 및 보유 역량
   - ## 경력 사항
   - ## 프로젝트 소개
   - # [포트폴리오 요약]
   - ## 프로젝트 개요 및 기여 내용
"""

    instruction = f"""
당신은 최고의 커리어 컨설턴트이자 테크/비즈니스 전문 라이터입니다.
아래 제공된 [스타일 지침]과 [작성 모드], 그리고 [사용자 기본 정보]를 충실히 반영하여
최고 수준의 맞춤형 이력서(Resume)와 포트폴리오 요약(Portfolio)을 완성해 주세요.

{style_guide}
{mode_guide}

[공통 규칙]
1. 사용자가 요청한 톤앤매너({tone})를 일관되게 유지하세요.
2. 결과물은 깔끔하고 가독성 높은 Markdown 문법으로만 출력하세요.
"""

    return f"{instruction}\n\n{base_info}\n\n위 원칙에 따라 이력서와 포트폴리오를 작성해 주세요."

@app.route('/sw.js')
@app.route('/api/sw.js')
@app.route('/api/index/sw.js')
def service_worker():
    """PWA Service Worker를 루트 스코프(/)로 서빙합니다."""
    response = make_response(send_from_directory(app.static_folder, 'sw.js'))
    response.headers['Content-Type'] = 'application/javascript'
    return response

@app.route('/manifest.json')
@app.route('/api/manifest.json')
@app.route('/api/index/manifest.json')
def manifest():
    """PWA Web App Manifest를 서빙합니다."""
    response = make_response(send_from_directory(app.static_folder, 'manifest.json'))
    response.headers['Content-Type'] = 'application/manifest+json'
    return response

@app.route('/static/<path:filename>')
def custom_static(filename):
    """정적 에셋(CSS, JS, 이미지 등)을 명시적으로 서빙합니다."""
    return send_from_directory(app.static_folder, filename)

@app.route('/')
@app.route('/api')
@app.route('/api/index')
def index():
    """메인 화면을 렌더링합니다."""
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
@app.route('/api/generate', methods=['POST'])
@app.route('/api/index/generate', methods=['POST'])
def generate():
    """사용자 입력을 받아 Gemini API를 호출하고 결과를 반환하는 REST API Route"""
    try:
        # 1. 요청 데이터 파싱
        data = request.get_json()
        if not data:
            logging.error("[요청 오류] JSON 데이터가 비어 있습니다.")
            return jsonify({'error': '요청 데이터가 전달되지 않았습니다.'}), 400

        name = data.get('name', '').strip()
        job_title = data.get('job_title', '').strip()
        experience = data.get('experience', '').strip()
        projects = data.get('projects', '').strip()
        tone = data.get('tone', '전문적이고 정중한').strip()
        prompt_type = data.get('prompt_type', 'A').strip().upper()
        resume_style = data.get('resume_style', 'classic').strip().lower()

        # 2. Backend 입력값 검증 (Validation)
        if not name:
            return jsonify({'error': '이름을 입력해 주세요.'}), 400
        if not job_title:
            return jsonify({'error': '지원 직무를 입력해 주세요.'}), 400
        if not experience:
            return jsonify({'error': '경력 사항을 입력해 주세요.'}), 400
        if not projects:
            return jsonify({'error': '프로젝트 경험을 입력해 주세요.'}), 400
        if prompt_type not in ['A', 'B']:
            prompt_type = 'A'
        if resume_style not in ['classic', 'tech', 'creative']:
            resume_style = 'classic'

        logging.info(f"[요청 접수] 이름: {name}, 직무: {job_title}, 스타일: {resume_style}, 모드: Prompt {prompt_type}, 톤: {tone}")

        # 3. API Key 존재 여부 확인
        current_api_key = os.getenv("GEMINI_API_KEY")
        if not current_api_key or current_api_key == "your_gemini_api_key_here":
            logging.error("[인증 오류] GEMINI_API_KEY가 올바르게 설정되지 않았습니다.")
            return jsonify({'error': '.env 파일에 올바른 GEMINI_API_KEY를 입력해 주세요.'}), 500

        # 4. 프롬프트 생성 및 Gemini 모델 호출
        prompt = build_prompt(name, job_title, experience, projects, tone, prompt_type, resume_style)
        
        # 모델 생성 (Google Gemini 최신 표준 모델)
        model = genai.GenerativeModel('gemini-3.6-flash')
        
        logging.info("[Gemini 호출] AI 생성 요청을 전송합니다...")
        response = model.generate_content(prompt)
        
        if not response or not response.text:
            logging.error("[응답 오류] Gemini API로부터 응답 텍스트를 받지 못했습니다.")
            return jsonify({'error': 'AI 응답을 생성하지 못했습니다. 다시 시도해 주세요.'}), 500

        result_text = response.text
        logging.info(f"[생성 완료] 응답 글자 수: {len(result_text)}자 반환 성공")

        return jsonify({
            'success': True,
            'result': result_text
        })

    except Exception as e:
        error_msg = str(e)
        logging.error(f"[서버 오류 발생] {error_msg}")
        
        # 초보자 친화적 오류 메시지 가공
        if "API_KEY_INVALID" in error_msg or "403" in error_msg:
            user_msg = "Gemini API 키가 유효하지 않습니다. .env 파일의 키를 확인해 주세요."
        elif "ResourceExhausted" in error_msg or "429" in error_msg:
            user_msg = "Gemini API 무료 사용량 한도를 초과했습니다. 잠시 후 다시 시도해 주세요."
        else:
            user_msg = f"생성 중 오류가 발생했습니다: {error_msg}"

        return jsonify({'error': user_msg}), 500

if __name__ == '__main__':
    # Flask 개발 서버 실행 (디버그 모드)
    app.run(debug=True, host='127.0.0.1', port=5000)
