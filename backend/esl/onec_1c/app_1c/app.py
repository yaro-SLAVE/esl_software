from flask import Flask, jsonify
import requests
import os
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()

ONEC_URL = os.getenv('ONEC_URL', '')
ONEC_LOGIN = os.getenv('ONEC_LOGIN', '')
ONEC_PASSWORD = os.getenv('ONEC_PASSWORD', '')

@staticmethod
def send_request(url, filter=None):
    if filter is not None:
        response = requests.get(
            f"{ONEC_URL}/odata/standard.odata/{url}?$format=json&$filter={filter.replace(' ', '%20').replace("'", "'")}",
            auth=(ONEC_LOGIN, ONEC_PASSWORD),
            timeout=30
        )
    else:
        response = requests.get(
            f"{ONEC_URL}/odata/standard.odata/{url}?$format=json",
            auth=(ONEC_LOGIN, ONEC_PASSWORD),
            timeout=30
        )

    return response


@app.route('/api/product', methods=['GET'])
def get_products_list():
    try:
        response_products = send_request("Catalog_Номенклатура")
        
        products = response_products.json().get('value')

        products_data = []
        for product in products:
            products_data.append({
                'id': product.get('Ref_Key'),
                'short_name': product.get('Description'),
                'description': product.get('Комментарий'),
            })

        return products_data
            
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

@app.route('/api/product/<id>', methods=['GET'])
def get_product_info(id):
    try:
        response_product = send_request(f"Catalog_Номенклатура(guid'{id}')")

        response_fix_price = send_request('InformationRegister_ЦеныНоменклатуры', f"Номенклатура_Key eq guid'{id}'")

        response_prices = send_request("Document_УстановкаЦенНоменклатуры")
        
        product = response_product.json()
        prices = response_prices.json().get('value')
        prices = prices[len(prices) - 1].get('Запасы')
        fix_price = response_fix_price.json().get('value')

        price = next((item for item in prices if item['Номенклатура_Key'] == product.get('Ref_Key')), None)

        if price is not None:
            product_data = {
                'id': product.get('Ref_Key'),
                'short_name': product.get('Description'),
                'description': product.get('Комментарий'),
                'price': price.get('Цена'),
                'old_price': price.get('ЦенаСтарая')
            }

        else:
            product_data = {
                'id': product.get('Ref_Key'),
                'short_name': product.get('Description'),
                'description': product.get('Комментарий'),
                'price': fix_price.get('Цена'),
                'old_price': fix_price.get('Цена')
            }

        return product_data
            
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

@app.route('/api/updates', methods=['GET'])
def get_updates():
    pass

@app.route('/api/company-info', methods=['GET'])
def get_company_info():
    try:
        company_info = {
            'company': {},
            'filials': []
        }

        response_companies = send_request('Catalog_Организации', "PredefinedDataName eq 'ОсновнаяОрганизация'")

        response_filials = send_request('Catalog_СтруктурныеЕдиницы', "ТипСтруктурнойЕдиницы eq 'МагазинГруппаСкладов'")

        company = response_companies.json().get('value')[0]
        filials = response_filials.json().get('value')

        company_info['company'] = {
            'id': company.get('Ref_Key'),
            'name': company.get('НаименованиеСокращенное')
        }

        for filial in filials:
            company_info['filials'].append({
                'id': filial.get('Ref_Key'),
                'name': filial.get('Description')
            })


        return company_info
            
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