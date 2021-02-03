class Controller:
    def __init__(self, model, view):
        super().__init__()
        self.model = model
        self.view = view
        self.connect_signals()

    def connect_signals(self):
        self.view.cartoonify_btn.clicked.connect(self.view.open_cartoonified_dialog)
        self.view.upload_btn.clicked.connect(self.view.open_image_filename_dialog)
