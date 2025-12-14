# news_app/app.py
import json
import requests
from flask import Flask, render_template, request, jsonify

# Flask 애플리케이션 인스턴스 생성
app = Flask(__name__)

# --- API 키 및 기본 설정 ---
# 🚨🚨🚨 실제 Client ID와 Secret으로 교체되어야 합니다! 🚨🚨🚨
NAVER_CLIENT_ID = "AgwStYnlHOuNUOOn7kiD" 
NAVER_CLIENT_SECRET = "_ZBcX8Ec50" 

# 🚨🚨🚨 최종 적용된 YouTube Data API Key 🚨🚨🚨
YOUTUBE_API_KEY = "AIzaSyAM7Sc6RxrYBr_uSFcbSp8tuUGg9h2sPSM"


# --- 1. UI 라우팅 (페이지 렌더링) ---
@app.route('/')
def index_view():
    """메인 페이지 렌더링 (index.html)"""
    return render_template('index.html')

@app.route('/omok')
def omok_view():
    """오목 페이지 렌더링 (omok.html)"""
    return render_template('omok.html')

@app.route('/searcher')
def news_searcher_view():
    """뉴스 검색기 페이지 렌더링 (news_searcher.html)"""
    return render_template('news_searcher.html')

@app.route('/baduk')
def baduk_view():
    """바둑 페이지 렌더링 (baduk.html)"""
    return render_template('baduk.html')


# --- 2. 뉴스 검색 API 라우팅 ---

@app.route('/api/search_news/', methods=['POST'])
def search_news():
    if request.method == 'POST':
        try:
            data = request.get_json()
            keyword = data.get('keyword', '')
            
            if not keyword:
                return jsonify({'error': '키워드가 필요합니다.'}), 400

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

            response = requests.get(url, headers=headers, params=params)
            
            if response.status_code == 200:
                return jsonify(response.json())
            else:
                return jsonify({
                    'error': f"네이버 API 호출 오류: {response.status_code}",
                    'detail': response.text
                }), response.status_code

        except Exception as e:
            print(f"Server Error: {e}")
            return jsonify({'error': f'서버 내부 오류: {str(e)}'}), 500

    return jsonify({'error': 'POST 요청만 허용됩니다.'}), 404

# --- 3. 이미지 검색 API 라우팅 ---

@app.route('/api/search_image/', methods=['POST'])
def search_image():
    if request.method == 'POST':
        try:
            data = request.get_json()
            keyword = data.get('keyword', '')
            
            if not keyword:
                return jsonify({'error': '키워드가 필요합니다.'}), 400

            headers = {
                'X-Naver-Client-Id': NAVER_CLIENT_ID,
                'X-Naver-Client-Secret': NAVER_CLIENT_SECRET
            }
            url = "https://openapi.naver.com/v1/search/image" 
            params = {
                'query': keyword,
                'display': 5,
                'sort': 'sim'
            }

            response = requests.get(url, headers=headers, params=params)
            
            if response.status_code == 200:
                return jsonify(response.json())
            else:
                return jsonify({
                    'error': f"네이버 이미지 API 호출 오류: {response.status_code}",
                    'detail': response.text
                }), response.status_code

        except Exception as e:
            print(f"Image Server Error: {e}")
            return jsonify({'error': f'서버 내부 오류: {str(e)}'}), 500

    return jsonify({'error': 'POST 요청만 허용됩니다.'}), 404

# --- 4. 유튜브 검색 API 라우팅 ---

@app.route('/api/search_youtube/', methods=['POST'])
def search_youtube():
    """
    키워드를 받아 YouTube Data API를 호출하고 결과를 JSON 형태로 반환합니다.
    """
    if request.method == 'POST':
        try:
            data = request.get_json()
            keyword = data.get('keyword', '')
            
            if not keyword:
                return jsonify({'error': '키워드가 필요합니다.'}), 400
            
            # API 키가 설정되지 않은 경우를 대비한 가드
            if YOUTUBE_API_KEY == "YOUR_YOUTUBE_API_KEY":
                return jsonify({
                    'error': "YouTube API Key가 설정되지 않았습니다. app.py 파일의 YOUTUBE_API_KEY를 실제 키로 교체해 주십시오."
                }), 403 # Forbidden

            # YouTube API 호출 설정
            url = "https://www.googleapis.com/youtube/v3/search"
            params = {
                'part': 'snippet',
                'q': keyword,
                'key': YOUTUBE_API_KEY,
                'type': 'video',
                'maxResults': 5  # 영상 5개만 표시
            }

            response = requests.get(url, params=params)
            
            if response.status_code == 200:
                return jsonify(response.json())
            else:
                # YouTube API 오류 상세 정보 전달
                error_detail = response.json().get('error', {}).get('message', '알 수 없는 오류')
                return jsonify({
                    'error': f"YouTube API 호출 오류: {response.status_code}",
                    'detail': error_detail
                }), response.status_code

        except Exception as e:
            print(f"Youtube Server Error: {e}")
            return jsonify({'error': f'서버 내부 오류: {str(e)}'}), 500

    return jsonify({'error': 'POST 요청만 허용됩니다.'}), 404

if __name__ == '__main__':
    app.run(debug=True)