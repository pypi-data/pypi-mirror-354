from livenodes.viewer import View_QT
from PyQt5.QtWidgets import QFormLayout, QLabel

from ln_ports import Ports_empty
from livenodes import Ports_collection, Port

class Port_stringable(Port):

    example_values = [
        ["EMG1", "EMG2"],
        [0, 1],
        [20, .1],
        20,
        "Bla"
    ]

    def __init__(self, name='stringable', *args, **kwargs):
        super().__init__(name, *args, **kwargs)

    @classmethod
    def check_value(cls, value):
        try: 
            str(value)
            return True, None
        except Exception as err:
            return False, err

class Ports_stringable(Ports_collection):
    text: Port_stringable = Port_stringable("Text")

class Print_data(View_QT):
    ports_in = Ports_stringable()
    ports_out = Ports_empty()

    category = "Debug"
    description = ""

    example_init = {
        "name": "Display Channel Data",
    }


    def process(self, text, **kwargs):
        self._emit_draw(text=text)

    def _init_draw(self, parent):

        label = QLabel("")

        layout = QFormLayout(parent)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addRow(label)

        def update(text=None):
            nonlocal label
            label.setText(str(text))
        return update
