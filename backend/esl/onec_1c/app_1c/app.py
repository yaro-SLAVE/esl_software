# flask_app/app.py
from flask import Flask, jsonify, request
import requests
import os
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

ONC_SERVER = os.getenv('ONEC_URL', '')
ONC_USER = os.getenv('ONEC_LOGIN', '')
ONC_PASSWORD = os.getenv('ONEC_PASSWORD', '')

@app.route('/api/product/<id>', methods=['GET'])
def get_product_info(id):
    try:
        date_from = request.args.get('date_from')
        date_to = request.args.get('date_to')
        
        response = requests.get(
            f"{ONC_SERVER}/odata/standard.odata/{id}",
            params={
                '$filter': f"Date ge {date_from} and Date le {date_to}",
                '$format': 'json'
            },
            auth=(ONC_USER, ONC_PASSWORD),
            timeout=30
        )
        
        if response.status_code == 200:
            return jsonify({
                'status': 'success',
                'data': response.json(),
                'source': '1c'
            })
        else:
            return jsonify({
                'status': 'error',
                'message': f'1C returned status {response.status_code}'
            }), 502
            
    except requests.exceptions.RequestException as e:
        return jsonify({
            'status': 'error',
            'message': f'Error connecting to 1C: {str(e)}'
        }), 503
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Internal error: {str(e)}'
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)