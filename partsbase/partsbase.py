import csv
from datetime import datetime

from inv_sheets.inv_list_scripts import authorize_sheets, get_all_sheets_records


def download_inventory(url, creds):
    workbook = authorize_sheets(url, creds)

    print("\nDownloading inventory sheets...")
    sheet_data = get_all_sheets_records(workbook)

    master_sheet = []

    print("\nCreating master sheet...")

    for sheet in sheet_data:
        for item in sheet:
            master_sheet.append(item)

    return master_sheet


def clean_skus(sheet):
    clean_sheet = []

    for item in sheet:
        if item['SKU'] != '':
            if 'FL' not in item['SKU'] and 'BB' not in item['SKU']:
                clean_sheet.append(item)

    return clean_sheet


def clean_desc(sheet):
    clean_sheet = []
    for item in sheet:
        if item['DESC'] != '':
            item['DESC'] = item['DESC'].upper()
            clean_sheet.append(item)

    return clean_sheet


def clean_pn(sheet):
    clean_sheet = []
    for item in sheet:
        if item['PN'] != '':
            item['PN'] = str(item['PN']).upper()
            clean_sheet.append(item)

    return clean_sheet


def clean_cc(sheet):
    clean_sheet = []
    for item in sheet:
        if item['CC'] == '':
            item['CC'] = 'AR'
        item['CC'] = item['CC'].strip()
        if item['CC'].upper() == 'CORE':
            item['CC'] = 'CR'
        if item['CC'].upper() == 'NOS':
            item['CC'] = 'NS'
        if item['CC'].upper() == 'NEW':
            item['CC'] = 'NE'
        if len(item['CC']) > 2:
            print("\nSKU: " + item['SKU'] + " CC: " + item['CC'])
            new_cc = input("Condition Code must be 2 letters. Enter new code: ")
            if new_cc == '':
                new_cc = 'AR'
            item['CC'] = new_cc.upper()

        clean_sheet.append(item)

    return clean_sheet


def clean_qty(sheet):
    clean_sheet = []

    for item in sheet:
        if item['QTY'] != '':
            if str(item['QTY']) == '0':
                continue
            if not str(item['QTY']).isdecimal():
                print("\nSKU:", item['SKU'], "QTY:", item['QTY'])
                qty = int(input("Quantity invalid. Enter single number: "))
                item['QTY'] = qty
            clean_sheet.append(item)

    return clean_sheet


def parse_inventory(master_sheet):
    print("\nParsing master file...")
    headers = ['PartNumber', 'AlternatePartNumber', 'ConditionCode', 'Quantity', 'Description']

    parsed_sheet = []
    for item in master_sheet:
        try:
            new_item = {'SKU': item['SKU'],
                        'PN': item['PN'],
                        'APN': item['Alt PN'],
                        'CC': item['Cond'],
                        'QTY': item['Quan'],
                        'DESC': item['Description']}
        except KeyError:
            print(item)
            continue
        parsed_sheet.append(new_item)

    print("\nCurrent Sheet Length:", len(parsed_sheet), "rows")
    print("Cleaning bad SKUs...")
    parsed_sheet = clean_skus(parsed_sheet)
    print("\nCurrent Sheet Length:", len(parsed_sheet), "rows")
    print("Cleaning bad descriptions...")
    parsed_sheet = clean_desc(parsed_sheet)
    print("\nCurrent Sheet Length:", len(parsed_sheet), "rows")
    print("Cleaning bad part numbers...")
    parsed_sheet = clean_pn(parsed_sheet)
    print("\nCurrent Sheet Length:", len(parsed_sheet), "rows")
    print("Cleaning bad quantities...")
    parsed_sheet = clean_qty(parsed_sheet)
    print("\nCurrent Sheet Length:", len(parsed_sheet), "rows")
    print("Cleaning bad condition codes...")
    parsed_sheet = clean_cc(parsed_sheet)

    final_sheet = []
    final_sheet.append(headers)
    for item in parsed_sheet:
        final_sheet.append([item['PN'], item['APN'], item['CC'], item['QTY'], item['DESC'][:40] + ' - ' + item['SKU']])

    print("\nFinal Sheet Length:", len(parsed_sheet) - 1, "rows")

    return final_sheet


def save_sheet_file(sheet):
    file_name = 'PartsbaseInventory-' + datetime.today().strftime("%Y-%m-%d") + ".csv"

    print("\nSaving sheet to", file_name)

    with open(file_name, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(sheet)

    return


if __name__ == '__main__':
    master_sheet = download_inventory(inv_sheet_url, google_credentials)
    clean_sheet = parse_inventory(master_sheet)
    save_sheet_file(clean_sheet)

    print("Done.")
