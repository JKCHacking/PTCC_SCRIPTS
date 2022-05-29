import os


class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.connect_signals()

    def split_pdf(self):
        src_pdf = self.view.input_edit.text()
        dst_pdf = os.path.splitext(self.view.output_edit.text())[0] + ".pdf"

        top_pad = self.view.pad_top_edit.text()
        bot_pad = self.view.pad_bot_edit.text()
        right_pad = self.view.pad_right_edit.text()
        left_pad = self.view.pad_left_edit.text()

        if not os.path.exists(src_pdf):
            self.view.display_message_box("Source file does not exists.", "error")
        else:
            if not top_pad.isdigit() or \
                    not bot_pad.isdigit() or \
                    not right_pad.isdigit() or \
                    not left_pad.isdigit():
                self.view.display_message_box("Padding should be numbers", "error")
            else:
                dst_pdf = os.path.join(os.path.dirname(src_pdf), dst_pdf)
                self.model.split(src_pdf, dst_pdf, float(left_pad), float(right_pad), float(top_pad), float(bot_pad))
                if os.path.exists(dst_pdf):
                    self.view.display_message_box("Splitting Done!")
                    self.view.clear_all()

    def connect_signals(self):
        self.view.browse_button.clicked.connect(self.view.open_file)
        self.view.split_button.clicked.connect(self.split_pdf)
