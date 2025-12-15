import os
import requests
from flask import Flask, render_template, request, jsonify
from urllib.parse import quote

app = Flask(__name__, template_folder='templates')

# 네이버 API 키 (환경 변수에서 가져오거나 직접 설정)
NAVER_CLIENT_ID = os.getenv("NAVER_CLIENT_ID", "YOUR_NAVER_CLIENT_ID")
NAVER_CLIENT_SECRET = os.getenv("NAVER_CLIENT_SECRET", "YOUR_NAVER_CLIENT_SECRET")

# 유튜브 API 키 (환경 변수에서 가져오거나 직접 설정)
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "YOUR_YOUTUBE_API_KEY")

# =========================================================================
# 1. 메인 검색 페이지 라우트
# =========================================================================
@app.route('/')
def index():
    """메인 검색 페이지를 렌더링합니다."""
    return render_template('news_searcher.html')

# =========================================================================
# 2. 게임 페이지 라우트 (추가됨)
# =========================================================================
@app.route('/game/tictactoe')
def tictactoe_game():
    """틱택토 게임 페이지를 렌더링합니다."""
    return render_template('tictactoe.html')

# =========================================================================
# 3. 네이버 뉴스 검색 API 엔드포인트
# =========================================================================
@app.route('/api/search_news')
def search_news():
    query = request.args.get('query')
    if not query:
        return jsonify({"error": "Query parameter is missing"}), 400

    enc_text = quote(query)
    url = f"https://openapi.naver.com/v1/search/news.json?query={enc_text}&display=5&sort=sim"
    
    headers = {
        "X-Naver-Client-Id": NAVER_CLIENT_ID,
        "X-Naver-Client-Secret": NAVER_CLIENT_SECRET
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status() 
        return jsonify(response.json())
    except requests.RequestException as e:
        app.logger.error(f"Naver News API request failed: {e}")
        return jsonify({"error": f"Naver News API error: {e}"}), 500

# =========================================================================
# 4. 네이버 이미지 검색 API 엔드포인트
# =========================================================================
@app.route('/api/search_image')
def search_image():
    query = request.args.get('query')
    if not query:
        return jsonify({"error": "Query parameter is missing"}), 400

    enc_text = quote(query)
    # 이미지 검색 API 설정 (최신 순으로 5개)
    url = f"https://openapi.naver.com/v1/search/image.json?query={enc_text}&display=5&sort=date"
    
    headers = {
        "X-Naver-Client-Id": NAVER_CLIENT_ID,
        "X-Naver-Client-Secret": NAVER_CLIENT_SECRET
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.RequestException as e:
        app.logger.error(f"Naver Image API request failed: {e}")
        return jsonify({"error": f"Naver Image API error: {e}"}), 500

# =========================================================================
# 5. 유튜브 영상 검색 API 엔드포인트
# =========================================================================
@app.route('/api/search_youtube')
def search_youtube():
    query = request.args.get('query')
    if not query:
        return jsonify({"error": "Query parameter is missing"}), 400

    # YouTube Data API v3 검색 엔드포인트
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        'part': 'snippet',
        'q': query,
        'key': YOUTUBE_API_KEY,
        'type': 'video',
        'maxResults': 5,
        'regionCode': 'KR' # 한국 지역 코드로 검색 결과 선호
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.RequestException as e:
        app.logger.error(f"YouTube API request failed: {e}")
        return jsonify({"error": f"YouTube API error: {e}"}), 500

if __name__ == '__main__':
    # Render 환경에서 Gunicorn 등이 Flask 앱을 실행하므로, 로컬 테스트용으로만 사용
    app.run(debug=True, host='0.0.0.0', port=5000)