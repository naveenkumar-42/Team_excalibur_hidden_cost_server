from flask import Flask, request, jsonify
from flask_cors import CORS
from scraper import ScrapeProductInfo

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

scraper = ScrapeProductInfo()

@app.route('/scrape', methods=['POST'])
def scrape():
    data = request.get_json()
    url = data.get('url')
    result = scraper.identify_platform(url)
    return jsonify({'product_title': result[0], 'product_mrp': result[1], 'product_category':result[2], 'percentage':result[3],'product_selling_price':result[4]})

if __name__ == "__main__":
    app.run(debug=True)