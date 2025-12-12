from flask import Flask, render_template, request, jsonify
import requests
import os
import json # JSON 모듈 추가

app = Flask(__name__)

# 환경 변수에서 API 키 가져오기 (Render에서 설정했음)
NEWS_API_KEY = os.environ.get('NEWS_API_KEY')

# ==========================================================
# 1. 메인 인덱스 페이지 (새로 추가/수정)
# ==========================================================
@app.route('/')
def index():
    # 이제 /는 뉴스 검색기가 아닌, 카드 선택 페이지가 됩니다.
    return render_template('index.html')

# ==========================================================
# 2. 뉴스 검색기 페이지 (기존 /를 /news로 이동)
# ==========================================================
@app.route('/news', methods=['GET', 'POST'])
def news_searcher():
    # Render 환경에서 API 키가 설정되지 않았다면 예외 처리
    if not NEWS_API_KEY:
        return "Error: NEWS_API_KEY is not configured in environment variables.", 500

    news_data = None
    query = request.args.get('query')

    if query:
        url = f"https://newsapi.org/v2/everything?q={query}&language=ko&pageSize=10&apiKey={NEWS_API_KEY}"
        
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status() # HTTP 오류 발생 시 예외 발생
            data = response.json()
            
            # API 호출이 성공했으나 기사가 없는 경우
            if data['status'] == 'ok' and data['totalResults'] > 0:
                news_data = data['articles']
            else:
                news_data = [] # 검색 결과 없음
                
        except requests.exceptions.RequestException as e:
            print(f"API Request Error: {e}")
            return f"API 요청 중 오류 발생: {e}", 500

    return render_template('news_searcher.html', news_data=news_data, query=query)

# ==========================================================
# 3. 오목 게임 페이지
# ==========================================================
@app.route('/omok')
def omok():
    return render_template('omok.html')

# ==========================================================
# 4. 바둑 게임 페이지 (새로 추가)
# ==========================================================
@app.route('/baduk')
def baduk():
    return render_template('baduk.html')


if __name__ == '__main__':
    app.run(debug=True)