import gspread, re
from oauth2client.service_account import ServiceAccountCredentials
import time

def authorize_sheets(url, creds):
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']

    # creds = {
    #     "type": "",
    #     "project_id": "",
    #     "private_key_id": "",
    #     "private_key": "",
    #     "client_email": "",
    #     "client_id": "",
    #     "auth_uri": "",
    #     "token_uri": "",
    #     "auth_provider_x509_cert_url": "",
    #     "client_x509_cert_url": ""
    # }

    credentials = ServiceAccountCredentials.from_json_keyfile_dict(creds, scope)
    gc = gspread.authorize(credentials)
    workbook = gc.open_by_url(url)

    return workbook


def get_sheet_list(workbook):
    form = re.compile(r"^.{2,3}$")

    sheet_list = []

    for sheet in workbook.worksheets():
        if form.match(sheet.title):
            sheet_list.append(sheet.title)

    return sheet_list


def get_sheet(workbook, sheet):
    sheet_data = workbook.worksheet(sheet).get_all_values()
    headers = sheet_data.pop(0)

    return headers, sheet_data


def get_sheet_records(workbook, sheet):
    sheet_data = workbook.worksheet(sheet).get_all_records()
    return sheet_data


def get_all_sheets_records(workbook):
    sheet_list = get_sheet_list(workbook)

    all_sheet_data = []

    for sheet in sheet_list:
        print("Downloading:", sheet)
        sheet_data = get_sheet_records(workbook, sheet)
        all_sheet_data.append(sheet_data)
        time.sleep(1)

    return all_sheet_data


def get_all_sheets(workbook):
    sheet_list = get_sheet_list(workbook)

    all_sheet_data = []
    all_sheet_headers = []

    for sheet in sheet_list:
        headers, sheet_data = get_sheet(workbook, sheet)
        all_sheet_headers.append(headers)
        all_sheet_data.append(sheet_data)

    return all_sheet_headers, all_sheet_data


def edit_sku(workbook, sheet, sku, col, value):
    sheet = workbook.worksheet(sheet)
    cell = sheet.find(sku)
    sheet.update_cell(cell.row, int(col), value)

    return
