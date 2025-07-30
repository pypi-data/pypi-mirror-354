from livenodes.viewer import View_QT
from PyQt5.QtWidgets import QFormLayout, QLabel
import numpy as np
from ln_ports import Ports_empty, Ports_np

class Print_shape(View_QT):
    ports_in = Ports_np()
    ports_out = Ports_empty()

    category = "Debug"
    description = ""

    example_init = {
        "name": "Display Channel Shape",
    }

    def process(self, data_np, **kwargs):
        self._emit_draw(text=str(np.asarray(data_np).shape))

    def _init_draw(self, parent):

        label = QLabel("")

        layout = QFormLayout(parent)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addRow(label)

        def update(text=None):
            nonlocal label
            label.setText(str(text))
        return update
