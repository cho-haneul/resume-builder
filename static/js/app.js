// ==========================================================================
// AI Resume & Portfolio Builder - 프론트엔드 스크립트 (app.js)
// ==========================================================================

document.addEventListener('DOMContentLoaded', () => {
    // 1. 주요 HTML 요소 참조 가져오기
    const resumeForm = document.getElementById('resumeForm');
    const generateBtn = document.getElementById('generateBtn');
    const loadingIndicator = document.getElementById('loadingIndicator');
    const errorMessage = document.getElementById('errorMessage');
    const resultPlaceholder = document.getElementById('resultPlaceholder');
    const resultOutput = document.getElementById('resultOutput');
    const actionButtons = document.getElementById('actionButtons');
    const copyBtn = document.getElementById('copyBtn');
    const downloadBtn = document.getElementById('downloadBtn');

    // 2. 폼 제출 이벤트 핸들러
    resumeForm.addEventListener('submit', async (e) => {
        e.preventDefault(); // 폼 기본 새로고침 동작 방지

        // 에러 메시지 초기화
        hideError();

        // 입력값 가져오기
        const name = document.getElementById('name').value.trim();
        const jobTitle = document.getElementById('jobTitle').value.trim();
        const tone = document.getElementById('tone').value;
        const promptType = document.querySelector('input[name="prompt_type"]:checked').value;
        const resumeStyle = document.querySelector('input[name="resume_style"]:checked')?.value || 'classic';
        const experience = document.getElementById('experience').value.trim();
        const projects = document.getElementById('projects').value.trim();

        // [프론트엔드 검증] 빈칸 확인
        if (!name || !jobTitle || !experience || !projects) {
            showError('모든 필수 항목(*)을 입력해 주세요.');
            return;
        }

        // 로딩 UI 활성화
        setLoading(true);

        try {
            // Flask 백엔드 /generate 엔드포인트로 POST 요청 전송
            const response = await fetch('/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    name: name,
                    job_title: jobTitle,
                    tone: tone,
                    prompt_type: promptType,
                    resume_style: resumeStyle,
                    experience: experience,
                    projects: projects
                })
            });

            const data = await response.json();

            if (!response.ok) {
                // 서버에서 400 또는 500 에러를 반환한 경우
                throw new Error(data.error || '이력서 생성 중 오류가 발생했습니다.');
            }

            // 성공: 생성된 이력서 결과 화면에 표시
            displayResult(data.result);

        } catch (error) {
            console.error('생성 요청 오류:', error);
            showError(error.message);
        } finally {
            // 로딩 UI 해제
            setLoading(false);
        }
    });

    // 3. 내용 복사 버튼 클릭 이벤트
    copyBtn.addEventListener('click', async () => {
        const text = resultOutput.value;
        if (!text) return;

        try {
            await navigator.clipboard.writeText(text);
            const originalText = copyBtn.innerText;
            copyBtn.innerText = '✅ 복사 완료!';
            copyBtn.style.backgroundColor = '#38a169';
            copyBtn.style.color = '#ffffff';

            setTimeout(() => {
                copyBtn.innerText = originalText;
                copyBtn.style.backgroundColor = '';
                copyBtn.style.color = '';
            }, 2000);
        } catch (err) {
            alert('클립보드 복사에 실패했습니다. 수동으로 복사해 주세요.');
        }
    });

    // 4. Markdown 파일 다운로드 버튼 클릭 이벤트
    downloadBtn.addEventListener('click', () => {
        const text = resultOutput.value;
        if (!text) return;

        const name = document.getElementById('name').value.trim() || '이력서';
        const filename = `${name}_AI_이력서_포트폴리오.md`;

        // 파일 다운로드를 위한 임시 가상 링크 생성
        const blob = new Blob([text], { type: 'text/markdown;charset=utf-8;' });
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = filename;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(url);
    });

    // --- 헬퍼 함수들 ---

    // 로딩 상태 제어 함수
    function setLoading(isLoading) {
        if (isLoading) {
            generateBtn.disabled = true;
            generateBtn.innerText = '⏳ AI 작성 중...';
            loadingIndicator.style.display = 'block';
            resultPlaceholder.style.display = 'none';
            resultOutput.style.display = 'none';
            actionButtons.style.display = 'none';
        } else {
            generateBtn.disabled = false;
            generateBtn.innerText = '✨ AI 이력서 & 포트폴리오 생성하기';
            loadingIndicator.style.display = 'none';
        }
    }

    // 결과 표시 함수
    function displayResult(resultText) {
        resultPlaceholder.style.display = 'none';
        resultOutput.style.display = 'block';
        resultOutput.value = resultText;
        actionButtons.style.display = 'flex';
        hideError();
    }

    // 오류 메시지 표시 함수
    function showError(message) {
        errorMessage.innerText = '⚠️ ' + message;
        errorMessage.style.display = 'block';
    }

    // 오류 메시지 숨김 함수
    function hideError() {
        errorMessage.style.display = 'none';
        errorMessage.innerText = '';
    }
});
