from PyQt5.QtGui import QStandardItemModel, QStandardItem


class GenericSheetModel(QStandardItemModel):
    def __init__(self):
        super(GenericSheetModel, self).__init__()

        self.values = []
        self.headers = []

    def get_sku(self, item):
        return self.item(item.row(), 0).text()

    def load_sheet(self, sheet, headers):
        self.values = sheet
        self.headers = headers
        self.clear()
        self.setHorizontalHeaderLabels(self.headers)
        for row in self.values:
            item = [QStandardItem(str(val)) for val in row]
            self.appendRow(item)


def format_text(self, case):
    if case == 'upper':
        for index in self.invTV.selectionModel().selectedIndexes():
            text = self.sheetModel.itemFromIndex(index).text().upper()
            self.sheetModel.setData(index, text)
    if case == 'title':
        for index in self.invTV.selectionModel().selectedIndexes():
            text = self.sheetModel.itemFromIndex(index).text().title()
            self.sheetModel.setData(index, text)
    if case == 'lower':
        for index in self.invTV.selectionModel().selectedIndexes():
            text = self.sheetModel.itemFromIndex(index).text().lower()
            self.sheetModel.setData(index, text)


def cut_cell(self):
    index = self.invTV.selectionModel().selectedIndexes()[0]
    text = self.sheetModel.itemFromIndex(index).text()
    self.clipboard.setText(text)
    self.sheetModel.setData(index, '')

    return


def copy_cell(self):
    text = self.sheetModel.itemFromIndex(self.invTV.selectionModel().selectedIndexes()[0]).text()
    self.clipboard.setText(text)

    return


def paste_cell(self):
    for index in self.invTV.selectionModel().selectedIndexes():
        text = self.clipboard.text()
        self.sheetModel.setData(index, text)

    return


def filter_action(self):
    for row in range(self.sheetModel.rowCount()):
        self.invTV.setRowHidden(row, False)

    keyword = self.filterLE.text()

    if not keyword:
        return

    for row in range(self.sheetModel.rowCount()):
        show = False
        for cell in range(self.sheetModel.columnCount()):
            data = str(self.sheetModel.item(row, cell).text()).lower()
            if keyword.lower() in data:
                show = True
        if show == False:
            self.invTV.setRowHidden(row, True)

    self.invTV.resizeColumnsToContents()
    return
