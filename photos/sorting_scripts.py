import os
import re
import shutil

from PIL import Image
from PyQt5.QtWidgets import QApplication, QFileDialog
from pyzbar.pyzbar import decode, ZBarSymbol


def find_sku_barcode(file):
    form = re.compile(r"\D{2}\d{4}")

    sku = None
    im = Image.open(file)
    results = decode(im, symbols=[ZBarSymbol.CODE39, ZBarSymbol.CODE128])
    if results:
        if form.match(results[0].data.decode()):
            sku = results[0].data.decode()
        else:
            sku = None
    else:
        sku = None

    return sku

def manual_sort(dest_dir, file_names):

    sku = input("Enter SKU: ").upper()

    try:
        os.mkdir(dest_dir+sku)
    except:
        pass

    for file in file_names:
        try:
            shutil.move(file, dest_dir + sku + "/" + file.split('/')[-1])
        except:
            pass

    return

def basic_auto_sort(dest_dir, file_names):
    match = False
    for file in reversed(file_names):
        sku = find_sku_barcode(file)
        if sku:
            match = True
            break
    if match == False:
        sku = input("Barcode not found. Enter SKU: ")

    try:
        print(sku.upper())
        try:
            os.mkdir(dest_dir + sku.upper())
        except Exception as e:
            print(e)
            pass
        for file in file_names:
            shutil.move(file, dest_dir + sku.upper() + "/" + file.split('/')[-1])
    except Exception as e:
        print(e)
        pass

    return


def bulk_auto_sort(dest_dir, file_names):
    skus = {}
    current_sku = 'NO_SKU'
    skus[current_sku] = []

    for i, file in enumerate(reversed(file_names)):
        print("Images Processed: ", str(i + 1) + "/" + str(len(file_names)))
        sku = find_sku_barcode(file)
        if sku:
            current_sku = sku
            if sku not in skus.keys():
                skus[sku] = []
            if sku in skus.keys():
                pass
        skus[current_sku].append(file)

    for sku in skus.keys():
        try:
            os.mkdir(dest_dir + sku.upper())
        except:
            pass
        for file in skus[sku]:
            try:
                shutil.move(file, dest_dir + current_sku.upper() + "/" + file.split('/')[-1])
            except:
                continue

    print("\nSKUs Found: ", len(skus.keys()))
    print("Total Images: ", len(file_names))
    print("")
    for sku in skus.keys():
        print("SKU:", sku, "Images:", len(skus[sku]))

    return


def photo_pick_dialogs():
    app = QApplication([])
    source_dir = QFileDialog.getExistingDirectory(None, "Select Unsorted Folder") + '/'
    dest_dir = QFileDialog.getExistingDirectory(None, "Select To Be Listed Folder") + '/'
    file_names, _ = QFileDialog.getOpenFileNames(directory=source_dir)
    if file_names == []:
        return

    return source_dir, dest_dir, file_names
