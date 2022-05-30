class Controller:
    def __init__(self, model, view):
        super().__init__()
        self.model = model
        self.view = view

    def connect_signals(self):
        self.view.cartoonify_btn.clicked.connect(self.cartoonify)
        self.view.upload_btn.clicked.connect(self.view.open_image_filename_dialog)

    def cartoonify(self):
        image_path = self.view.image_path_le.text()
        if image_path:
            image_temp_path = self.model.cartoonify(image_path)
            self.view.open_cartoonified_dialog(image_temp_path)
        else:
            self.view.messagebox("Please upload an image!", "Warning")

