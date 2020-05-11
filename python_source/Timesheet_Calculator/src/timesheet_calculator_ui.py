#!/usr/bin/env python

from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from src.timesheet_calculator import TimesheetCalculator
from src.logger import Logger
from src.constants import Constants
from shutil import copyfile
import csv
import os
import tkinter.font as font


class TimesheetCalculatorUI:

    def __init__(self):
        self.logger = Logger().get_logger()
        self.window = Tk()
        self.window.title('Timesheet Calculator')
        self.window.grid_columnconfigure(1, weight=1)
        self.ts_calc = TimesheetCalculator()

    def construct_ui(self):
        font_design = font.Font(family="Helvetica", size=10)
        sv_from_date = StringVar()
        sv_to_date = StringVar()
        text = StringVar()
        text.set('No Upload')

        from_date_label = Label(self.window,
                                text="From Date:",
                                font=font_design,
                                anchor='w')
        to_date_label = Label(self.window,
                              text="To Date:",
                              font=font_design,
                              anchor='w')
        from_date_entry = Entry(self.window,
                                textvariable=sv_from_date,
                                name="time_in_entry",
                                width=36)
        to_date_entry = Entry(self.window,
                              textvariable=sv_to_date,
                              name="time_out_entry",
                              width=36)

        upload_label = Label(self.window,
                             font=font_design,
                             textvariable=text)
        upload_button = Button(self.window,
                               text='Upload',
                               command=lambda: self.import_data(text, generate_button))
        generate_button = Button(self.window,
                                 text='Generate',
                                 command=lambda: self.generate_spreadsheet(sv_from_date, sv_to_date),
                                 state=DISABLED)

        from_date_label.grid(row=0, column=0, sticky='w', pady=(5, 0))
        from_date_entry.grid(row=0, column=1, pady=(5, 0), padx=(0, 5), sticky='ew')
        to_date_label.grid(row=1, column=0, sticky='w', pady=(5, 0))
        to_date_entry.grid(row=1, column=1, pady=(5, 0), padx=(0, 5), sticky='ew')

        upload_label.grid(row=2, column=0, sticky='nswe', pady=5)
        upload_button.grid(row=2, column=1, sticky='nsw', pady=5)
        generate_button.grid(row=2, column=1, sticky='nse', pady=5, padx=(0, 5))

        self.window.mainloop()

    def import_data(self, text, generate_button):
        self.ts_calc = TimesheetCalculator()
        sel_file_full_path = filedialog.askopenfilename(initialdir='/', title='Select a file',
                                                        filetypes=(("csv files", "*.csv"), ("all files", "*.*")))

        file_name = os.path.basename(sel_file_full_path)
        if file_name != '':
            generate_button['state'] = NORMAL
            text.set(file_name)
            dst = os.path.join(Constants.INPUT_DIR, file_name)
            try:
                copyfile(sel_file_full_path, dst)
            except FileExistsError as e:
                self.logger.error(e)

            input_csv_path = os.path.join(Constants.INPUT_DIR, file_name)
            self.logger.info('Importing Datasheet...')
            try:
                with open(input_csv_path, newline='') as timesheet_csv:
                    reader = csv.DictReader(timesheet_csv)
                    for row in reader:
                        ret = self.ts_calc.add_to_list(row)
                        if ret == -1:
                            messagebox.showinfo("Error", 'Something is wrong with your csv input!')
                            self.logger.info('Importing Datasheet failed..')
                            break
            except FileNotFoundError as e:
                self.logger.error(e.strerror)
                self.logger.error('File not found!')
            self.logger.info('Importing Datasheet done..')

    def generate_spreadsheet(self, fr_date, to_date):
        fr_date_str = fr_date.get()
        to_date_str = to_date.get()
        if fr_date_str == '' or to_date_str == '':
            messagebox.showinfo("Try again", "Range date are incomplete!")
        else:
            ret1 = self.ts_calc.generate_between_days(fr_date_str, to_date_str)
            ret2 = self.ts_calc.generate_manhour_analysis(fr_date_str, to_date_str)

            if ret1 is None or ret2 is None:
                self.logger.error('You inputted an invalid date')
                messagebox.showinfo('Error', 'You inputted an invalid date')
            elif ret1 == 1 and ret2 == 1:
                messagebox.showinfo('Generation Complete', 'Check result in "Output" folder')
