import multiprocessing as mp
import numpy as np

from livenodes.viewer import View_QT
from PyQt5.QtWidgets import QLineEdit, QFormLayout, QLabel, QPushButton, QSizePolicy

from ln_ports import Ports_ts, Port_2D_Number, Port_List_Str
from livenodes import Ports_collection

class Ports_out(Ports_collection):
    # TODO: it doesn't make much sense to have this return batched data, instead these should be simple lists, which can be stacked back together if needed?
    # TODO: maybe re-consider the online v offline approaches? ie offline needs batches for performance, online doesn't know what a batch is...
    data: Port_2D_Number = Port_2D_Number("Data")
    annot: Port_List_Str = Port_List_Str("Annotation")

class Annotate_ui_button(View_QT):
    """
    Annotate a signal Stream Live via GUI Buttons.
    IMPORTANT: never use with batches. The node assumes a live signal without batches.
    IMPORTANT: we assume that the length of data is always short enough that we do not care about timing issues with the label
    """
    ports_in = Ports_ts()
    ports_out = Ports_out()

    category = "Annotation"
    description = ""

    example_init = {
        "name": "GUI Button Annotation",
        "fall_back_target": "Unknown",
    }

    def __init__(self,
                 fall_back_target="Unknown",
                 name="GUI Button Annotation",
                 **kwargs):
        super().__init__(name=name, **kwargs)

        self.fall_back_target = fall_back_target

        self.annot_target = fall_back_target
        self.current_target = fall_back_target
        self.recording = False

        self.target_q = mp.Queue()

    def _settings(self):
        """
        Get the Nodes setup settings.
        Primarily used for serialization from json files.
        """
        return { \
            "name": self.name,
            "fall_back_target": self.fall_back_target
        }

    def process(self, ts, **kwargs):
        while not self.target_q.empty():
            self.fall_back_target, self.current_target = self.target_q.get()

        return self.ret(data=ts, annot=np.repeat(self.current_target, np.array(ts).shape[0]))

    def __activity_toggle_rec(self):
        if self.recording:
            # Stop recording
            self.button.setText('Start')
            self.target_q.put((self.fall_back_target, self.fall_back_target))
        else:
            # Start recording
            self.button.setText('Stop')
            self.target_q.put((self.fall_back_target, self.annot_target))

        self.recording = not self.recording

    def __update_fallback(self, text):
        self.fall_back_target = text
        self.target_q.put((self.fall_back_target, self.annot_target))

    def __update_annot(self, text):
        self.annot_target = text

    def _init_draw(self, parent):

        qline_fallback = QLineEdit(str(self.fall_back_target))
        qline_fallback.textChanged.connect(self.__update_fallback)

        qline_current = QLineEdit(str(self.annot_target))
        qline_current.textChanged.connect(self.__update_annot)

        self.button = QPushButton("Start")
        self.button.setSizePolicy(QSizePolicy())
        self.button.clicked.connect(self.__activity_toggle_rec)


        layout = QFormLayout(parent)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addRow(QLabel("Annotate"))
        layout.addRow(QLabel('Fallback:'), qline_fallback)
        layout.addRow(QLabel('Performing:'), qline_current)
        layout.addRow(self.button)

        # layout = QVBoxLayout(parent)
        # layout.addWidget(QLabel("Annotate"), stretch=0)
        # layout.addWidget(qline_fallback)
        # layout.addWidget(qline_current)
        # layout.addWidget(self.button, stretch=2)

