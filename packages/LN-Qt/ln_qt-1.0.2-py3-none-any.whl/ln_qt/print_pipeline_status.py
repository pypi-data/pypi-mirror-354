from livenodes.viewer import View_QT
from PyQt5.QtWidgets import QVBoxLayout, QLabel
from PyQt5.QtCore import Qt
from ln_ports import Ports_empty, Ports_any

class Print_pipeline_status(View_QT):
    ports_in = Ports_any()
    ports_out = Ports_empty()

    category = "Info"
    description = ""

    example_init = {
        "name": "Pipeline Status",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.running = False
        self.finished = False

    def _onstart(self):
        self.running = True
        self.finished = False
        self._emit_draw(running=self.running, finished=self.finished)

    def _onstop(self):
        self.finished = True
        self.running = False
        self._emit_draw(running=self.running, finished=self.finished)

    def process(self, any, **kwargs):
       self._emit_draw(running=self.running, finished=self.finished)
       
    # def _should_draw(self, **cur_state):
    #     return True

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

        def update(running=None, finished=None):
            nonlocal label
            if running:
                text = "Running"
            elif finished:
                text = "Finished"
            else:
                text = "Idle"
            label.setText(str(text))
        return update
