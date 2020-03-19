import imghdr

import requests.exceptions
from requests_toolbelt.multipart.encoder import MultipartEncoder

categories = {
    'Airboats': '25',
    'Engines': '22',
    'Hulls': '24',
    'Other': '26',
    'Parts': '23',
    'Aircraft for Sale': '1',
    'Amphibian': '16',
    'Helicopters': '17',
    'Projects': '12',
    'Singles': '18',
    'Twins': '19',
    'Aerobatic': '28',
    'Aeronca': '27',
    'Antique': '30',
    'Beechcraft': '31',
    'Bellanca': '32',
    'Cessna': '33',
    'Cirrus': '34',
    'Control Surfaces': '35',
    'General Parts': '117',
    'Helicopter': '37',
    'Interior': '38',
    'Luscombe': '39',
    'Mooney': '40',
    'Piper': '41',
    'Taylorcraft': '42',
    'Warbird': '43',
    'Antennas': '45',
    'Audio Panels': '46',
    'AutoPilot': '47',
    'ELTs': '48',
    'Engine Monitors': '49',
    'GPS': '50',
    'Indicators': '51',
    'Intercom': '52',
    'Nav/Coms': '53',
    'Packages': '54',
    'Pitot Tubes': '55',
    'Transponders': '56',
    'Trays & Connectors': '57',
    'Weather Systems': '58',
    'Batteries': '60',
    'Lighting': '61',
    'Jacks': '63',
    'Nuts & Bolts': '64',
    'Rivets': '65',
    'Testing Equipment': '67',
    'Tools': '66',
    'Skis': '70',
    'Tailwheel': '71',
    'Tires & Tubes': '72',
    'Wheels & Brakes': '73',
    'Aviator Accessories': '74',
    'Bags': '75',
    'Books': '76',
    'Collectibles': '77',
    'Cover & Accessories': '78',
    'Headsets': '79',
    'Manuals': '80',
    'Oils, Liquids, & Sprays': '81',
    'Pilot Wear': '82',
    'Safety': '83',
    'Stickers & Decals': '84',
    'Tow': '85',
    'Engine Parts': '88',
    'Environmental': '118',
    'Exhaust': '89',
    'Fuel System': '90',
    'Propellers': '91'
}

def get_hs_session(username, password):
    payload = {}
    payload['Username'] = username
    payload['Password'] = password

    session = requests.Session()

    session.post('https://www.hangarswap.com/Main/ProcessLogin', data=payload, verify=False, allow_redirects=False)

    return session

def add_product(product, session, primary_photo=None):

    item_form = {
        'productName': product['title'],
        'productDescription': product['desc'],
        'CategoryID': product['cat'],
        'productCondition': product['cond'],
        'Qty': product['qty'],
        'PartNumber': product['pn'],
        'APN': product['apn'],
        'SerialNumber': product['sn'],
        'SKU': product['sku'],
        'Manufacturer': product['mfg'],
        'Price': product['price'],
        'ShippingCost': product['ship'],
        'HasCore': '0',
        'CoreCharge': '0.00',
        'Active': '1',
        'OnSale': '0',
        'AllowBestOffer': '1',
        'Featured': '0',
    }

    if primary_photo:
        item_form['productImage'] = (
            'filename', open(primary_photo, 'rb'),
            ('image/' + str(imghdr.what(primary_photo))))

    product_data = MultipartEncoder(fields=item_form, boundary='-----WebKitFormBoundarymkISNjkugjjFZdvE')
    session.post('https://www.hangarswap.com/Seller/SaveProduct', data=product_data,
           headers={'Content-Type': product_data.content_type})

    return

def upload_photos(product_id, file_names, session):

    for i, photo_path in enumerate(file_names):
        print("ID:", product_id, "File:", i, "of", len(file_names))

        photo_form = MultipartEncoder(
            fields={
                'productid': str(product_id),
                'ProductImage': (
                    'filename', open(photo_path, 'rb'),
                    ('image/' + str(imghdr.what(photo_path)))),
            }, boundary='-----WebKitFormBoundarydMG06kgczAncwn4B')

        session.post('https://www.hangarswap.com/Seller/SaveExtraImages', data=photo_form,
                     headers={'Content-Type': photo_form.content_type}, verify=False)

    return