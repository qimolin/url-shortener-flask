from flask import Flask, request
from url import URL

app = Flask(__name__)
url_processor = URL()

@app.route('/')
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/shorten', methods=['POST'])
def shorten_url():

    data = request.get_json()
    original_url = data.get('url')
    shortened_url = url_processor.generate_shortened_url(original_url)

    return(shortened_url)

@app.route('/original', methods=['GET'])
def get_original_url():
    return "TODO"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)