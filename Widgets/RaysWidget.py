from PyQt5.QtWidgets import QWidget, QLineEdit, QFormLayout, QLabel, QHBoxLayout, QVBoxLayout, QDialog, QDialogButtonBox, QPushButton, QTableWidget, QTableWidgetItem

from RayPropagation.RayPropagation import Rays, Ray

import numpy as np


class RaysWidget(QWidget):
    
    def __init__(self):

        super().__init__()

        self._init_widgets()
        self._init_layout()
        self._init_UI()

    def _init_widgets(self):

        self.xRangeEdit = QLineEdit()
        self.xRangeEdit.setText('200')

        self.yRangeEdit = QLineEdit()
        self.yRangeEdit.setText('20')

        self.addBtn = QPushButton('Add ray')
        self.addPointSourceBtn = QPushButton('Add point source')
        self.removeBtn = QPushButton('Remove ray')

        self.raysTable = QTableWidget(0, 3)
        self.raysTable.setHorizontalHeaderLabels([
            'r [mm]',
            '{} [rad]'.format(u'\u03B8'),
            'Color'
        ])

    def _init_layout(self):

        form = QFormLayout()
        form.addRow(QLabel('X range [mm]:'), self.xRangeEdit)
        form.addRow(QLabel('Y range [mm]:'), self.yRangeEdit)

        btnsBox = QHBoxLayout()
        btnsBox.addWidget(self.addBtn)
        btnsBox.addWidget(self.addPointSourceBtn)
        btnsBox.addWidget(self.removeBtn)

        mainLayout = QVBoxLayout()
        mainLayout.addLayout(form)
        mainLayout.addWidget(self.raysTable)
        mainLayout.addLayout(btnsBox)

        self.setLayout(mainLayout)

    def _init_UI(self):

        self.addBtn.clicked.connect(self._add_ray_dialog)
        self.addPointSourceBtn.clicked.connect(self._add_point_source_dialog)
        self.removeBtn.clicked.connect(self._remove_ray)

    def get_geometry_properties(self):

        ret = {}

        ret['X range'] = float(self.xRangeEdit.text()) * 1e-3
        ret['Y range'] = float(self.yRangeEdit.text()) * 1e-3

        return ret

    def add_ray_row(self, rayParams):

        rowCount = self.raysTable.rowCount()
        self.raysTable.insertRow(rowCount)

        self.raysTable.setItem(
            rowCount,
            0,
            QTableWidgetItem()
        )
        self.raysTable.item(rowCount, 0).setText('{}'.format(rayParams['r']))

        self.raysTable.setItem(
            rowCount,
            1,
            QTableWidgetItem()
        )
        self.raysTable.item(rowCount, 1).setText('{}'.format(rayParams['theta']))

        self.raysTable.setItem(
            rowCount,
            2,
            QTableWidgetItem()
        )
        self.raysTable.item(rowCount, 2).setText(rayParams['color'])

    def propagate(self, lenses):

        rays = Rays()

        for i in range(self.raysTable.rowCount()):
            ray = Ray(
                float(self.raysTable.item(i, 0).text())*1e-3,
                float(self.raysTable.item(i, 1).text())
            )
            rays.add_ray(ray)

        ret = rays.propagate(
            self.get_geometry_properties(),
            lenses
        )

        return ret

    def get_colors(self):

        ret = []
        for i in range(self.raysTable.rowCount()):
            ret.append(self.raysTable.item(i, 2).text())

        return ret

    def _add_ray_dialog(self):

        dlg = AddRayDialog(self)
        dlg.exec()

    def _add_point_source_dialog(self):

        dlg = AddPointSourceDialog(self)
        dlg.exec()

    def _remove_ray(self):

        if self.raysTable.rowCount() > 0 and self.raysTable.selectionModel().hasSelection():
            self.raysTable.removeRow(self.raysTable.currentRow())


class AddRayDialog(QDialog):

    def __init__(self, parent):

        super().__init__()

        self.parent = parent

        self.rEdit = QLineEdit()
        self.thetaEdit = QLineEdit()
        self.colorEdit = QLineEdit()
        self.colorEdit.setText('C0')
        btns = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        btnBox = QDialogButtonBox(btns)
        btnBox.accepted.connect(self._accept)
        btnBox.rejected.connect(self.reject)

        form = QFormLayout()
        form.addRow(QLabel('r [mm]:'), self.rEdit)
        form.addRow(QLabel('{} [rad]:'.format(u'\u03B8')), self.thetaEdit)
        form.addRow(QLabel('Color:'), self.colorEdit)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(QLabel('Insert new ray parameters:'))
        mainLayout.addLayout(form)
        mainLayout.addWidget(btnBox)

        self.setLayout(mainLayout)

    def _accept(self):

        self.parent.add_ray_row({
            'r': float(self.rEdit.text()),
            'theta': float(self.thetaEdit.text()),
            'color': self.colorEdit.text()
        })
        self.accept()


class AddPointSourceDialog(QDialog):

    def __init__(self, parent):

        super().__init__()

        self.parent = parent

        self.rEdit = QLineEdit()
        self.thetaEdit = QLineEdit()
        self.NEdit = QLineEdit()
        self.colorEdit = QLineEdit()
        self.colorEdit.setText('C0')
        btns = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        btnBox = QDialogButtonBox(btns)
        btnBox.accepted.connect(self._accept)
        btnBox.rejected.connect(self.reject)

        form = QFormLayout()
        form.addRow(QLabel('r [mm]:'), self.rEdit)
        form.addRow(QLabel('Max {} [rad]:'.format(u'\u03B8')), self.thetaEdit)
        form.addRow(QLabel('Rays number:'), self.NEdit)
        form.addRow(QLabel('Color:'), self.colorEdit)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(QLabel('Insert point source parameters:'))
        mainLayout.addLayout(form)
        mainLayout.addWidget(btnBox)

        self.setLayout(mainLayout)

    def _accept(self):

        theta = float(self.thetaEdit.text())
        thetas = np.linspace(-theta, theta, int(self.NEdit.text()))

        for t in thetas:
            self.parent.add_ray_row({
                'r': float(self.rEdit.text()),
                'theta': t,
                'color': self.colorEdit.text()
            })

        self.accept()