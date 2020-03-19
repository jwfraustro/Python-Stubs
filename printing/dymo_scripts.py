from win32com.client import Dispatch

def print_sku_barcode_label(printer, loc, sku, notes):

    isOpen = labelCom.Open('./SKU2.label')

    loc = "LOC: " + loc.upper()
    sku = sku.upper()

    labelText.SetField('SKU', sku)
    labelText.SetField('LOC', loc)
    labelText.SetField('TEXT', notes)
    labelCom.StartPrintJob()
    labelCom.Print(1, True)
    labelCom.EndPrintJob()

    return

def print_barcodes(printer, loc):

    loc = loc.upper()

    isOpen = labelCom.Open('./shelf_label.label')
    labelText.SetField('BARCODE', loc)
    labelCom.StartPrintJob()
    labelCom.Print(1, True)
    labelCom.EndPrintJob()

    return


def connect_to_printer(printer_name):

    labelCom = Dispatch('Dymo.DymoAddIn')
    labelText = Dispatch('Dymo.DymoLabels')
    selectPrinter = printer_name
    labelCom.SelectPrinter(selectPrinter)

    ### With PyQt5 #####
    #app = QApplication([])
    # dialog = QtPrintSupport.QPrintDialog()
    # if dialog.exec_() == QDialog.Accepted:
    #     printer = dialog.printer()
    #     labelCom = Dispatch('Dymo.DymoAddIn')
    #     labelText = Dispatch('Dymo.DymoLabels')
    #     isOpen = labelCom.Open('./SKU2.label')
    #     selectPrinter = printer.printerName()
    #     labelCom.SelectPrinter(selectPrinter)

    return

