# news_app/app.py
import json
import requests
from flask import Flask, render_template, request, jsonify

# Flask 애플리케이션 인스턴스 생성
app = Flask(__name__)

# --- API 키 및 기본 설정 (실제 키로 대체 필요) ---
NAVER_CLIENT_ID = "YOUR_NAVER_CLIENT_ID" # 실제 ID로 대체하세요
NAVER_CLIENT_SECRET = "YOUR_NAVER_CLIENT_SECRET" # 실제 Secret으로 대체하세요


# --- 1. UI 라우팅 (페이지 렌더링) ---
# 404 오류 방지를 위해 슬래시 버전과 슬래시 없는 버전을 모두 정의합니다.
# (URL 경로를 정의합니다.)

@app.route('/')
def index_view():
    """메인 페이지 렌더링 (index.html)"""
    return render_template('index.html')

@app.route('/omok')
@app.route('omok')
def omok_view():
    """오목 페이지 렌더링 (omok.html)"""
    return render_template('omok.html')

@app.route('/searcher')
@app.route('searcher')
def news_searcher_view():
    """뉴스 검색기 페이지 렌더링 (news_searcher.html)"""
    return render_template('news_searcher.html')

@app.route('/baduk')
@app.route('baduk')
def baduk_view():
    """바둑 페이지 렌더링 (baduk.html)"""
    return render_template('baduk.html')


# --- 2. API 라우팅 (뉴스 검색 로직) ---

@app.route('/api/search_news/', methods=['POST'])
def search_news():
    """
    키워드를 받아 네이버 뉴스 검색 API를 호출하고 결과를 JSON 형태로 반환합니다.
    """
    if request.method == 'POST':
        try:
            # POST 요청 본문에서 JSON 데이터 파싱
            data = request.get_json()
            keyword = data.get('keyword', '')
            
            if not keyword:
                return jsonify({'error': '키워드가 필요합니다.'}), 400

            # 네이버 API 호출 설정
            headers = {
                'X-Naver-Client-Id': NAVER_CLIENT_ID,
                'X-Naver-Client-Secret': NAVER_CLIENT_SECRET
            }
            url = "https://openapi.naver.com/v1/search/news.json"
            params = {
                'query': keyword,
                'display': 10,
                'sort': 'date'
            }

            # API 요청 및 응답 처리
            response = requests.get(url, headers=headers, params=params)
            
            if response.status_code == 200:
                # 성공 시, 네이버 API 결과를 JSON 형태로 클라이언트에 전달
                return jsonify(response.json())
            else:
                # 네이버 API 오류 발생 시
                return jsonify({
                    'error': f"네이버 API 호출 오류: {response.status_code}",
                    'detail': response.text
                }), response.status_code

        except Exception as e:
            # 예외 처리: 로그 출력 후 500 응답
            print(f"Server Error: {e}")
            return jsonify({'error': f'서버 내부 오류: {str(e)}'}), 500

    return jsonify({'error': 'POST 요청만 허용됩니다.'}), 404

if __name__ == '__main__':
    # 로컬 개발 환경에서만 사용
    app.run(debug=True)