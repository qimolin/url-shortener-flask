from flask import Flask, request, redirect
from url import URL

app = Flask(__name__)
url_processor = URL()

@app.post('/')
def shorten_url():

    data = request.get_json()
    original_url = data.get('value')
    shortened_url = url_processor.generate_shortened_url(original_url)
    
    status_code = 201 if shortened_url != "Invalid URL" else 400

    return {"id": shortened_url}, status_code

@app.get('/')
def get_all_urls():
    all_urls = url_processor.get_all_urls()
    return all_urls, 200

@app.delete('/')
def delete_all_urls():
    deleted = url_processor.delete_all_urls()
    return deleted, 404

@app.get('/<id>')
def get_original_url(id):
    original_url = url_processor.get_original_url(id)
    
    if original_url:
        # return redirect(original_url, code=301)
        return {"value": original_url}, 301
    return "URL not found", 404

@app.put('/<id>')
def update_original_url(id):
    new_url = request.get_json().get('url')
    updated_url = url_processor.update_original_url(id, new_url)
    
    if updated_url == "Invalid URL":
        status_code = 400
    elif updated_url == "URL not found":
        status_code = 404
    else:
        status_code = 200
        
    return {"value":updated_url}, status_code

@app.delete('/<id>')
def delete_original_url(id):
    deleted = url_processor.delete_original_url(id)
    status_code = 204 if deleted == "URL deleted" else 404
    return deleted, status_code

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)