from flask import Flask, jsonify, request
import requests
import os
from dotenv import load_dotenv
import base64
import threading
from datetime import datetime
import time
import json

app = Flask(__name__)

load_dotenv()

ONEC_URL = os.getenv('ONEC_URL', '')
ONEC_LOGIN = os.getenv('ONEC_LOGIN', '')
ONEC_PASSWORD = os.getenv('ONEC_PASSWORD', '')

@staticmethod
def get_main_server_url():
    return 'http://127.0.0.1:8000'

@staticmethod
def send_request(url, filter=None):
    if filter is not None:
        response = requests.get(
            f"{ONEC_URL}/odata/standard.odata/{url}?$format=json&{filter.replace(' ', '%20').replace("'", "'")}",
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

@staticmethod
def get_product_image(image_id):
    response = requests.get(
        f"{ONEC_URL}/odata/standard.odata/Catalog_НоменклатураПрисоединенныеФайлы(guid'1387e11e-13b7-11f1-937e-14133384446c')/ФайлХранилище",
        auth=(ONEC_LOGIN, ONEC_PASSWORD),
        timeout=30
    )

    data = response

    # file_content = base64.b64decode(response['value'])
    print(data)

    return response

@staticmethod
def get_updates_by_responses(response_prices_updates, response_promotions, response_ends_promotions, response_products_updates):
    response_products = send_request("Catalog_Номенклатура")
        
    products = response_products.json().get('value')
    prices_updates = response_prices_updates.json().get('value')
    actual_promotions = response_promotions.json().get('value')
    ends_promotions = [] if response_ends_promotions == [] else response_ends_promotions.json().get('value')
    products_updates = response_products_updates.json().get('value')

    updates = []

    for item in prices_updates:
        if next((a for a in updates if a['id'] == item['Номенклатура']['Ref_Key']), None) is None:            
            updates.append({
                "id": item['Номенклатура']['Ref_Key'],
                "price": float(item['Цена'])
            })

    for product in products_updates:
        update_num = next((i for i, obj in enumerate(updates) if obj['id'] == product['Ref_Key']), None)
        if update_num is not None:
            updates[update_num]['short_name'] = product['Description']
        else:
            prices = send_request("InformationRegister_ЦеныНоменклатуры", f"$filter=Номенклатура_Key eq guid'{product['Ref_Key']}'").json().get('value')
            price = prices[len(prices) - 1]

            updates.append({
                "id": product['Ref_Key'],
                "short_name": product['Description'],
                "price": float(price['Цена'])
            })
    
    actual_promotions_list = []
    for promotion in actual_promotions:
        for item in promotion['НоменклатураГруппыЦеновыеГруппы']:
            actual_promotions_list.append(item)

    ends_promotions_list = []
    for promotion in ends_promotions:
        for item in promotion['НоменклатураГруппыЦеновыеГруппы']:
            ends_promotions_list.append(item)

    for promotion in actual_promotions_list:
        if promotion['ЗначениеУточнения_Type'] == 'StandardODATA.Catalog_Номенклатура':
            update_num = next((i for i, obj in enumerate(updates) if obj['id'] == promotion['ЗначениеУточнения']), None)
            if update_num is not None:
                updates[update_num]['have_promotion'] = True
                updates[update_num]['promotion'] = promotion['ЗначениеСкидкиНаценки']

            else:
                updates.append({
                    "id": promotion['ЗначениеУточнения'],
                    "have_promotion": True,
                    "promotion": promotion['ЗначениеСкидкиНаценки']
                })

        elif promotion['ЗначениеУточнения_Type'] == 'StandardODATA.Catalog_КатегорииНоменклатуры':
            promotion_products = [product for product in products if product['КатегорияНоменклатуры_Key'] == promotion['ЗначениеУточнения']]

            for product in promotion_products:
                update_num = next((i for i, obj in enumerate(updates) if obj['id'] == product['Ref_Key']), None)
                if update_num is not None:
                    updates[update_num]['have_promotion'] = True
                    updates[update_num]['promotion'] = promotion['ЗначениеСкидкиНаценки']

                else:
                    updates.append({
                        "id": product['Ref_Key'],
                        "have_promotion": True,
                        "promotion": promotion['ЗначениеСкидкиНаценки']
                    })

    for promotion in ends_promotions_list:
        if promotion['ЗначениеУточнения_Type'] == 'StandardODATA.Catalog_Номенклатура':
            update_num = next((i for i, obj in enumerate(updates) if obj['id'] == promotion['ЗначениеУточнения']), None)
            if update_num is not None:
                updates[update_num]['have_promotion'] = False
                updates[update_num]['promotion'] = 0

            else:
                updates.append({
                    "id": promotion['ЗначениеУточнения'],
                    "have_promotion": False,
                    "promotion": 0
                })

        elif promotion['ЗначениеУточнения_Type'] == 'StandardODATA.Catalog_КатегорииНоменклатуры':
            promotion_products = [product for product in products if product['КатегорияНоменклатуры_Key'] == promotion['ЗначениеУточнения']]

            for product in promotion_products:
                update_num = next((i for i, obj in enumerate(updates) if obj['id'] == product['Ref_Key']), None)
                if update_num is not None:
                    updates[update_num]['have_promotion'] = False
                    updates[update_num]['promotion'] = 0

                else:
                    updates.append({
                        "id": product['Ref_Key'],
                        "have_promotion": False,
                        "promotion": 0
                    })

    return updates

def update_data_periodically():
    session = requests.Session()
    # Настройка сессии
    adapter = requests.adapters.HTTPAdapter(
        pool_connections=10,
        pool_maxsize=10,
        max_retries=3,
        pool_block=False
    )
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    while True:
        try:
            last_update = os.getenv('LAST_UPDATE', '')
            if last_update == '':
                os.environ['LAST_UPDATE'] = datetime.now().isoformat()
            
            else:
                response_prices_updates = send_request('InformationRegister_ЦеныНоменклатуры', f"$orderby=Period desc&$expand=Номенклатура&$filter=Period ge datetime'{last_update}'")
                response_promotions = send_request("Catalog_АвтоматическиеСкидки", f"$filter=((ДатаОкончания gt datetime'{datetime.now().isoformat()}' and ДатаНачала le datetime'{datetime.now().isoformat()}') and (Действует eq true) and (ЕстьУточненияПоКатегориям eq true or ЕстьУточненияПоНоменклатуре eq true)) and (ДатаНачала gt datetime'{last_update}')")
                response_ends_promotions = send_request("Catalog_АвтоматическиеСкидки", f"$filter=((ДатаОкончания gt datetime'{last_update}' and ДатаНачала lt datetime'{last_update}') and (ЕстьУточненияПоКатегориям eq true or ЕстьУточненияПоНоменклатуре eq true)) and (ДатаОкончания lt datetime'{datetime.now().isoformat()}')")
                response_products_updates = send_request("Catalog_Номенклатура", f"$filter=ДатаИзменения ge datetime'{last_update}'")

                updates = get_updates_by_responses(response_prices_updates, response_promotions, response_ends_promotions, response_products_updates)
                os.environ['LAST_UPDATE'] = datetime.now().isoformat()

                if len(updates) > 0:                            
                    print(updates)
                    # data = json.loads({'updates': updates})
                    response = session.post(
                        f"{get_main_server_url()}/api/product/update/",
                        json={'updates': updates},
                        headers={'Content-Type': 'application/json'},
                    )

                    print(response.status_code)

        except requests.exceptions.RequestException as e:
            print(e)
        except Exception as e:
            print(e)
        
        time.sleep(5)

def start_background_updater():
    thread = threading.Thread(target=update_data_periodically, daemon=True)
    thread.start()


@app.route('/api/product/', methods=['GET'])
def get_products_list():
    try:
        response_products = send_request("Catalog_Номенклатура")
        
        products = response_products.json().get('value')

        products_data = []
        for product in products:
            products_data.append({
                'id': product.get('Ref_Key'),
                'short_name': product.get('Description'),
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

@app.route('/api/product/<id>/', methods=['GET'])
def get_product_info(id):
    try:
        response_product = send_request(f"Catalog_Номенклатура(guid'{id}')")

        response_prices = send_request('InformationRegister_ЦеныНоменклатуры', f"$filter=Номенклатура_Key eq guid'{id}'")

        response_promotions = send_request("Catalog_АвтоматическиеСкидки", f"$filter=(ДатаОкончания gt datetime'{datetime.now().isoformat()}' and ДатаНачала le datetime'{datetime.now().isoformat()}') and (Действует eq true) and (ЕстьУточненияПоКатегориям eq true or ЕстьУточненияПоНоменклатуре eq true)")
        
        product = response_product.json()

        prices = response_prices.json().get('value')
        price = prices[len(prices) - 1]

        actual_promotions = response_promotions.json().get('value')

        promotion = None

        if len(actual_promotions) > 0:
            promotions = []

            for promotion in actual_promotions:
                for item in promotion['НоменклатураГруппыЦеновыеГруппы']:
                    promotions.append(item)

            promotion = next((item for item in promotions
                if(
                    (item['ЗначениеУточнения'] == product.get('Ref_Key') 
                    and item['ЗначениеУточнения_Type'] == 'StandardODATA.Catalog_Номенклатура') 
                    or (item['ЗначениеУточнения'] == product.get('КатегорияНоменклатуры_Key') 
                        and item['ЗначениеУточнения_Type'] == 'StandardODATA.Catalog_КатегорииНоменклатуры')
                    )
                ), None)
        
        # response_image = get_product_image(product['ФайлКартинки_Key'])

        # print(response_image.content)

        product_data = {
            'id': product.get('Ref_Key'),
            'short_name': product.get('Description'),
            'description': product.get('Комментарий'),
            'price': price.get('Цена')
        }

        if promotion is not None:
            product_data['have_promotion'] = True
            product_data['promotion'] = promotion['ЗначениеСкидкиНаценки']
        else:
            product_data['have_promotion'] = False
            product_data['promotion'] = 0

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

@app.route('/api/updates/', methods=['GET'])
def get_updates():
    try:
        is_first_update = request.args.get('is_first_update', default=False, type=bool) 
        last_update = os.getenv('LAST_FORCE_UPDATE', '')
        if is_first_update or last_update == '':
            response_prices_updates = send_request('InformationRegister_ЦеныНоменклатуры', f"$orderby=Period desc&$expand=Номенклатура")
            response_promotions = send_request("Catalog_АвтоматическиеСкидки", f"$filter=(ДатаОкончания gt datetime'{datetime.now().isoformat()}' and ДатаНачала le datetime'{datetime.now().isoformat()}') and (Действует eq true) and (ЕстьУточненияПоКатегориям eq true or ЕстьУточненияПоНоменклатуре eq true)")
            response_ends_promotions = []        
            response_products_updates = send_request("Catalog_Номенклатура")
        else:
            response_prices_updates = send_request('InformationRegister_ЦеныНоменклатуры', f"$orderby=Period desc&$expand=Номенклатура&$filter=Period ge datetime'{last_update}'")
            response_promotions = send_request("Catalog_АвтоматическиеСкидки", f"$filter=((ДатаОкончания gt datetime'{datetime.now().isoformat()}' and ДатаНачала le datetime'{datetime.now().isoformat()}') and (Действует eq true) and (ЕстьУточненияПоКатегориям eq true or ЕстьУточненияПоНоменклатуре eq true)) and (ДатаНачала gt datetime'{last_update}')")
            response_ends_promotions = send_request("Catalog_АвтоматическиеСкидки", f"$filter=((ДатаОкончания gt datetime'{last_update}' and ДатаНачала lt datetime'{last_update}') and (ЕстьУточненияПоКатегориям eq true or ЕстьУточненияПоНоменклатуре eq true)) and (ДатаОкончания lt datetime'{datetime.now().isoformat()}')")
            response_products_updates = send_request("Catalog_Номенклатура", f"$filter=ДатаИзменения ge datetime'{last_update}'")

        updates = get_updates_by_responses(response_prices_updates, response_promotions, response_ends_promotions, response_products_updates)
            
        os.environ['LAST_FORCE_UPDATE'] = datetime.now().isoformat()

        return updates

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

@app.route('/api/company-info/', methods=['GET'])
def get_company_info():
    try:
        company_info = {
            'company': {},
            'filials': []
        }

        response_companies = send_request('Catalog_Организации', "$filter=PredefinedDataName eq 'ОсновнаяОрганизация'")

        response_filials = send_request('Catalog_СтруктурныеЕдиницы', "$filter=ТипСтруктурнойЕдиницы eq 'МагазинГруппаСкладов'")

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
    
@app.route('/api/filial/<id>/', methods=['GET'])
def get_filial_info(id):
    try:
        response_filial = send_request(f"Catalog_СтруктурныеЕдиницы(guid'{id}')")

        filial = response_filial.json()

        filial_info = {
            'id': filial.get('Ref_Key'),
            'name': filial.get('Description')
        }


        return filial_info
            
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
    
# @app.route('/api/config/', methods=['PUT'])
# def update_config():


if __name__ == '__main__':
    start_background_updater()

    app.run(host='0.0.0.0', port=5000, debug=False)