import os
import requests
from flask import Flask, render_template, request, jsonify
from urllib.parse import quote

app = Flask(__name__, template_folder='templates')

# =========================================================================
# 1. API 키 설정 (사용자님이 제공한 실제 키 값으로 업데이트됨)
# =========================================================================

# 네이버 API 키
NAVER_CLIENT_ID = os.getenv("NAVER_CLIENT_ID", "AgwStYnlHOuNUOOn7kiD")
NAVER_CLIENT_SECRET = os.getenv("NAVER_CLIENT_SECRET", "_ZBcX8Ec50")

# 유튜브 API 키
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "AIzaSyAM7Sc6RxrYBr_uSFCbSp8tuUGg9h2sPSM")

# =========================================================================
# 2. 페이지 라우트
# =========================================================================

@app.route('/')
def index():
    """메인 검색 페이지를 렌더링합니다."""
    return render_template('news_searcher.html')

@app.route('/game/tictactoe')
def tictactoe_game():
    """틱택토 게임 페이지를 렌더링합니다."""
    return render_template('tictactoe.html')

@app.route('/game/minesweeper')
def minesweeper_game():
    """지뢰 찾기 게임 페이지를 렌더링합니다."""
    return render_template('minesweeper.html')

@app.route('/game/memory')
def memory_game():
    """메모리 게임 페이지를 렌더링합니다."""
    return render_template('memory.html')

@app.route('/game/snake')
def snake_game():
    """뱀 게임 페이지를 렌더링합니다."""
    return render_template('snake.html')

@app.route('/game/pong')
def pong_game():
    """퐁 게임 페이지를 렌더링합니다."""
    return render_template('pong.html')

@app.route('/game/tetris')
def tetris_game():
    """테트리스 게임 페이지를 렌더링합니다."""
    return render_template('tetris.html')

@app.route('/game/sudoku')
def sudoku_game():
    """스도쿠 게임 페이지를 렌더링합니다."""
    return render_template('sudoku.html')

@app.route('/game/2048')
def game_2048():
    """2048 게임 페이지를 렌더링합니다."""
    return render_template('2048.html')

# --- 새로 추가된 과일 게임 라우트 ---
@app.route('/game/fruits')
def fruits_game():
    """과일 합치기 게임 페이지를 렌더링합니다."""
    return render_template('fruits_game.html')
# --------------------------------------

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

    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        'part': 'snippet',
        'q': query,
        'key': YOUTUBE_API_KEY,
        'type': 'video',
        'maxResults': 5,
        'regionCode': 'KR'
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.RequestException as e:
        app.logger.error(f"YouTube API request failed: {e}")
        return jsonify({"error": f"YouTube API error: {e}"}), 500

if __name__ == '__main__':
    # Render 환경에서 포트 충돌을 피하기 위해 host='0.0.0.0'을 사용하는 것이 좋습니다.
    app.run(debug=True, host='0.0.0.0', port=5000)