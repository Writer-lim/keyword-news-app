from flask import Flask, render_template, request, jsonify
import requests

# Flask 애플리케이션 생성
app = Flask(__name__)

# 발급받은 API 키를 여기에 넣으세요! (키가 정확한지 확인해주세요)
NEWS_API_KEY = '82d7161a9739477682aad3df4d5b6ab6' 
NEWS_API_ENDPOINT = 'https://newsapi.org/v2/everything'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search_news():
    keyword = request.args.get('keyword')

    if not keyword:
        return jsonify({'articles': []})
    
    params = {
        'q': keyword,
        'apiKey': NEWS_API_KEY,
        'sortBy': 'publishedAt',
        'language': 'ko' 
    }

    try:
        response = requests.get(NEWS_API_ENDPOINT, params=params)
        response.raise_for_status()
        data = response.json()
        
        return jsonify(data)
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching news: {e}")
        return jsonify({'error': '뉴스 검색 중 오류가 발생했습니다.'}), 500

@app.route('/omok')
def omok():
    return render_template('omok.html')

if __name__ == '__main__':
    app.run(debug=True)