# backend/conftest.py
import os
import sys

# 현재 파일의 경로를 구함
current_dir = os.path.dirname(os.path.abspath(__file__))

# sys.path에 현재 디렉토리 추가
if current_dir not in sys.path:
    sys.path.append(current_dir)