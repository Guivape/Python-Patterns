class Event:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

class Widget:
    def __init__(self, parent=None):
        self.parent = parent

    def handle(self, event):
        # Using a dictionary for event -> handler method
        handlers = {
            "close": self.handle_close,
            "paint": self.handle_paint,
            "down": self.handle_down,
        }
        method = handlers.get(event.name, self.handle_default)

        if callable(method):
            method(event)
        elif self.parent is not None:
            self.parent.handle(event)

    def handle_close(self, event):
        if self.parent is not None:
            self.parent.handle(event)

    def handle_paint(self, event):
        if self.parent is not None:
            self.parent.handle(event)

    def handle_down(self, event):
        if self.parent is not None:
            self.parent.handle(event)

    def handle_default(self, event):
        if self.parent is not None:
            self.parent.handle(event)

class MainWindow(Widget):
    def handle_close(self, event):
        print(f"MainWindow: {event}")

    def handle_default(self, event):
        print(f"MainWindow Default: {event}")

class SendDialog(Widget):
    def handle_paint(self, event):
        print(f"SendDialog: {event}")

class MsgText(Widget):
    def handle_down(self, event):
        print(f"MsgText: {event}")

def main():
    mw = MainWindow()
    sd = SendDialog(mw)
    msg = MsgText(sd)

    for e_name in ("down", "paint", "unhandled", "close"):
        evt = Event(e_name)

        print(f"Sending event -{evt}- to MainWindow")
        mw.handle(evt)

        print(f"Sending event -{evt}- to SendDialog")
        sd.handle(evt)

        print(f"Sending event -{evt}- to MsgText")
        msg.handle(evt)

if __name__ == '__main__':
    main()
