from livenodes.viewer import View_QT
from PyQt5.QtWidgets import QVBoxLayout, QLabel
from PyQt5.QtCore import Qt

from ln_ports import Ports_empty, Ports_any
import time

class Print_elapsed_time(View_QT):
    ports_in = Ports_any()
    ports_out = Ports_empty()

    category = "Info"
    description = ""

    example_init = {
        "name": "Display Elapsed Time",
    }

    def _onstart(self):
        self.start_time = time.time()

    def process(self, any, **kwargs):
       elapsed = time.time() - self.start_time
       hours = int(elapsed // 3600)
       minutes = int((elapsed % 3600) // 60)
       seconds = int(elapsed % 60)
       if hours > 0:
           text = f"{hours:02d}:{minutes:02d}:{seconds:02d}h"
       elif minutes > 0:
           text = f"{minutes:02d}:{seconds:02d}min"
       else:
           text = f"{seconds}s"
       self._emit_draw(text=text)
       
    def _init_draw(self, parent):

        label = QLabel("")
        # increase font size and center text inside the label
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("font-size: 16pt;")

        # use a vertical box layout to center label in parent
        layout = QVBoxLayout(parent)
        layout.setContentsMargins(0, 0, 0, 0)
        # add stretches to center vertically and horizontally
        layout.addStretch()
        layout.addWidget(label, alignment=Qt.AlignCenter)
        layout.addStretch()

        def update(text=None):
            nonlocal label
            label.setText(str(text))
        return update
