from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QTextEdit

from Widgets.PlotCanvas import PlotCanvas
from Widgets.RaysWidget import RaysWidget
from Widgets.ElementsWidget import OpticalElementsWidget

import numpy as np
from RayPropagation.RayPropagation import find_imaging_planes


class MainWidget(QWidget):

    def __init__(self):

        super().__init__()

        self._init_widgets()
        self._init_layout()
        self._init_UI()
    
    def _init_widgets(self):

        self.plotWidget = PlotCanvas(parent=self)
        self.raysWidget = RaysWidget()
        self.opticalElementsWidget = OpticalElementsWidget()
        self.propagateBtn = QPushButton('Propagate')
        self.propagateMessage = QTextEdit()
        self.propagateMessage.setReadOnly(True)
    
    def _init_layout(self):

        rightBox = QVBoxLayout()
        rightBox.addWidget(self.raysWidget)
        rightBox.addWidget(self.opticalElementsWidget)
        rightBox.addWidget(self.propagateBtn)
        rightBox.addWidget(self.propagateMessage)
        rightBox.addStretch(1)

        mainBox = QHBoxLayout()
        mainBox.addWidget(self.plotWidget, 0.8)
        mainBox.addLayout(rightBox, 0.2)

        self.setLayout(mainBox)
    
    def _init_UI(self):

        self.propagateBtn.clicked.connect(self.propagate)

        self.plotWidget.set_style(
            xLabel='X [mm]',
            yLabel='Y [mm]'
        )

    def propagate(self):

        try:
            geometry = self.raysWidget.get_geometry_properties()
        except ValueError:
            return 0

        lenses = self.opticalElementsWidget.get_lenses()

        xs, ys_list = self.raysWidget.propagate(lenses)
        # print(xs)

        self.plotWidget.prepare_axes(**{       
            'x1Lim': 0,
            'x2Lim': geometry['X range']*1e3,
            'y1Lim': -geometry['Y range']*1e3,
            'y2Lim': geometry['Y range']*1e3    
        })

        self.plotWidget.set_style(
            xLabel='X [mm]',
            yLabel='Y [mm]'
        )

        # Plot rays
        cs = self.raysWidget.get_colors()
        for i, ys in enumerate(ys_list):
            self.plotWidget.plot(
                xs * 1e3,
                ys * 1e3,
                c=cs[i]
            )

        # Plot apertures
        for lens in lenses:
            self.plotWidget.plot(
                [lens.position*1e3, lens.position*1e3],
                [0.5*lens.aperture*1e3, geometry['Y range']*1e3],
                c='k'
            )
            self.plotWidget.plot(
                [lens.position*1e3, lens.position*1e3],
                [-geometry['Y range']*1e3, -0.5*lens.aperture*1e3],
                c='k'
            )

        self.plotWidget.refresh()

        mes = self.find_planes(xs, lenses)
        self.propagateMessage.setText(mes)

        return 1

    def find_planes(self, xs, lenses):

        im_planes = find_imaging_planes(xs, lenses)

        ret = ''
        for plane in im_planes:
            ret += 'Imaging plane at x = {:.2f} mm\n'.format(plane['x']*1e3)
            ret += 'A = {:.4e} \n'.format(plane['A'])
            ret += 'B = {:.4e} \n'.format(plane['B'])
            ret += 'C = {:.4e} \n'.format(plane['C'])
            ret += 'D = {:.4e} \n'.format(plane['D'])

        return ret