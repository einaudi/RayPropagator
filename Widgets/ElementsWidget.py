from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QCheckBox

from RayPropagation.RayPropagation import Lens


class OpticalElementsWidget(QWidget):
    
    def __init__(self):

        super().__init__()

        self._id = 0

        self._init_widgets()
        self._init_layout()
        self._init_UI()

    def _init_widgets(self):

        self.elementsTable = QTableWidget(0, 5)
        self.elementsTable.setHorizontalHeaderLabels([
            '',
            'Lens',
            'Focal length [mm]',
            'Position [mm]',
            'Aperture [mm]'
        ])
        self.elementsTable.setColumnWidth(0, 15)

        self.btnAdd = QPushButton('Add lens')
        self.btnRemove = QPushButton('Remove lens')

    def _init_layout(self):

        btnBox = QHBoxLayout()
        btnBox.addWidget(self.btnAdd, 1)
        btnBox.addWidget(self.btnRemove, 1)

        mainBox = QVBoxLayout()
        mainBox.addWidget(self.elementsTable)
        mainBox.addLayout(btnBox)

        self.setLayout(mainBox)

    def _init_UI(self):

        self.btnAdd.clicked.connect(self._add_lens)
        self.btnRemove.clicked.connect(self._remove_lens)

    def _add_lens(self):

        rowCount = self.elementsTable.rowCount()
        name = 'L{0}'.format(self._id)
        self._id += 1

        self.elementsTable.insertRow(rowCount)

        self.elementsTable.setCellWidget(
            rowCount,
            0,
            QCheckBox()
        )
        self.elementsTable.cellWidget(rowCount, 0).setChecked(True)

        self.elementsTable.setItem(
            rowCount,
            1,
            QTableWidgetItem()
        )
        self.elementsTable.item(rowCount, 1).setText(name)

        self.elementsTable.setItem(
            rowCount,
            2,
            QTableWidgetItem()
        )
        self.elementsTable.item(rowCount, 2).setText('50')

        self.elementsTable.setItem(
            rowCount,
            3,
            QTableWidgetItem()
        )
        self.elementsTable.item(rowCount, 3).setText('10')

        self.elementsTable.setItem(
            rowCount,
            4,
            QTableWidgetItem()
        )
        self.elementsTable.item(rowCount, 4).setText('25.4')

    def _remove_lens(self):

        if self.elementsTable.rowCount() > 0 and self.elementsTable.selectionModel().hasSelection():
            self.elementsTable.removeRow(self.elementsTable.currentRow())

    def get_lenses(self):

        rowCount = self.elementsTable.rowCount()

        ret = []
        try:
            for i in range(rowCount):
                if self.elementsTable.cellWidget(i, 0).isChecked():
                    name = self.elementsTable.item(i, 1).text()
                    f = float(self.elementsTable.item(i, 2).text()) * 1e-3
                    pos = float(self.elementsTable.item(i, 3).text()) * 1e-3
                    aperture = float(self.elementsTable.item(i, 4).text()) * 1e-3

                    ret.append(
                        Lens(name, f, pos, aperture)
                    )
        except ValueError:
            return []

        return ret