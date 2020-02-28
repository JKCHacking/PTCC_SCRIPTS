#!/usr/bin/env python

#################################
# Author: Joshnee Kim B. Cunanan
# Created: 4/16/2018
# Last Modified: 10/8/2019
# Version: 7.0
#################################

import threading
from tkinter import *
from tkinter import messagebox
import tkinter.font as font
from datetime import datetime
from datetime import timedelta
import time
import re

from logger import Logger

COMPLETE_TIME_INTERVAL = [
	'6:30-7:00',
	'7:00-7:30:',
	"7:30-8:00:",
	"8:00-8:30:",
	"8:30-9:00:",
	"9:00-9:30:",
	"9:30-10:00:",
	"10:00-10:30:",
	"10:30-11:00:",
	"11:00-11:30:",
	"11:30-12:00:",
	"12:00-12:30:",
	"12:30-13:00:",
	"13:00-13:30:",
	"13:30-14:00:",
	"14:00-14:30:",
	"14:30-15:00:",
	"15:00-15:30:",
	"15:30-16:00:",
	"16:00-16:30:",
	"16:30-17:00:",
	"17:00-17:30:",
	"17:30-18:00:",
	"18:00-18:30:",
	"18:30-19:00:",
	"19:00-19:30:",
	"19:30-20:00:",
	"20:00-20:30:",
	"20:30-21:00:",
	"21:00-21:30:",
	"21:30-22:00:"
]

# CONSTANTS
VERSION = "7.0"
HIDDEN_TIME = 1800
DROPDOWN_OPTIONS = ["Whole-Day", "Half-Day"]
DURATION_DICT = {
	"Whole-Day": 9,
	"Half-Day": 4
}
TIME_FORMAT = "%H:%M"

class TaskTrackerApp():

	def __init__(self):
		logger = Logger()
		self.entries = []
		self.logger = logger.get_logger()
		self.logger.info("Initializing Task Tracker App...")
		self.root = Tk()
		self.time_interval_to_display = COMPLETE_TIME_INTERVAL
		self.create_main_form()
		self.root.mainloop()

	def create_main_form(self):
		self.logger.info("Constructing the Tracker UI...")
		self.root.title(f"My Task Tracker v{VERSION}")
		self.font_design = font.Font(family="Helvetica", size=8)
		# ====================MENU=========================
		menubar = Menu(self.root)
		self.root.config(menu=menubar)

		file = Menu(menubar)
		file.add_command(label="Exit", command=self.root.quit)
		menubar.add_cascade(label="File", menu=file)

		edit = Menu(menubar)
		edit.add_command(label="Clear All", command=self.restore_default)
		menubar.add_cascade(label="Edit", menu=edit)

		self.root.grid_rowconfigure(1, weight=1)
		self.root.grid_columnconfigure(0, weight=1)

		# Major Frames
		self.top_frame = Frame(self.root, width=340, height=90, pady=3,
			name="top_frame")
		self.center_frame = Frame(self.root, name="center_frame",
			width=340, height=750, pady=3)
		bottom_frame = Frame(self.root, width=340,
			height=50, pady=3, name="bottom_frame")

		self.top_frame.grid(row=0, sticky='ew')
		self.center_frame.grid(row=1, sticky='nsew')
		bottom_frame.grid(row=2, sticky='ew')

		self.top_frame.grid_rowconfigure(0, weight=1)
		self.top_frame.grid_columnconfigure(1, weight=1)
		self.center_frame.grid_columnconfigure(1, weight=1)

		duration_label = Label(self.top_frame, text="Duration:",
			font=self.font_design, anchor='e', width=10, padx=5, pady=2)
		time_in_label = Label(self.top_frame, text="Time-in:",
			font=self.font_design, anchor='e', width=10, padx=5, pady=2)
		time_out_label = Label(self.top_frame, text="Time-out:",
			font=self.font_design, anchor='e', width=10, padx=5, pady=2)
		
		sv_time_in = StringVar()
		sv_time_out = StringVar()
		time_in_entry = Entry(self.top_frame, textvariable=sv_time_in,
			name="time_in_entry")
		time_out_entry = Entry(self.top_frame, textvariable=sv_time_out,
			name="time_out_entry")
		b3 = Button(bottom_frame, text='Save', command=self.record_hide)

		option_value = StringVar(self.top_frame)
		option_value.set(DROPDOWN_OPTIONS[0])
		duration_option = OptionMenu(self.top_frame, option_value,
			*DROPDOWN_OPTIONS,
			command=(
				lambda event: self.get_time_out(sv_time_in, option_value))
		)

		duration_label.grid(row=0, column=0)
		time_in_label.grid(row=1, column=0)
		time_out_label.grid(row=2, column=0)
		duration_option.grid(row=0, column=1, sticky='w')

		time_in_entry.grid(row=1, column=1, sticky='we', padx=(0,10))
		time_in_entry.bind('<Return>', (lambda event:
			self.get_time_out(sv_time_in, option_value)))

		time_out_entry.grid(row=2, column=1, sticky='we', padx=(0,10))
		time_out_entry.bind('<Return>', (lambda event:
			self.check_for_undertime(sv_time_out, sv_time_in, option_value)))

		self.construct_form_contents(self.center_frame)
		
		b3.pack(fill=Y, pady=(0,2))

		# Use "Ctrl+q" key as a shortcut for Quit.
		self.root.bind('<Control-q>', quit) 

	def check_for_undertime(self, sv_time_out, sv_time_in, option_value):
		# convert to datetime
		self.time_out_object = datetime.strptime(sv_time_out.get(), TIME_FORMAT)
		time_diff = self.time_out_object - self.time_in_object
		total_seconds = time_diff.total_seconds()
		hours = int(total_seconds / 3600)
		if hours < DURATION_DICT[option_value.get()]:
			messagebox.showerror("Under Time Error",
				"Please adjust time-out to avoid undertime.")
		else:
			self.get_time_out(sv_time_in, option_value)

	def get_time_out(self, sv, option_value):
		try:
			time_in_object = datetime.strptime(sv.get(), TIME_FORMAT)
			time_out_object = time_in_object + timedelta(
				hours=DURATION_DICT[option_value.get()])
			time_out_string = time_out_object.strftime(TIME_FORMAT)
			self.time_out_object = time_out_object
			self.time_in_object = time_in_object

			parent_frame = "top_frame"
			parent_path = f".{parent_frame}"
			widget_name = "time_out_entry"
			time_out_entry_object = self.get_widget_object(self.top_frame,
				parent_path, widget_name)
			time_out_entry_object.delete(0, END)
			time_out_entry_object.insert(0, time_out_string)

			self.redisplay_form_contents(self.center_frame)
		except ValueError as e:
			self.logger.error(e)
			messagebox.showerror("Invalid input time!",
				"Please input valid (24hour) time entry!")
	
	def restore_default(self):
		major_frame = {self.top_frame, self.center_frame}
		for frame in major_frame:
			self.destroy_all_widgets_in_frame(frame)
		self.time_interval_to_display = COMPLETE_TIME_INTERVAL
		self.create_main_form()

	def redisplay_form_contents(self, parent_frame):
		self.determine_time_to_display()
		self.destroy_all_widgets_in_frame(parent_frame)
		self.construct_form_contents(parent_frame)

	def determine_time_to_display(self):
		self.time_interval_to_display = []
		start_found = False
		for time_interval in COMPLETE_TIME_INTERVAL:
			time_interval_split = time_interval.split("-")
			start_time_interval = time_interval_split[0]
			end_time_interval = time_interval_split[1][:-1]

			# convert them to datetime
			start_time_dt_obj = datetime.strptime(start_time_interval,
				TIME_FORMAT)
			end_time_dt_obj = datetime.strptime(end_time_interval, TIME_FORMAT)

			if start_time_dt_obj <= self.time_in_object <= end_time_dt_obj:
				start_found = True
			if start_found:
				self.time_interval_to_display.append(time_interval)
				if start_time_dt_obj <= self.time_out_object <= end_time_dt_obj:
					break
				
	def construct_form_contents(self, center_frame):
		self.logger.info("Displaying Form...")
		self.entries = []
		entry_string = "entry"
		button_string = "button"

		for row_num, field in enumerate(self.time_interval_to_display):
			entry_name = f'{entry_string}_{row_num}'
			button_name = f'{button_string}_{row_num}'

			lab = Label(center_frame, width=10, text=field,
				font=self.font_design)
			ent = Entry(center_frame, name=entry_name)
			ent.bind('<Return>', (lambda event: self.record_hide()))

			if row_num == 0:
				cpy_btn = Button(center_frame, text="v", font=self.font_design,
					state=DISABLED)
			else:
				cpy_btn = Button(center_frame, text="v", font=self.font_design,
					name=button_name)
				cpy_btn.bind("<Button-1>", 
					(lambda event: self.copy_task_name(event)))

			lab.grid(row=row_num, column=0)
			ent.grid(row=row_num, column=1, sticky='we', padx=5, pady=2)
			cpy_btn.grid(row=row_num, column=2, padx=(0,5), pady=(0,2))
			self.entries.append((field, ent))
		return self.entries

	def destroy_all_widgets_in_frame(self, parent_frame):
		for widget in parent_frame.winfo_children():
			widget.destroy()

	def copy_task_name(self, event):
		button_name = event.widget
		split_btn_name = str(button_name).split(".")
		center_frame_name = split_btn_name[1]
		reference_number = split_btn_name[len(split_btn_name)-1].split("_")[1]

		# get the current entry widget
		parent_path = f".{center_frame_name}"
		widget_name = f"entry_{reference_number}"
		current_entry_object = self.get_widget_object(self.root, parent_path,
			widget_name)

		above_ref_number = int(reference_number)-1
		# get the above entry widget
		widget_name = f"entry_{above_ref_number}"
		above_entry_object = self.get_widget_object(self.root, parent_path,
			widget_name)

		# get the value of the above entry widget
		value_to_copy = above_entry_object.get()
		# update the value of the current entry widget
		current_entry_object.delete(0, END)
		current_entry_object.insert(0, value_to_copy)
		current_entry_object.focus()
		
	def get_widget_object(self, parent_frame, parent_path, widget_name):
		object_widget_str = f"{parent_path}.{widget_name}"
		return parent_frame.nametowidget(object_widget_str)
	
	def record_hide(self):
		#Record
		# 	 4.1 we need to create an empty Dictionary.
		summary_dict = {}
		hours_inc = 0
		self.logger.info("Copying task to file...")
		date_filename = str(datetime.now().strftime('%Y-%m-%d'))
		try:
			with open("Task_"+date_filename+".txt", "w+") as myfile:
				for entry in self.entries:
					field = entry[0]
					self.logger.info(entry[1])
					text  = entry[1].get()
					myfile.write(field+" "+text+"\n")

					if text != '' or text != ' ':
						# 3. split the string using ',' as delimiter
						temp_split = text.split(',')
						# 4. each string.split[i] will be checked if existing 
						# in the Dictionary.
						for task in temp_split:
							task = task.strip()
							result = re.search(".M Break", text)
							if result != None:
								string_length = len(temp_split)
								if task == 'AM Break' or task == 'PM Break':
									hours_inc = 0.25
								else:
									hours_inc = 0.25 / (string_length-1)
							else:
								hours_inc = 0.5/ len(temp_split)
							# 5. if not yet existing, we put it in the key 
							# and add the value by 1.
							if task not in summary_dict:
								summary_dict[task] = 0
							# 6. if existing, we locate the key and 
							# add the value by 1.
							if task in summary_dict:
								summary_dict[task] = summary_dict[task] +\
									hours_inc
				myfile.write("\n==SUMMARY==\n")
				# 7. after writing all the entries, write the Key and Value on
				# the dictionary at the end of text file.
				for task, num_task in summary_dict.items():
					myfile.write(task+": "+str((num_task))+"hr(s)\n")
			self.logger.info("Copying done...")
		except IOError as error:
			self.logger.error(f"An Error occured: {error}")
		#Hide
		self.logger.info("Hiding GUI...")
		self.root.withdraw()
		time.sleep(HIDDEN_TIME)#30mins
		self.root.update()
		self.root.deiconify()

if __name__ == "__main__":
	task_tracker = TaskTrackerApp()
