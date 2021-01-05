class PDFLinkCtrl:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.connect_signals()

    def create_links(self):
        pass

    def connect_signals(self):
        self.view.buttons['Browse'].clicked.connect(self.view.open_file)
        self.view.buttons['Ok'].connect(self.create_links)
        self.view.buttons['Cancel'].connect(self.view.close)
