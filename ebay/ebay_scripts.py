from ebaysdk.trading import Connection as Trading
import ntpath

def get_no_photo_listings(api, today, end):

    total_pages = get_seller_list_pages(api, today, end)

    item_list = []

    for i in range(1, total_pages+1):

        api.execute('GetSellerList', {'EndTimeFrom': today, 'EndTimeTo': end, 'GranularityLevel': 'Coarse',
                                      'outputSelector': ['ItemArray.Item.SKU', 'ItemArray.Item.ItemID',
                                                         'ItemArray.Item.PictureDetails',
                                                         'ItemArray.Item.SellingStatus.ListingStatus'],
                                      'Pagination': {'EntriesPerPage': '200', 'PageNumber': str(i)}})

        for product in api.response.dict()['ItemArray']['Item']:
            if product['SellingStatus']['ListingStatus'] == 'Active':
                item_list.append(product)

    good_items = []
    bad_items = []

    for item in item_list:
        try:
            listing = [item['ItemID'], item['SellingStatus']['ListingStatus'], item['SKU'],
                       len(item['PictureDetails']['PictureURL'])]
            good_items.append(listing)
        except KeyError:
            bad_items.append(item)

    return good_items, bad_items

def auth_ebay_api(ebay_token, ebay_appid, ebay_devid, ebay_certid):
    api = Trading(config_file=None, certid=ebay_certid, devid=ebay_devid, appid=ebay_appid, token=ebay_token,
                  debug=False)

    return api

def get_seller_list_pages(api, today, end):
    api.execute('GetSellerList', {'EndTimeFrom': today, 'EndTimeTo': end, 'GranularityLevel': 'Coarse',
                                  'OutputSelector': 'PaginationResult.TotalNumberOfPages',
                                  'Pagination': {'EntriesPerPage': '200'}})

    total_pages = int(api.response.dict()['PaginationResult']['TotalNumberOfPages'])

    return total_pages

def get_seller_list(api, today, end):

    total_pages = get_seller_list_pages(api, today, end)

    seller_list = []

    for page in range(1, total_pages + 1):
        print('Getting page: ', page)
        api.execute('GetSellerList', {'EndTimeFrom': today, 'EndTimeTo': end,
                                      'outputSelector': ['ItemArray.Item.SKU', 'ItemArray.Item.ID'],
                                      'Pagination': {'EntriesPerPage': '200', 'PageNumber': page},
                                      'GranularityLevel': 'Coarse'})

        for item in api.response.dict()['ItemArray']['Item']:
            try:
                seller_list.append([item['SKU'], item['ItemID']])
            except:
                pass

        return seller_list


def create_item(api, title, description, price, cond, cond_desc, ship, brand, mpn, sku):
    myitem = {
        "Item": {
            "Title": title,
            "Description": "<![CDATA[" + description + "]]>",
            "PrimaryCategory": {"CategoryID": "26439"},
            "StartPrice": price,
            "CategoryMappingAllowed": "true",
            "Country": "US",
            "BestOfferDetails": {"BestOfferEnabled": "true"},
            "ConditionID": cond,
            "ConditionDescription": cond_desc,
            "Currency": "USD",
            "DispatchTimeMax": "3",
            "ListingDuration": "GTC",
            "ListingType": "FixedPriceItem",
            "PaymentMethods": "PayPal",
            "PayPalEmailAddress": "",
            "PostalCode": "",
            "Quantity": "1",
            "ReturnPolicy": {
                "ReturnsAcceptedOption": "ReturnsAccepted",
                "RefundOption": "MoneyBack",
                "ReturnsWithinOption": "Days_30",
                # "Description": "Items must be returned in exact condition purchased. Returns may not be accepted for purchasing incorrect items. Not repairs, alterations, damage or modifications to the part will be accepted for return.",
                "ShippingCostPaidByOption": "Buyer"
            },
            "ShippingDetails": {
                "ShippingType": "Flat",
                "GlobalShipping": "true",
                "ShippingServiceOptions": {
                    "ShippingServicePriority": "1",
                    "ShippingService": "ShippingMethodStandard",
                    "ShippingServiceCost": ship
                },
            },
            "ItemSpecifics": {"NameValueList": [{"Name": "Brand", "Value": brand},
                                                {"Name": "Manufacturer Part Number", "Value": mpn}]},
            "SKU": sku,
            "Site": "US"
        }
    }

    return api.execute('AddItem', myitem)


def upload_photos(api, id, file_names):
    pic_urls = []

    for file_name in file_names[:11]:
        files = {'file': ('EbayImage', open(file_name, 'rb'))}

        picture_data = {
            "WarningLevel": "High",
            "PictureName": ntpath.basename(file_name).split('.')[0]
        }

        api.execute('UploadSiteHostedPictures', picture_data, files=files)

        url = api.response.dict()['SiteHostedPictureDetails']['FullURL']
        pic_urls.append(url)

    item = {
        "Item": {
            "ItemID": id,
            "PictureDetails": {"PictureURL": pic_urls}
        }
    }

    return api.execute('ReviseFixedPriceItem', item)
