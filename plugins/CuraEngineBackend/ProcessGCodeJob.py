from UM.Job import Job
from UM.Application import Application


class ProcessGCodeLayerJob(Job):
    def __init__(self, message):
        super().__init__()

        self._scene = Application.getInstance().getController().getScene()
        self._message = message

    def run(self):
        self._scene.gcode_list.append(self._message.data.decode('utf-8', 'replace'))