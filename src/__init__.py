from gi.repository import GObject, RB, Peas


class FloonitzPlugin(GObject.Object, Peas.Activatable):
    object = GObject.property(type=GObject.Object)

    def __init__(self):
        super(FloonitzPlugin, self).__init__()

    def do_activate(self):
        print("Hello World")
