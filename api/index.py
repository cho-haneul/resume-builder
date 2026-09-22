import os
import sys

# Vercel Serverless Function 환경에서 프로젝트 루트 경로를 sys.path에 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

# Vercel은 WSGI callable인 app 객체를 감지하여 구동합니다.
