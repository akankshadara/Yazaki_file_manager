import Tkinter as tk
import tkMessageBox as tkmb
import tkFileDialog
from PIL import Image
import calendar
import datetime
from os import walk, getcwd
import re
import time
import csv
from shutil import move, copy
from subprocess import Popen
from pandas import DataFrame, read_csv, concat
from passlib.handlers.sha2_crypt import sha256_crypt as crypt

# initializing variables
LARGE_FONT = ("Verdana", 12)
# global variables
user_db_file = ""
user_database = DataFrame()
users_list = []

path_app_data = ""
user_database = DataFrame()
user_db_file = ""

path_app_data = ''

current_folder = getcwd() #from os

revision_date = ''
receipt_date = ''
online_path = ''
absolute_path = ''
current_user = ''
current_user_category = ''
logo_path = current_folder + '\logo.gif'
logo2_path =current_folder + '\logo2.gif'
path_of_Obsolete_folder = ""		##  ## Files will be moved From here
path_of_Online_folder = ""			##  ## File will be moved To here
pdf_attached = ''						##  ## File to be browsed and saved to Online Folder


part_names_path = ""
part_names_list = ""
var_part_name = ""
projects_path = ""
projects_list = ""
var_project = ""

#read csv for part name and project master
def prepare_list(input_file):
	plist = []
	with open(input_file, 'r') as file:
		reader = csv.reader(file)
		for row in reader:
			plist.append(row[0])
	file.close()
	return plist

# to write an updated list to a csv file
def write_to_csv(plist, input_file):
	with open(input_file, 'wb') as file:
		wr = csv.writer(file, delimiter = ',')
		for i in plist:
			wr.writerow([i])
	file.close()

# to get the app_data from the path mentioned in the source text file
def connect():
	global path_app_data
	global users_list
	global user_database
	global user_db_file
	global path_of_Online_folder
	global path_of_Obsolete_folder
	global part_names_path
	global projects_path
	global csv_file
	global part_names_list
	global projects_list
	try:
		file = open('source.txt','r')
		path_app_data = str(file.read())
		user_db_file = path_app_data + "\user_db.csv"
		user_database = read_csv(user_db_file)
		user_database.set_index(["user_name"], inplace = True)
		users_list = user_database.index.values.tolist()
		users_list = sorted(users_list)
		part_names_path = path_app_data + "\part_names.csv"
		projects_path = path_app_data + "\projects.csv"
		path_of_Online_folder = path_app_data+"\Online"
		path_of_Obsolete_folder = path_app_data+"\Obsolete"
		csv_file = path_app_data + "\logs.csv"
		part_names_list = prepare_list(part_names_path)
		projects_list = prepare_list(projects_path)
		file.close()
	except:
		tkmb.showerror("ERROR","Connection Failed.")

connect()

var_part_name = ''
var_project = ''


########################################## NEW CALENDAR #################################################################
#########################################################################################################################

# the calendat widget
import calendar, datetime, Tkinter

class calendarTk(Tkinter.Frame): # class calendarTk
    """ Calendar, the current date is exposed today, or transferred to date"""
    def __init__(self,master=None,date=None,dateformat="%d-%m-%Y",command=lambda i:None):
        Tkinter.Frame.__init__(self, master)
        self.dt=datetime.datetime.now() if date is None else datetime.datetime.strptime(date, dateformat) 
        self.showmonth()
        self.command=command
        self.dateformat=dateformat
    def showmonth(self): # Show the calendar for a month
        sc = calendar.month(self.dt.year, self.dt.month).split('\n')
        for t,c in [('<<',0),('<',1),('>',5),('>>',6)]: # The buttons to the left to the right year and month
            Tkinter.Button(self,text=t,relief='flat',command=lambda i=t:self.callback(i)).grid(row=0,column=c)
        Tkinter.Label(self,text=sc[0]).grid(row=0,column=2,columnspan=3) # year and month
        for line,lineT in [(i,sc[i+1]) for i in range(1,len(sc)-1)]: # The calendar
            for col,colT in [(i,lineT[i*3:(i+1)*3-1]) for i in range(7)]: # For each element
                obj=Tkinter.Button if colT.strip().isdigit() else Tkinter.Label # If this number is a button, or Label
                args={'command':lambda i=colT:self.callback(i)} if obj==Tkinter.Button else {} # If this button, then fasten it to the command
                bg='green' if colT.strip()==str(self.dt.day) else 'SystemButtonFace' # If the date coincides with the day of date - make him a green background
                fg='red' if col>=5 else 'SystemButtonText' # For the past two days, the color red
                obj(self,text="%s"% colT,relief='flat',bg=bg,fg=fg,**args).grid(row=line, column=col, ipadx=2, sticky='nwse') # Draw Button or Label
    def callback(self,but): # Event on the button
        if but.strip().isdigit():  self.dt=self.dt.replace(day=int(but)) # If you clicked on a date - the date change
        elif but in ['<','>','<<','>>']:
            day=self.dt.day
            if but in['<','>']: self.dt=self.dt+datetime.timedelta(days=30 if but=='>' else -30) # Move a month in advance / rewind
            if but in['<<','>>']: self.dt=self.dt+datetime.timedelta(days=365 if but=='>>' else -365) #  Year forward / backward
            try: self.dt=self.dt.replace(day=day) # We are trying to put the date on which stood
            except: pass                          # It is not always possible
        if but in ['<','>','<<','>>']:
            self.showmonth() # Then always show calendar again
        else:
            self.master.destroy()
        if but.strip().isdigit(): self.command(self.dt.strftime(self.dateformat)) # If it was a date, then call the command

############################################# GUI CODE ###############################################################
######################################################################################################################
class Application(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        self.title("Part Revision Manager: Yazaki")

        container.pack(side="top", fill="both", expand = True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (LoginPage, Admin_Page, PartMaster, UserMaster, PartNameMaster, ProjectMaster, Viewer_Page, Restricted_Page, View_PDF_Admin, View_PDF_Viewer, View_PDF_Restricted):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(LoginPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.update()
        frame.reset_fields()
        frame.tkraise()

def onFrameConfigure(canvas):
		canvas.configure(scrollregion=canvas.bbox("all"))
		# '''Reset the scroll region to encompass the inner frame'''

 
############################################ LOGIN PAGE #######################################################################################
###############################################################################################################################################
  
class LoginPage(tk.Frame):
	def reset_fields(self):
		pass
	
	def about(self):
		tkmb.showinfo("About", "Made by:\nAkanksha Dara\nakankshadara7@gmail.com\nDivakar Verma\ndivakarv96@gmail.com\nBITS Pilani\nPilani Campus")
		# tk.Message(self, text = "Made by:\nAkanksha Dara\nDivakar Verma\nBITS Pilani")
	 
	# login function to verify user credentials and math the password with the hashed password
	def login_func(self, user, pw, controller):
			global path_app_data
			global user_database
			global current_user
			global current_user_category
			try:
				pwrd = user_database.loc[user.get()]["hashed_pword"]
				current_user_category = user_database.loc[user.get()]["category"]
				# print current_user_category
				if (crypt.verify(pw.get() , pwrd)):
					if(current_user_category == 'admin'):
						controller.show_frame(Admin_Page)
					elif(current_user_category == 'viewer'):
						controller.show_frame(Viewer_Page)
					elif(current_user_category == 'restricted'):
						controller.show_frame(Restricted_Page)
					current_user = user.get()
					user.set('')
					pw.set('')
				else:
					tkmb.showerror("ERROR", "Incorrect Password!")
					
			# open the new (main) window from here
			except:
			 	tkmb.showerror("ERROR", "Invalid Credentials\nCheck Username/Password!")
		

	def __init__(self, parent, controller):
		tk.Frame.__init__(self,parent)
		top = self.winfo_toplevel()
		top.rowconfigure(0, weight = 1)
		top.columnconfigure(0, weight = 1)
		top = self.winfo_toplevel()
		self.menuBar = tk.Menu(top)
		top['menu'] = self.menuBar
		self.subMenu1 = tk.Menu(self.menuBar)
		self.subMenu2 = tk.Menu(self.menuBar)
		self.subMenu3 = tk.Menu(self.menuBar)
		
		self.menuBar.add_cascade(label='File', menu=self.subMenu1)
		self.subMenu1.add_command(label='About', command = self.about)
		self.subMenu1.add_command(label = 'Exit', command=self.quit)
		self.menuBar.add_cascade(label='Help', menu=self.subMenu2)
		
		label = tk.Label(self, text="Yazaki Part Revision Manager: Login to get access!", font=LARGE_FONT)
		label.grid(row = 1, column = 1, pady= (50, 20), padx = 150, columnspan = 5)	
		user_name = tk.StringVar() # defines the widget state as string
		pword = tk.StringVar()
		user_label = tk.Label(self, text = "Username:")
		user_label.grid(row = 3, column = 1, padx = (100, 10), pady = 10, columnspan = 2)
		user_form = tk.Entry(self,textvariable=user_name) # adds a textarea widget
		user_form.grid(row = 3, column = 3, padx = 5, pady = 10, columnspan = 2)
		pword_label = tk.Label(self, text = "Password:")
		pword_label.grid(row = 4, column = 1, padx = (100, 10), pady = 10, columnspan = 2)
		pword_form = tk.Entry(self,textvariable=pword, show = "*")
		pword_form.grid(row = 4, column = 3, padx = 10, pady = 10, columnspan = 2)

		self.loginButton = tk.Button(self, foreground = 'blue', border = 3, relief = "groove" , text = 'Login')
		self.loginButton["command"] = lambda: self.login_func(user_name, pword, controller)
		self.loginButton.grid(column = 3, row = 5, padx = (5, 100), pady = 30, ipadx = 25, ipady = 0, columnspan = 2)

		self.exitButton = tk.Button(self, foreground = 'red', justify = tk.CENTER, border = 3, relief = "groove",text = 'Exit', command = self.quit)
		self.exitButton.grid(column = 1, row = 5,  padx = (210,5), pady = 30, ipadx = 35, ipady = 0, columnspan = 2)

		self.f = tk.Frame(self, bg = "red")
		self.f.grid(row = 11, column = 2, columnspan = 3, pady = 0, padx = 10)
		logo_canvas = tk.Canvas(self.f, width = 345, height = 65, bg= "yellow")
		logo_canvas.grid(row = 11, column = 3, columnspan= 5, padx = 0, pady = 0)
		logo_canvas.background = tk.PhotoImage(file= logo2_path)
		logo_canvas.create_image(175,30,image=logo_canvas.background)#,anchor='nw')

################################################################## ADMIN PAGE ##################################################################
################################################################################################################################################
		
class Admin_Page(tk.Frame):

	def reset_fields(self):
		pass

	def log_csv(self):
		global path_app_data
		csv_file = path_app_data + "\logs.csv"
		Popen([csv_file], shell = True)

	def online_csv(self):
		global online_csv
		csv_file = path_app_data + "\online.csv"
		Popen([csv_file], shell = True)
		# to open the CSV file on the local computer
	
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)

		self.gray_frame= tk.Frame(self, bg = "gray", width = 780, height = 15)
		self.gray_frame.grid(row = 0, column = 0, columnspan = 18, pady = 0, padx = 0)
		# admin_menu = tk.Menubutton(frame2, text = "Edit")
		# admin_menu.grid(row = 0, column = 0, columnspan = 2)

		
		label = tk.Label(self, text="Welcome Admin!", font=("Verdana", 12), justify = "right")
		label.grid(row = 0, column = 0, pady=10, padx=0, columnspan = 1)
		self.modify = tk.StringVar()

		self.button_frame = tk.LabelFrame(self, border = 2, text = "Admin Options")
		self.button_frame.grid(column = 0, row = 2, padx = 20, pady = 5, rowspan = 2,ipadx = 3, ipady = 3, columnspan = 5)

		# to modify an existing file/add new
		self.partButton = tk.Button(self.button_frame, border = 2, text = 'Part Master', relief = "groove")
		self.partButton["command"] = lambda: controller.show_frame(PartMaster)
		self.partButton.grid(column = 0, row = 1, padx = 5, pady = 5, rowspan = 2,ipadx = 10, ipady = 3)
		
		# to edit users
		self.userButton = tk.Button(self.button_frame, border = 2, text = 'User Master', relief = "groove")
		self.userButton["command"] = lambda: controller.show_frame(UserMaster)
		self.userButton.grid(column = 1, row = 1, padx = 5, pady = 5, rowspan = 2,ipadx = 10, ipady = 3)

		# to modify part name database
		self.part_name_master = tk.Button(self.button_frame, border = 2, text = 'Part Name Master', relief = "groove")
		self.part_name_master["command"] = lambda: controller.show_frame(PartNameMaster)
		self.part_name_master.grid(column = 2, row = 1, padx = 5, pady = 5, rowspan = 2,ipadx = 10, ipady = 3)
		
		# to modify project database
		self.project_master = tk.Button(self.button_frame, border = 2, text = 'Project Master', relief = "groove")
		self.project_master["command"] = lambda: controller.show_frame(ProjectMaster)
		self.project_master.grid(column = 3, row = 1, padx = 5, pady = 5, rowspan = 2,ipadx = 10, ipady = 3)
		
		#to open online PDFs
		self.viewer_page = tk.Button(self.button_frame, border = 2, text = 'PDF Viewer', relief = "groove")
		self.viewer_page["command"] = lambda: controller.show_frame(View_PDF_Admin)
		self.viewer_page.grid(column = 4, row = 1, padx = 5, pady = 5, rowspan = 2,ipadx = 10, ipady = 3)
		
		# to view the logs of all the part revisions
		self.csv_log = tk.Button(self.button_frame, border = 2, text = 'Logs', relief = "groove")
		self.csv_log["command"] = lambda: self.log_csv()
		self.csv_log.grid(column = 5, row = 1, padx = 5, pady = 5, rowspan = 2,ipadx = 15, ipady = 3)

		# to view the contents and logs of the PDF files in the online folder
		self.csv_online = tk.Button(self.button_frame, border = 2, text = 'Online CSV', relief = "groove")
		self.csv_online["command"] = lambda: self.online_csv()
		self.csv_online.grid(column = 6, row = 1, padx = 5, pady = 5, rowspan = 2,ipadx = 5, ipady = 3)
		
		# singing out
		self.logoutButton = tk.Button(self, foreground = 'red', cursor = "hand2", border = 3, justify = "right", relief = "flat" , text = 'Sign Out', font =("Verdana", 10))
		self.logoutButton["command"] = lambda: controller.show_frame(LoginPage)
		self.logoutButton.grid(column = 4, row = 0, padx = 5, pady = 0, ipadx = 1, ipady = 0)

		self.f = tk.Frame(self, bg = "red")
		self.f.grid(row = 10, column = 0, columnspan = 5, pady = 50, padx = 10)
		logo_canvas = tk.Canvas(self.f, width = 370, height = 70, bg= "yellow")
		logo_canvas.grid(row = 10, column = 0, columnspan= 5, padx = 0, pady = 0)
		logo_canvas.background = tk.PhotoImage(file=logo2_path)
		logo_canvas.create_image(190,30,image=logo_canvas.background)#,anchor='nw')

############################################# PART MASTER ###############################################################
#########################################################################################################################		

class PartMaster(tk.Frame):

	# function to reset all the canvas fields and variables
	def reset_fields(self):
		global file_name
		global part_names_list
		global projects_list
		file_name = ""
		self.fname_canvas.delete("all")
		self.rev_date_canvas.delete("all")
		self.receipt_date_canvas.delete("all")
		self.pdf_name.set("")
		self.part_name.set("Select Part") # defines the widget state as string
		self.rev_number.set("")
		self.part_number.set("") 
		self.project.set("Select Project")
		self.rev_date = ""
		self.rec_date = ""
		self.project_name_menu = tk.OptionMenu(self.entry_frame, self.project , *projects_list)
		self.project_name_menu.grid(row = 5, column = 2, padx = 2, pady = 10, ipadx = 15, columnspan = 4)
		self.part_name_menu = tk.OptionMenu(self.entry_frame, self.part_name , *part_names_list)
		self.part_name_menu.grid(row = 4, column = 2, padx = 2, pady = 10,columnspan = 4, ipadx = 25)
		


	def signout(self, controller):
		global current_user_category
		global current_user
		current_user_category = ''
		current_user = ''
		self.reset_fields()
		self.modify.set("")
		controller.show_frame(LoginPage)


	# to display text on the Tkinter canvas
	def text_on_canvas(self, name):
		global file_name
		file_name = name.get()
		selected_pdf = name.get()
		self.fname_canvas.delete("all")
		self.fname_canvas.create_text(10, 10, text = str(selected_pdf), font = ('Pursia', 9,'bold'), justify = tk.LEFT, anchor = 'w')
		# removing ".pdf" from the string
	 	selected_pdf = selected_pdf.replace(' ', '')[:-4].upper()
		#splitting the string about "_" and stroing separated values in a list 
		split_string = selected_pdf.split("_")
		# declaring variables
		part_num = split_string[0]
		self.part_number.set(part_num)
		part_name = split_string[1]
		self.part_name.set(part_name)
		project = split_string[2]
		self.project.set(project)
		rev_num = split_string[3]
		rev_date = split_string[4]
		self.rev_date = rev_date
		receipt_date = split_string[5]
		self.rec_date = receipt_date

		self.part_form.delete(0, 'end')
		self.part_form.insert(0, str(part_num))

		self.rev_num_form.delete(0, 'end')
		self.rev_num_form.insert(0, str(rev_num))

		self.rev_date_canvas.delete("all")
		self.rev_date_canvas.create_text(10, 10, text = str(rev_date), font = ('Pursia', 9,'bold'), justify = tk.LEFT, anchor = 'w')
		
		self.receipt_date_canvas.delete("all")
		self.receipt_date_canvas.create_text(10, 10, text = str(receipt_date), font = ('Pursia', 9,'bold'), justify = tk.LEFT, anchor = 'w')
		
	def search(self, to_search, controller):
		# search function to browse through the list in scroll menu. 
		key = self.to_search.get()
		self.searchBox.insert(0, str(key))
		global path_of_Online_folder
		search_list = next(walk(path_of_Online_folder))[2]  #from os

		display_list = []
		for f in search_list:
			if (re.search(key.lower(), f.lower()) != None):
				display_list.append(f)

		self.canvas.delete("all")
		self.scroll(display_list, controller)
	
	# the scroll function to insert a list into the scroll menu on the GUI
	def scroll(self, files, controller):

		i=1
		buttons = [] 

		self.canvas = tk.Canvas(self.online_Frame, borderwidth=0, width = 220, height = 412)
		self.frame = tk.Frame(self.canvas)
		
		self.vsb = tk.Scrollbar(self.online_Frame, orient="vertical", command=self.canvas.yview)
		self.canvas.configure(yscrollcommand=self.vsb.set)
		self.vsb.grid(row = 0 , column = 11, rowspan = 10, columnspan = 5, sticky = "nsew", padx = 0)

		# self.canvas.xview_moveto(0)
		self.hsb = tk.Scrollbar(self.online_Frame, orient="horizontal", command=self.canvas.xview, width =20)
		self.canvas.configure(xscrollcommand=self.hsb.set)
		self.hsb.grid(row = 10 , column = 1, rowspan = 1, columnspan = 20, sticky = "nsew")

		self.canvas.grid(row = 0 , column = 6, rowspan = 10, columnspan =5, sticky = 'w', padx = 0)
		self.canvas.create_window((5,15), window=self.frame, anchor="nw", tags="self.frame")
		self.frame.bind("<Configure>", lambda event, canvas=self.canvas: onFrameConfigure(self.canvas))

		# serach bok to implement search function
		self.to_search = tk.StringVar()
		self.searchBox = tk.Entry(self.online_Frame, width = 32, border = 2, textvariable = self.to_search, relief = "groove", bg = "white")
		self.searchBox.grid(column = 5, row = 11, padx = 0, pady = 0, rowspan = 2,columnspan = 6,ipadx = 10, ipady = 3)
		self.searchButton = tk.Button(self.online_Frame, cursor = "hand2", width = 3, border = 2, text = "Go", relief = "groove", fg = "blue")
		self.searchButton["command"] = lambda: self.search(self.to_search, controller)
		self.searchButton.grid(column = 11, row = 11, padx = 0, pady = 0, rowspan = 2,ipadx = 1, ipady = 2)

		for f in files:
			b = tk.Radiobutton(self.frame, text=' ' + str(f), variable = self.pdf_name, anchor='w', value = f, indicatoron=0, relief = "ridge", width= 60, justify = "left")
			b.grid(row=i, padx = 0, ipadx = 20, ipady = 2, sticky = "w")
			b['command'] = lambda: self.text_on_canvas(self.pdf_name)
			buttons.append(b)
			i+=1

	def attach_file(self):
		global pdf_attached
		pdf_attached = tkFileDialog.askopenfilename(defaultextension = ".pdf", title = "Select PDF")

	# to toggle between the add and modify options while uploading files
	def toggle_modify(self):
		modify = self.modify.get()

		global projects_list
		global part_names_list
		
		if (modify == '0'):
			self.part_name_menu.config(state = "normal")
			self.project_name_menu.config(state = "normal")
			self.part_form.config(state="normal")
			self.pdf_name.set("")
			self.part_form.delete(0, 'end')
			self.rev_num_form.delete(0, 'end')
			self.part_number.set("")
			self.part_name.set("Select Part")
			self.project.set("Select Project")
			self.fname_canvas.delete("all")
			self.receipt_date_canvas.delete("all")
			self.receipt_date = ""
			
		elif (modify == '1'):
			self.part_name_menu.config(state = "disabled")
			self.project_name_menu.config(state = "disabled")
			
	def Go(self, controller):
		# to refresh the scroll window
		global path_of_Online_folder
		files = next(walk(path_of_Online_folder))[2] #from os
		self.scroll(files, controller)

	def print_rev_date(self, date):
		self.rev_date_canvas.delete("all")
		self.rev_date_canvas.create_text(10,10, text = str(date), font = ('Pursia', 9), justify = tk.LEFT, anchor = 'w')
		self.rev_date = date
		# print date

	def call_calendar_rev(self):
		root = tk.Toplevel(self)
		current_date = time.strftime("%d-%m-%Y") 
		c = calendarTk(root, date = current_date, dateformat = "%d-%m-%Y", command = self.print_rev_date)
		c.pack()

	def print_receipt_date(self, date):
		self.receipt_date_canvas.delete("all")
		self.receipt_date_canvas.create_text(10,10, text = str(date), font = ('Pursia', 9), justify = tk.LEFT, anchor = 'w')
		self.rec_date = date
		# print date

	def call_calendar_receipt(self):
		root = tk.Toplevel(self)
		current_date = time.strftime("%d-%m-%Y") 
		c = calendarTk(root, date = current_date, dateformat = "%d-%m-%Y", command = self.print_receipt_date)
		c.pack()

	def check_fields_for_modify(self):
		a = self.rev_number.get()
		b = self.rev_date.get()
		c = self.receipt_date.get()
		if(a != '' and b != '' and c != ''):
			return True
		else:
			return False

	def check_fields_for_add(self):
		a = self.part_number.get()
		b = self.part_name.get()
		c = self.project.get()
		d = self.receipt_date.get()
		if(a!='' and b!='' and c!='' and d!=''):
			return True
		else:
			return False


	def save_file(self, add_or_modify, controller):
		global path_of_Online_folder
		global path_of_Obsolete_folder
		global pdf_attached
		global file_name
		global csv_file
		global current_user
		global path_app_data

		logs_csv = path_app_data + "\online.csv"
		f = read_csv(logs_csv)
		f.set_index(["Part_no"], inplace = True)
							
		today = str(time.strftime("%d-%m-%Y"))
		part_num =  self.part_number.get()
		part_num = part_num.upper()
		part_name = self.part_name.get()
		project = self.project.get()
		rev_number = self.rev_number.get()
		rev_number = rev_number.upper()
		rev_date =  str(self.rev_date)
		rec_date = str(self.rec_date)
		
			
		# current_pdf_path = path_of_Online_folder + "/" + self.pdf_name.get()
		try:
			if(self.modify.get() != ""):
				flag= str(add_or_modify.get())
				# print "value of flag " + flag
				if(pdf_attached != ""):
					file_to_be_moved = path_of_Online_folder +"/"+self.pdf_name.get()	#which is selected from the enlisted files in Online Folder / scroll Window

					if (self.modify.get() == '1'):
						move(file_to_be_moved, path_of_Obsolete_folder) #from shutil
						self.Go(controller)
						flag = "0"
						# try:
						f.drop(str(part_num).upper(), inplace = True)
						f.to_csv(logs_csv)
						# except:
						# 	tkmb.showerror("ERROR", "Check if the CSV file is open.")
						
					if (flag =="0"):
						if (rev_date ==""):
							rev_date = str(time.strftime("%d-%m-%Y"))
						if (rev_number == ""):
							rev_number="0"
						renamed = path_of_Online_folder + '/'+part_num+"_"+part_name+"_"+project+"_"+rev_number+"_"+rev_date+"_"+rec_date+ ".pdf"
						copy(pdf_attached, renamed) #from shutil

						csv_input = str(part_num)+ ',' + str(part_name) +',' + str(project) + ',' + str(rev_number) + ',' + str(rev_date) + ',' + str(rec_date) + ',' + str(current_user) +',' + str(today) + "\n"
						
						try:		
							with open(csv_file, 'a') as csvfile:
								csvfile.write(csv_input)
								csv_input = ""
							csvfile.close()	
						except:
							tkmb.showerror("ERROR", "Check if the CSV file is open.")
						try:
							new_entry = DataFrame({'Part_name':str(part_name), "Project" : str(project),"Rev_no":str(rev_number),"Rev_date":str(rev_date), "Recepipt_date":str(rec_date) ,"Modifier":str(current_user), "Modified_date" : str(today)}, index = [part_num])
							frames = [f, new_entry]
							f = concat(frames)
							f.to_csv(logs_csv)
						except Exception as e:
							tkmb.showerror("ERROR", "Check if the CSV file is open.")
						
						self.Go(controller)
						self.reset_fields()
						pdf_attached=""
				else:
					tkmb.showerror("ERROR", "New PDF not selected!")
			else:
				tkmb.showerror("ERROR", "Select Add/Modify")
		except Exception as e:
			tkmb.showerror("ERROR", str(e))

	def back(self, controller):
		controller.show_frame(Admin_Page)
		global path_of_Online_folder
		self.modify.set("")
		files=next(walk(path_of_Online_folder))[2] #from os
		self.scroll(files, controller)
	
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		global path_of_Online_folder

		self.gray_frame= tk.Frame(self, bg = "gray", width = 780,  height = 15)
		self.gray_frame.grid(row = 0, column = 1, columnspan = 25, pady = 0, padx = 0)
		
		# singing out
		self.logoutButton = tk.Button(self, foreground = 'red', cursor = "hand2", border = 3, justify = "right", relief = "flat" , text = 'Sign Out', font =("Verdana", 10))
		self.logoutButton["command"] = lambda: self.signout(controller)
		self.logoutButton.grid(row = 0, column = 12, padx = 0, pady = 0, ipadx = 1, ipady = 0)

		self.backButton = tk.Button(self, border = 2, text = 'Back', relief = "flat", cursor = "hand2", foreground = 'red', font =("Verdana", 10))
		self.backButton["command"] = lambda: self.back(controller)
		self.backButton.grid(row = 0, column = 1, padx = 10, pady = 0, ipadx = 1, ipady = 0)

		self.pdf_name = tk.StringVar()
		self.part_number = tk.StringVar() 
		self.part_name = tk.StringVar() # defines the widget state as string
		self.rev_number = tk.StringVar()
		self.project = tk.StringVar()
		self.rev_date = ""
		self.rec_date = ""

		self.entry_frame = tk.LabelFrame(self, border = 2, text = "Part Revision")
		self.entry_frame.grid(column = 1, row = 1, padx = (15,2), pady = 8, rowspan = 2,ipadx = 3, ipady = 3, columnspan = 7)

		self.label1 = tk.Label(self.entry_frame, text="Enter details & upload PDF", font=LARGE_FONT)
		self.label1.grid(row = 0, column = 1,pady=15, padx= 20)

		self.part_label = tk.Label(self.entry_frame, text = "Part Number:", justify = "left")
		self.part_label.grid(row = 3, column = 1, padx = 10, pady = 10)

		self.part_form = tk.Entry(self.entry_frame,textvariable = self.part_number, width = 25) # adds a textarea widget
		self.part_form.grid(row = 3, column = 2, padx = 20 ,pady = 10,columnspan = 4)

		self.part_name_label = tk.Label(self.entry_frame, text = "Part Name:", justify = "left")
		self.part_name_label.grid(row = 4, column = 1, padx = 10, pady = 10)

		# part_name_var = tk.StringVar()
		self.part_name.set('Select Part')
		global part_names_list
		self.part_name_menu = tk.OptionMenu(self.entry_frame, self.part_name , *part_names_list)
		self.part_name_menu.grid(row = 4, column = 2, padx = 2, pady = 10,columnspan = 4, ipadx = 25)
		self.part_name_menu["menu"].config(bg = "white")
		
		################ drop menu for projects
		self.project_label = tk.Label(self.entry_frame, text = " Project:", justify = "left")
		self.project_label.grid(row = 5, column = 1, padx = 10, pady = 10, ipadx = 5)

		# project_name_var = tk.StringVar()
		self.project.set('Select Project')
		global projects_list
		self.project_name_menu = tk.OptionMenu(self.entry_frame, self.project , *projects_list)
		self.project_name_menu.grid(row = 5, column = 2, padx = 2, pady = 10, ipadx = 15, columnspan = 4)
		# self.project_name_menu.config(relief = "flat")
		self.project_name_menu["menu"].config(bg = "white")
		
		
		self.rev_num_label = tk.Label(self.entry_frame, text = "       Drawing Revision Number:", justify ="left")
		self.rev_num_label.grid(row = 6, column = 1, ipadx = 5, padx = 10, pady = 10, columnspan = 2)

		self.rev_num_form = tk.Entry(self.entry_frame,textvariable = self.rev_number)
		self.rev_num_form.grid(row = 6, column = 2, padx = 5, pady = 10,columnspan = 4)
		
		self.rev_date_label = tk.Label(self.entry_frame, text = "Drawing Revision Date:", justify = "left")
		self.rev_date_label.grid(row = 7, column = 1, padx = 5, pady = 10, columnspan = 2)

		# self.rev_date_text = tk.Text(self.entry_frame, bg = "yellow", height = 1, width = 15)
		# self.rev_date_text.grid(row = 7, column = 2, padx = 5, pady = 10,columnspan = 4)
		self.rev_date_canvas = tk.Canvas(self.entry_frame, bg = "white", height = 18, width = 140)
		self.rev_date_canvas.grid(row = 7, column = 2, padx = 5, pady = 10,columnspan = 4)


		self.rev_dateButton = tk.Button(self.entry_frame, text = "Date",cursor = "hand2", command = lambda: self.call_calendar_rev())
		self.rev_dateButton.grid(row = 7, column = 5)

		# make date widget over here!
		self.date_label = tk.Label(self.entry_frame, text = "   Receipt Date:", justify = "left")
		self.date_label.grid(row = 8, column = 1, padx = 10, pady = 10)

		self.receipt_date_canvas = tk.Canvas(self.entry_frame, bg = "white", height = 18, width = 140)
		self.receipt_date_canvas.grid(row = 8, column = 2, padx = 5, pady = 10,columnspan = 4)

		self.receipt_dateButton = tk.Button(self.entry_frame, text = "Date", cursor = "hand2", command = lambda: self.call_calendar_receipt())
		self.receipt_dateButton.grid(row = 8, column = 5)

		self.project_name_label = tk.Label(self.entry_frame, text = 'Selected File:', justify = "left", anchor = 'w')
		self.project_name_label.grid(row = 11, column = 1, padx = 10, pady = 0, ipadx = 5)

		self.fname_canvas = tk.Canvas(self.entry_frame, bg = "white", height = 22, width = 350)
		self.fname_canvas.grid(row = 12, column = 1, padx = 2, pady = (0,5),columnspan = 6)


		self.button_frame = tk.LabelFrame(self.entry_frame, border = 2)
		self.button_frame.grid(column = 0, row = 9, padx = (35,5), pady = 0, rowspan = 2,ipadx = 3, ipady = 3, columnspan = 7)

		self.modify = tk.StringVar()
		# to add a new file
		self.newButton = tk.Radiobutton(self.button_frame, border = 2, text = 'Add', relief = "groove", variable=self.modify, value = 0, indicatoron = 0)
		self.newButton["command"] = lambda:self.toggle_modify()
		self.newButton.grid(column = 1, row = 9 , padx = 6, pady = 3, rowspan = 2,ipadx = 38, ipady = 3)
		# to modify an existing file
		self.modifyButton = tk.Radiobutton(self.button_frame, border = 2, text = 'Modify', relief = "groove", variable=self.modify, value = 1, indicatoron = 0)
		self.modifyButton["command"] = lambda:self.toggle_modify()
		self.modifyButton.grid(column = 2, row = 9, padx = 6, pady = 3, rowspan = 2,ipadx = 30, ipady = 3)

		self.attachButton = tk.Button(self.button_frame, border = 2, text = 'Attach PDF', relief = "groove", fg = "blue")
		self.attachButton["command"] = lambda:self.attach_file()
		self.attachButton.grid(column = 1, row = 11, padx = 6, pady = 3, rowspan = 2,ipadx = 20, ipady = 3)

		self.saveButton = tk.Button(self.button_frame, border = 2, text = 'Save', relief = "groove", foreground = 'darkgreen')
		self.saveButton["command"] = lambda:self.save_file(self.modify,controller)
		self.saveButton.grid(column = 2, row = 11, padx = 6, pady = 3, rowspan = 2,ipadx = 35, ipady = 3)

		self.f = tk.Frame(self, bg = "red")
		self.f.grid(row = 10, column = 12, columnspan = 2, pady = 3, padx = 0)
		logo_canvas = tk.Canvas(self.f, width = 120, height = 35, bg= "yellow")
		logo_canvas.grid(row = 10, column = 3, columnspan= 5, padx = 0, pady = 0)
		logo_canvas.background = tk.PhotoImage(file=logo_path)
		logo_canvas.create_image(60, 18,image=logo_canvas.background)#,anchor='nw')


		self.online_Frame = tk.LabelFrame(self, border = 2, text = "Browse Online",  width = 240, height = 485)
		self.online_Frame.grid(row = 1, column = 8, padx = (4,7), pady = 25, columnspan = 6)

		files=next(walk(path_of_Online_folder))[2] #from os
		self.scroll(files, controller)

############################################# USER MASTER ###############################################################
#########################################################################################################################
class password_change_popupWindow(object):
	def __init__(self,master):
		
		top=self.top=tk.Toplevel(master)
		top.maxsize(340,200)
		top.minsize(340,200)
		top.title('Change Password')

		self.l=tk.Label(top,text="Current Password:")
		self.l.grid(row = 0, column = 0, padx = 15, pady = 15, sticky = 'w')
		self.curr_pword=tk.Entry(top, show = '*')
		self.curr_pword.grid(row = 0, column = 1, padx = 25, pady = 15)

		self.l1=tk.Label(top,text="New password:")
		self.l1.grid(row = 1, column = 0, padx = 15, pady = 5, sticky = 'w')
		self.new_p1=tk.Entry(top, show = '*')
		self.new_p1.grid(row = 1, column = 1, padx = 25, pady = 5)

		self.l1=tk.Label(top,text="Confirm New password:")
		self.l1.grid(row = 2, column = 0, padx = 15, pady = 5, sticky = 'w')
		self.new_p2 =tk.Entry(top, show = '*')
		self.new_p2.grid(row = 2, column = 1, padx = 25, pady = 5)

		self.okButton=tk.Button(top,text='Ok',command=self.cleanup)
		self.okButton.grid(row = 3, column = 1, padx = 20, pady = 20, ipadx = 15)

	def cleanup(self):
		global user_database
		global current_user
		current_password = user_database.loc[current_user]["hashed_pword"]
		entered_password=self.curr_pword.get()
		p1 = self.new_p1.get()
		p2 = self.new_p2.get()

		if(p1 != '' and p2 != '' and entered_password != ''):
			# if(current_password == entered_password):
			if (crypt.verify(entered_password ,current_password)):
				if(p1 == p2):
					new_password = p1
					user_database.loc[current_user]["hashed_pword"] = crypt.encrypt(new_password)
					user_database.to_csv(user_db_file)
					tkmb.showinfo("SUCCESS","Password successfully changed.")
					self.top.destroy()
				else:
					tkmb.showerror("ERROR", "Passwords do not match.")
			else:
				tkmb.showerror("ERROR", "Please enter your correct password.")
		else:
			tkmb.showerror("ERROR", "Empty feilds!")


class add_new_user_popupWindow(object):
	def __init__(self,master):
		
		top=self.top=tk.Toplevel(master)
		top.maxsize(350,270)
		top.minsize(350,270)
		top.title('Change Password')

		self.l=tk.Label(top,text="New User Name:")
		self.l.grid(row = 0, column = 0, padx = 15, pady = 15, sticky = 'w')
		self.new_user_name=tk.Entry(top)
		self.new_user_name.grid(row = 0, column = 1, padx = 25, pady = 15)

		self.l1=tk.Label(top,text="New password:")
		self.l1.grid(row = 1, column = 0, padx = 15, pady = 5, sticky = 'w')
		self.new_p1=tk.Entry(top, show = '*')
		self.new_p1.grid(row = 1, column = 1, padx = 25, pady = 5)

		self.l1=tk.Label(top,text="Confirm New password:")
		self.l1.grid(row = 2, column = 0, padx = 15, pady = 5, sticky = 'w')
		self.new_p2 =tk.Entry(top, show = '*')
		self.new_p2.grid(row = 2, column = 1, padx = 25, pady = 5)

		self.isAdmin = tk.IntVar()
		self.isAdmin.set(0)
		self.l1=tk.Label(top,text="User Category:")
		self.l1.grid(row = 3, column = 0, padx = 15, pady = 5, sticky = 'w')
		self.admin_option =tk.Radiobutton(top, text = "Admin", variable = self.isAdmin, value = 1)
		self.admin_option.grid(row = 3, column = 1, padx = 5, pady = 5)
		self.viewer_option =tk.Radiobutton(top, text = "Viewer", variable = self.isAdmin, value = 0)
		self.viewer_option.grid(row = 4, column = 1, padx = 5, pady = 5)
		self.restricted_option =tk.Radiobutton(top, text = "Restricted", variable = self.isAdmin, value = 2)
		self.restricted_option.grid(row = 5, column = 1, columnspan = 3,  padx = 5, pady = 5)

		self.okButton=tk.Button(top,text='Ok',command=self.cleanup)
		self.okButton.grid(row = 6, column = 1, padx = 20, pady = 20, ipadx = 25)

	def cleanup(self):
		global user_database
		global users_list
		new_user = self.new_user_name.get()
		p1 = self.new_p1.get()
		p2 = self.new_p2.get()
		is_admin = self.isAdmin.get()
		
		if(is_admin == 1):
			cat = 'admin'
		elif(is_admin == 0):
			cat = 'viewer'
		else:
			cat = 'restricted'

		if (new_user not in users_list) and (new_user != '') and (p1 != '') and (p2 != 0):
			if(p1 == p2):
				new_password = crypt.encrypt(p1)
				new_entry = DataFrame({'hashed_pword': new_password, 'category' : cat}, index = [new_user])
				frames = [user_database, new_entry]
				user_database = concat(frames)
				user_database.to_csv(user_db_file)
				users_list.append(new_user)			
				users_list = sorted(users_list)
				tkmb.showinfo("SUCCESS", "New user (" + str(new_user) + ") added.")
				self.top.destroy()
			else:
				tkmb.showerror("ERROR", "Passwords do not match.")
		elif(new_user in users_list):
			tkmb.showerror("ERROR", "User name already exists.")
		else:
			tkmb.showerror("ERROR", "Empty fields!")

selected_user = ''
class delete_user_popupWindow:

	def text_on_canvas(self, user):
		global selected_user
		selected_user = user.get()
		self.pname_canvas.delete("all")
		self.pname_canvas.create_text(10, 10, text = str(selected_user), font = ('Pursia', 9,'bold'), justify = tk.LEFT, anchor = 'w')
	
	def scroll(self, plist):	

			i=1
			user = tk.StringVar()
			buttons = [] 

			self.canvas = tk.Canvas(self.online_Frame, borderwidth=0, width = 120, height = 130)
			self.frame = tk.Frame(self.canvas)
			
			self.vsb = tk.Scrollbar(self.online_Frame, orient="vertical", command=self.canvas.yview)
			self.canvas.configure(yscrollcommand=self.vsb.set)
			self.vsb.grid(row = 0 , column = 5, rowspan = 10, sticky = "nsew")

			self.canvas.grid(row = 0 , column = 0, rowspan = 10, sticky = 'w')
			self.canvas.create_window((5,15), window=self.frame, anchor="nw",  tags="self.frame")
			self.frame.bind("<Configure>", lambda event, canvas=self.canvas: onFrameConfigure(self.canvas))
			
			files = sorted(plist)
			for f in files:
				b = tk.Radiobutton(self.frame, text=' ' + str(f), cursor = "hand2", variable = user, anchor='w', value = f, indicatoron=0, relief = "ridge", width= 14, justify = "left")
				b['command'] = lambda: self.text_on_canvas(user)
				b.grid(row=i, padx = 2, ipadx = 10, ipady = 2, sticky = "w")
				buttons.append(b)
				i+=1

	def __init__(self,master):
		global users_list
		
		top=self.top=tk.Toplevel(master)
		top.maxsize(640,250)
		top.minsize(640,250)
		top.title('Delete Existing User')

		self.l=tk.Label(top,text="Browse for User Name", font = LARGE_FONT)
		self.l.grid(row = 0, column = 0, padx = 5, pady = 15, sticky = 'w')

		self.online_Frame = tk.LabelFrame(top, border = 2, text = "Browse Users", width = 350, height = 250)
		self.online_Frame.grid(row = 0, column = 5, padx = (4,7), pady = 25, columnspan = 6, rowspan = 10, sticky = 'e')

		self.scroll(users_list)
		
		self.l1=tk.Label(top, text="Selected User:")
		self.l1.grid(row = 1, column = 0, padx = 25, pady = 5, sticky = 'w')
		
		self.pname_canvas = tk.Canvas(top, bg = "white", height = 17, width = 165)
		self.pname_canvas.grid(row = 1, column = 1, padx = 15, pady = 10,columnspan = 2)

		self.l1=tk.Label(top,text="Enter password:")
		self.l1.grid(row = 2, column = 0, padx = 25, pady = 5, sticky = 'w')

		self.pwrd = tk.StringVar()
		self.pwrd1 =tk.Entry(top, show = '*', width = 27, textvariable = self.pwrd)
		self.pwrd1.grid(row = 2, column = 1, padx = 15, pady = 5)

		self.okButton=tk.Button(top,text='Delete',command=lambda:self.cleanup(), foreground = "red")
		self.okButton.grid(row = 5, column = 1, padx = 60, pady = 40, ipadx = 45)

	def cleanup(self):
		global user_database
		global users_list
		global selected_user
		global current_user

		if (selected_user == current_user):
			tkmb.showerror("ERROR", "Cannot delete curent user!")

			self.top.destroy()

		pwrd = self.pwrd.get()
		hash_pword = user_database.loc[selected_user]["hashed_pword"]

		result = tkmb.askquestion('Delete', 'Delete '+ str(selected_user) + ' ?', icon = 'warning')
		if(result=='yes'):
			
			if pwrd != '':
				if(crypt.verify(pwrd, hash_pword)):
					user_database.drop(selected_user, inplace = True)
					user_database.to_csv(user_db_file)
					users_list = user_database.index.values.tolist()
					self.scroll(users_list)		
					tkmb.showinfo("SUCCESS", "User (" + str(selected_user) + ") deleted.")
					self.pname_canvas.delete("all")
					self.top.destroy()
				else:
					tkmb.showerror("ERROR", "Incorrect Password!")
			else:
				tkmb.showerror("ERROR", "Empty fields!")

	
class UserMaster(tk.Frame):
	def reset_fields(self):
		pass

	def change_password_popup(self):
		self.w=password_change_popupWindow(self.master)
		self.master.wait_window(self.w.top)

	def add_new_user_popup(self):
		self.w=add_new_user_popupWindow(self.master)
		self.master.wait_window(self.w.top)

	def delete_existing_user_popup(self):
		self.w = delete_user_popupWindow(self.master)
		self.master.wait_window(self.w.top)

	def entryValue(self):
		return self.w.value

	def signout(self, controller):
		global current_user_category
		global current_user
		current_user_category = ''
		current_user = ''
		controller.show_frame(LoginPage)

	
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		
		self.gray_frame= tk.Frame(self, bg = "gray", width = 780, pady = 0, padx = 0, height = 15)
		self.gray_frame.grid(row = 0, column = 0, columnspan = 18)
		
		self.label1 = tk.Label(self, text="User Master", font=LARGE_FONT)
		self.label1.grid(row = 0, column = 0,pady=15, padx= 20)

		# singing out
		self.logoutButton = tk.Button(self, foreground = 'red', cursor = "hand2", border = 3, justify = "right", relief = "flat" , text = 'Sign Out', font =("Verdana", 10))
		self.logoutButton["command"] = lambda: self.signout(controller)
		self.logoutButton.grid(row = 0, column = 9, padx = 0, pady = 0, ipadx = 1, ipady = 0)

		self.backButton = tk.Button(self, border = 2, text = 'Back', relief = "flat", cursor = "hand2", foreground = 'red', font =("Verdana", 10))
		self.backButton["command"] = lambda: controller.show_frame(Admin_Page)
		self.backButton.grid(row = 0, column = 10, padx = 10, pady = 0, ipadx = 1, ipady = 0)

		self.button_frame = tk.LabelFrame(self, border = 2, text = "Admin Options")
		self.button_frame.grid(column = 0, row = 1, padx = 20, pady = 5, rowspan = 2,ipadx = 3, ipady = 3, columnspan = 2)

		# to change password
		self.partButton = tk.Button(self.button_frame, border = 2, text = 'Change My Password', relief = "groove")
		self.partButton["command"] = lambda: self.change_password_popup()
		self.partButton.grid(column = 0, row = 1, padx = 5, pady = 5, rowspan = 2,ipadx = 25, ipady = 3)
		
		# to edit users
		self.userButton = tk.Button(self.button_frame, border = 2, text = 'Add New User', relief = "groove")
		self.userButton["command"] = lambda: self.add_new_user_popup()
		self.userButton.grid(column = 1, row = 1, padx = 5, pady = 5, rowspan = 2,ipadx = 40, ipady = 3)

		# to modify part name database
		self.delete_user_button = tk.Button(self.button_frame, border = 2, text = 'Delete User', relief = "groove")
		self.delete_user_button["command"] = lambda: self.delete_existing_user_popup()
		self.delete_user_button.grid(column = 2, row = 1, padx = 5, pady = 5, rowspan = 2,ipadx = 45, ipady = 3)
		
##############################################################################################################################		
##############################################################################################################################
def signout(self, controller):
		global current_user_category
		global current_user
		current_user_category = ''
		current_user = ''
		self.pname_canvas.delete("all")
		controller.show_frame(LoginPage)

def back(self, controller):
	self.pname_canvas.delete("all")
	controller.show_frame(Admin_Page)
############################################# PART NAME MASTER ###############################################################
##############################################################################################################################

class PartNameMaster(tk.Frame):
	global var_part_name

	def reset_fields(self):
		pass
	
	def text_on_canvas(self, pname):
		global var_part_name
		var_part_name = pname.get()
		self.pname_canvas.delete("all")
		self.pname_canvas.create_text(10, 10, text = str(var_part_name), font = ('Pursia', 9,'bold'), justify = tk.LEFT, anchor = 'w')
		

	def scroll(self, plist):	

			i=1
			pname = tk.StringVar()
			buttons = [] 

			self.canvas = tk.Canvas(self.online_Frame, borderwidth=0, width = 150, height = 303)
			self.frame = tk.Frame(self.canvas)
			
			self.vsb = tk.Scrollbar(self.online_Frame, orient="vertical", command=self.canvas.yview)
			self.canvas.configure(yscrollcommand=self.vsb.set)
			self.vsb.grid(row = 0 , column = 5, rowspan = 10, sticky = "nsew")

			# # self.canvas.xview_moveto(0)
			# self.hsb = tk.Scrollbar(self.online_Frame, orient="horizontal", command=self.canvas.xview)
			# self.canvas.configure(xscrollcommand=self.hsb.set)
			# self.hsb.grid(row = 9 , column = 0, rowspan = 1, sticky = "nsew", columnspan = 7)

			self.canvas.grid(row = 0 , column = 0, rowspan = 10, sticky = 'w', columnspan = 5)
			self.canvas.create_window((5,15), window=self.frame, anchor="nw",  tags="self.frame")
			self.frame.bind("<Configure>", lambda event, canvas=self.canvas: onFrameConfigure(self.canvas))
			
			files = plist
			for f in files:
				b = tk.Radiobutton(self.frame, text=' ' + str(f), variable = pname, anchor='w', value = f, indicatoron=0, relief = "ridge", width= 25, justify = "left")
				b['command'] = lambda: self.text_on_canvas(pname)
				b.grid(row=i, padx = 2, ipadx = 10, ipady = 2, sticky = "w")
				buttons.append(b)
				i+=1

	def add(self):
		global part_names_list
		global part_names_path
		pname = self.part_name.get()
		if (pname != '') and (pname not in part_names_list):
			part_names_list.append(pname)
			part_names_list = sorted(part_names_list)
			write_to_csv(part_names_list, part_names_path)
			self.scroll(part_names_list)
			tkmb.showinfo('SUCCESS', 'New part name (' + pname + ') added to the database.')
		elif (pname == ''):
			tkmb.showerror('ERROR', 'Empty field!')
		else:
			tkmb.showerror('ERROR', 'Part name already exists!')

	def delete(self):
		global var_part_name
		global part_names_list
		global part_names_path

		if(var_part_name != ''):
			result = tkmb.askquestion('Delete', 'Delete '+ str(var_part_name) + ' ?', icon = 'warning')
			if(result=='yes'):
				self.pname_canvas.delete("all")
				with open(part_names_path, 'wb') as f:
					writer = csv.writer(f)
					for p in part_names_list:
						if p != var_part_name:
							writer.writerow([p])
				f.close()

				part_names_list = prepare_list(part_names_path)
				part_names_list = sorted(part_names_list)
				self.scroll(part_names_list)
				var_part_name = ''
				
		else:
			tkmb.showerror('ERROR', 'Part name not selected!')



	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		
		self.gray_frame= tk.Frame(self, bg = "gray", width = 780,  height = 15)
		self.gray_frame.grid(row = 0, column = 1, columnspan = 25, pady = 0, padx = 0)
		# singing out
		self.logoutButton = tk.Button(self, foreground = 'red', cursor = "hand2", border = 3, justify = "right", relief = "flat" , text = 'Sign Out', font =("Verdana", 10))
		self.logoutButton["command"] = lambda: signout(self, controller)
		self.logoutButton.grid(row = 0, column = 18, padx = 0, pady = 0, ipadx = 1, ipady = 0)

		self.backButton = tk.Button(self, border = 2, text = 'Back', relief = "flat", cursor = "hand2", foreground = 'red', font =("Verdana", 10))
		self.backButton["command"] = lambda: back(self, controller)
		self.backButton.grid(row = 0, column = 15, padx = 10, pady = 0, ipadx = 1, ipady = 0)


		self.label1 = tk.Label(self, text="Part Name Master", font=LARGE_FONT)
		self.label1.grid(row = 0, column = 1,pady=15, padx= 20)

		self.entry_frame = tk.LabelFrame(self, border = 2, text = 'Add new Part Name')
		self.entry_frame.grid(row = 1, column = 1, padx = (75,2), pady = 18, rowspan = 5,ipadx = 3, ipady = 8, columnspan = 7)

		self.part_name_label = tk.Label(self.entry_frame, text = "Enter New Part Name:", justify = "left", anchor = 'w')
		self.part_name_label.grid(row = 3, column = 1, padx = 10, pady = 20)

		self.part_name = tk.StringVar()
		self.part_form = tk.Entry(self.entry_frame, width = 25, textvariable = self.part_name) # adds a textarea widget
		self.part_form.grid(row = 3, column = 2, padx = 20 ,pady = 10,columnspan = 4)

		self.addButton = tk.Button(self.entry_frame, border = 2, text = 'Add Part Name', relief = "groove")
		self.addButton["command"] = self.add
		self.addButton.grid(column = 2, row = 4, padx = 20, pady = 13, columnspan = 2,ipadx = 15, ipady = 3)

		self.modify_frame = tk.LabelFrame(self, border = 2, text = 'Delete Existing')
		self.modify_frame.grid(row = 6, column = 1, padx = (75,2), pady = 8, rowspan = 5,ipadx = 3, ipady = 13, columnspan = 6)

		self.part_name_label = tk.Label(self.modify_frame, text = 'Selected Part Name:', justify = "left", anchor = 'w')
		self.part_name_label.grid(row = 3, column = 1, padx = 10, pady = 20, ipadx = 15)

		self.pname_canvas = tk.Canvas(self.modify_frame, bg = "white", height = 18, width = 165)
		self.pname_canvas.grid(row = 3, column = 2, padx = 2, pady = 10,columnspan = 4)

		self.deleteButton = tk.Button(self.modify_frame, border = 2, text = 'Delete', relief = "groove")
		self.deleteButton["command"] = self.delete
		self.deleteButton.grid(column = 2, row = 4, padx = 6, pady = 3, columnspan = 2,ipadx = 35, ipady = 3)

		
		self.f = tk.Frame(self, bg = "red")
		self.f.grid(row = 15, column = 12, columnspan = 20, pady = 150, padx = 0, sticky = 's')
		logo_canvas = tk.Canvas(self.f, width = 120, height = 35, bg= "yellow")
		logo_canvas.grid(row = 20 , column = 10, columnspan= 15, padx = 0, pady = 0)
		logo_canvas.background = tk.PhotoImage(file = logo_path)
		logo_canvas.create_image(60, 18,image=logo_canvas.background)#,anchor='nw')

		self.online_Frame = tk.LabelFrame(self, border = 2, text = "Browse Part Names",  width = 260, height = 450)
		self.online_Frame.grid(row = 1, column = 15, padx = (4,7), pady = 15, columnspan = 5, rowspan = 11)

		self.scroll(part_names_list)


############################################# PROJECT MASTER ###################################################################
################################################################################################################################


class ProjectMaster(tk.Frame):
	def reset_fields(self):
		pass

	def text_on_canvas(self, pname):
		global var_project
		var_project = pname.get()
		self.pname_canvas.delete("all")
		self.pname_canvas.create_text(10, 10, text = str(var_project), font = ('Pursia', 9,'bold'), justify = tk.LEFT, anchor = 'w')
		

	def scroll(self, plist):	

		i=1
		pname = tk.StringVar()
		buttons = [] 

		self.canvas = tk.Canvas(self.online_Frame, borderwidth=0, width = 140, height = 303)
		self.frame = tk.Frame(self.canvas)
		
		self.vsb = tk.Scrollbar(self.online_Frame, orient="vertical", command=self.canvas.yview)
		self.canvas.configure(yscrollcommand=self.vsb.set)
		self.vsb.grid(row = 0 , column = 5, rowspan = 10, sticky = "nsew")

		# # self.canvas.xview_moveto(0)
		# self.hsb = tk.Scrollbar(self.online_Frame, orient="horizontal", command=self.canvas.xview)
		# self.canvas.configure(xscrollcommand=self.hsb.set)
		# self.hsb.grid(row = 9 , column = 0, rowspan = 1, sticky = "nsew", columnspan = 7)

		self.canvas.grid(row = 0 , column = 0, rowspan = 10, sticky = 'w', columnspan = 5)
		self.canvas.create_window((5,15), window=self.frame, anchor="nw",  tags="self.frame")
		self.frame.bind("<Configure>", lambda event, canvas=self.canvas: onFrameConfigure(self.canvas))
		
		files = plist
		for f in files:
			b = tk.Radiobutton(self.frame, text=' ' + str(f), variable = pname, anchor='w', value = f, indicatoron=0, relief = "ridge", width= 25, justify = "left")
			b['command'] = lambda: self.text_on_canvas(pname)
			b.grid(row=i, padx = 2, ipadx = 10, ipady = 2, sticky = "w")
			buttons.append(b)
			i+=1

	
	def add(self):
		global projects_list
		global projects_path
		pname = self.project_name.get()
		if (pname != '') and (pname not in projects_list):
			projects_list.append(pname)
			projects_list = sorted(projects_list)
			write_to_csv(projects_list, projects_path)
			self.scroll(projects_list)
			tkmb.showinfo('SUCCESS', 'New project (' + pname + ') added to the database.')
			
		elif (pname == ''):
			tkmb.showerror('ERROR', 'Empty field!')
		else:
			tkmb.showerror('ERROR', 'Project name already exists!')

	def delete(self):
		global var_project
		global projects_list
		global projects_path

		if(var_project != ''):
			result = tkmb.askquestion('Delete', 'Delete '+ str(var_project) + ' ?', icon = 'warning')
			if(result=='yes'):
				self.pname_canvas.delete("all")
				with open(projects_path, 'wb') as f:
					writer = csv.writer(f)
					for p in projects_list:
						if p != var_project:
							writer.writerow([p])
				f.close()

				projects_list = prepare_list(projects_path)
				projects_list = sorted(projects_list)
				self.scroll(projects_list)
				var_project = ''
				
		else:
			tkmb.showerror('ERROR', 'Project not selected!')
	

	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		
		self.gray_frame= tk.Frame(self, bg = "gray", width = 780,  height = 15)
		self.gray_frame.grid(row = 0, column = 1, columnspan = 25, pady = 0, padx = 0)
		# singing out
		self.logoutButton = tk.Button(self, foreground = 'red', cursor = "hand2", border = 3, justify = "right", relief = "flat" , text = 'Sign Out', font =("Verdana", 10))
		self.logoutButton["command"] = lambda: signout(self, controller)
		self.logoutButton.grid(row = 0, column = 18, padx = 0, pady = 0, ipadx = 1, ipady = 0)

		self.backButton = tk.Button(self, border = 2, text = 'Back', relief = "flat", cursor = "hand2", foreground = 'red', font =("Verdana", 10))
		self.backButton["command"] = lambda: back(self, controller)
		self.backButton.grid(row = 0, column = 15, padx = 10, pady = 0, ipadx = 1, ipady = 0)


		self.label1 = tk.Label(self, text="Project Master", font=LARGE_FONT)
		self.label1.grid(row = 0, column = 1,pady=15, padx= 20)

		self.entry_frame = tk.LabelFrame(self, border = 2, text = 'Add New Project Name')
		self.entry_frame.grid(row = 1, column = 1, padx = (75,2), pady = 18, rowspan = 5,ipadx = 3, ipady = 8, columnspan = 7)

		self.project_label = tk.Label(self.entry_frame, text = "Enter Project Name:", justify = "left", anchor = 'w')
		self.project_label.grid(row = 3, column = 1, padx = 10, pady = 20)

		self.project_name = tk.StringVar()
		self.project_form = tk.Entry(self.entry_frame, width = 25, textvariable = self.project_name) # adds a textarea widget
		self.project_form.grid(row = 3, column = 2, padx = 20 ,pady = 10,columnspan = 4)

		self.addButton = tk.Button(self.entry_frame, border = 2, text = 'Add Project', relief = "groove")
		self.addButton["command"] = self.add
		self.addButton.grid(column = 2, row = 4, padx = 20, pady = 13, columnspan = 2,ipadx = 15, ipady = 3)

		self.modify_frame = tk.LabelFrame(self, border = 2, text = 'Delete Existing')
		self.modify_frame.grid(row = 6, column = 1, padx = (85,2), pady = 8, rowspan = 5,ipadx = 3, ipady = 13, columnspan = 6)

		self.part_name_label = tk.Label(self.modify_frame, text = 'Selected Project:', justify = "left", anchor = 'w')
		self.part_name_label.grid(row = 3, column = 1, padx = 10, pady = 20, ipadx = 15)

		self.pname_canvas = tk.Canvas(self.modify_frame, bg = "white", height = 18, width = 178)
		self.pname_canvas.grid(row = 3, column = 2, padx = 2, pady = 10,columnspan = 4)

		self.deleteButton = tk.Button(self.modify_frame, border = 2, text = 'Delete', relief = "groove")
		self.deleteButton["command"] = self.delete
		self.deleteButton.grid(column = 2, row = 4, padx = 6, pady = 3, columnspan = 2,ipadx = 35, ipady = 3)

		
		self.f = tk.Frame(self, bg = "red")
		self.f.grid(row = 15, column = 12, columnspan = 20, pady = 150, padx = 0, sticky = 's')
		logo_canvas = tk.Canvas(self.f, width = 120, height = 35, bg= "yellow")
		logo_canvas.grid(row = 20 , column = 10, columnspan= 15, padx = 0, pady = 0)
		logo_canvas.background = tk.PhotoImage(file = logo_path)
		logo_canvas.create_image(60, 18,image=logo_canvas.background)#,anchor='nw')

		self.online_Frame = tk.LabelFrame(self, border = 2, text = "Browse Project Names",  width = 260, height = 450)
		self.online_Frame.grid(row = 1, column = 15, padx = (4,7), pady = 15, columnspan = 5, rowspan = 11)

		self.scroll(projects_list)


#################################################### VIEW PDFs ########################################################
#######################################################################################################################

def signout2(self, controller):
		global path_of_Online_folder
		files =next(walk(path_of_Online_folder))[2] #from os
		scroll(self, files)
		global current_user_category
		global current_user
		current_user_category = ''
		current_user = ''
		clear_canvas(self)
		controller.show_frame(LoginPage)

def  file_on_canvas(self, x):
	global path_of_Online_folder
	global selected_pdf_path
	global current_user_category
	selected_pdf = x.get()
	selected_pdf_path = path_of_Online_folder + "/" + str(selected_pdf)

	self.file_name_canvas.delete("all")
	self.file_name_canvas.create_text(10, 10, text = str(selected_pdf), font = ('Pursia', 9,'bold'), justify = tk.LEFT, anchor = 'w')
	
	# removing ".pdf" from the string
 	selected_pdf = selected_pdf.replace(' ', '')[:-4].upper()
	#splitting the string about "_" and stroing separated values in a list 
	split_string = selected_pdf.split("_")
	# declaring variables
	part_num = split_string[0]
	part_name = split_string[1]
	project = split_string[2]
	rev_num = split_string[3]
	rev_date = split_string[4]
	receipt_date = split_string[5]

	self.part_canvas.delete("all")
	self.part_canvas.create_text(10, 10, text = str(part_num), font = ('Pursia', 9,'bold'), justify = tk.LEFT, anchor = 'w')
	
	self.part_name_canvas.delete("all")
	self.part_name_canvas.create_text(10, 10, text = str(part_name), font = ('Pursia', 9,'bold'), justify = tk.LEFT, anchor = 'w')
	
	self.project_canvas.delete("all")
	self.project_canvas.create_text(10, 10, text = str(project), font = ('Pursia', 9,'bold'), justify = tk.LEFT, anchor = 'w')
	
	self.rev_num_canvas.delete("all")
	self.rev_num_canvas.create_text(10, 10, text = str(rev_num), font = ('Pursia', 9,'bold'), justify = tk.LEFT, anchor = 'w')
	
	self.rev_date_canvas.delete("all")
	self.rev_date_canvas.create_text(10, 10, text = str(rev_date), font = ('Pursia', 9,'bold'), justify = tk.LEFT, anchor = 'w')
	
	self.receipt_date_canvas.delete("all")
	self.receipt_date_canvas.create_text(10, 10, text = str(receipt_date), font = ('Pursia', 9,'bold'), justify = tk.LEFT, anchor = 'w')
	
def clear_canvas(self):
	self.pdf_name.set("")
	self.file_name_canvas.delete("all")
	self.part_canvas.delete("all")
	self.part_name_canvas.delete("all")
	self.project_canvas.delete("all")
	self.rev_date_canvas.delete("all")
	self.rev_num_canvas.delete("all")
	self.receipt_date_canvas.delete("all")
		
def search(self, to_search):
	key = to_search.get()
	global path_of_Online_folder
	search_list = next(walk(path_of_Online_folder))[2] #from os

	display_list = []
	for f in search_list:
		if (re.search(key.lower(), f.lower()) != None):
			display_list.append(f)

	scroll(self, display_list)

def scroll(self, files):
	global selected_pdf

	i=1
	buttons = [] 

	self.canvas = tk.Canvas(self.online_Frame, borderwidth=0, background="#ffffff", width = 200, height = 375)
	self.frame = tk.Frame(self.canvas, background="#ffffff")
	
	self.vsb = tk.Scrollbar(self.online_Frame, orient="vertical", command=self.canvas.yview)
	self.canvas.configure(yscrollcommand=self.vsb.set)
	self.vsb.grid(row = 0 , column = 55, rowspan = 20, columnspan = 2, sticky = "nsew")

	self.canvas.xview_moveto(0)
	self.hsb = tk.Scrollbar(self.online_Frame,width = 30, orient="horizontal", command=self.canvas.xview)
	self.canvas.configure(xscrollcommand=self.hsb.set)
	self.hsb.grid(row = 10 , column = 1, rowspan = 1, columnspan = 16, sticky = "nsew")

	self.canvas.grid(row = 1, column = 6, rowspan = 10, columnspan =20, sticky = 'w')
	self.canvas.create_window((5,15), window=self.frame, anchor="nw",  tags="self.frame")
	self.frame.bind("<Configure>", lambda event, canvas=self.canvas: onFrameConfigure(self.canvas))
	
	to_search = tk.StringVar()
	self.searchBox = tk.Entry(self.online_Frame, width = 25, border = 2, textvariable = to_search, relief = "groove", bg = "white")
	self.searchBox.grid(column = 6, row = 11, padx = 0, pady = 0, rowspan = 2,columnspan = 6,ipadx = 10, ipady = 3)
	self.searchButton = tk.Button(self.online_Frame, cursor = "hand2", width = 3, border = 2, text = "Go", relief = "groove", fg = "blue")
	self.searchButton["command"] = lambda: search(self, to_search)
	self.searchButton.grid(column = 16, row = 11, padx = 0, pady = 0, rowspan = 2,ipadx = 1, ipady = 2)

	for f in files:
		b = tk.Radiobutton(self.frame, text=' ' + str(f), variable = self.pdf_name, anchor='w', value = f, indicatoron=0, relief = "ridge", width= 50, justify = "left")
		b.grid(row=i, padx = 2, ipadx = 30, ipady = 2, sticky = "w")
		b['command'] = lambda: file_on_canvas(self, self.pdf_name)
		buttons.append(b)
		i+=1

def view(self):
	global current_user_category
	global selected_pdf_path
	
	if(selected_pdf_path !=''):
		Popen([selected_pdf_path], shell = True) #from subprocess
	else:
		tkmb.showerror("ERROR", "File not selected.")

def call_view_gui(self, controller):
		
		global current_user_category
		global path_of_Online_folder

		self.pdf_name = tk.StringVar()
		self.pdf_name.set("")

		self.gray_frame= tk.Frame(self, bg = "gray", width = 780,  height = 15)
		self.gray_frame.grid(row = 0, column = 1, columnspan = 25, pady = 0, padx = 0)
		
		self.logoutButton = tk.Button(self, foreground = 'red', cursor = "hand2", border = 3, justify = "right", relief = "flat" , text = 'Sign Out', font =("Verdana", 10))
		self.logoutButton["command"] = lambda: signout2(self, controller)
		self.logoutButton.grid(row = 0, column = 20, columnspan = 1, padx = 3, ipadx = 5, pady = 0, ipady = 0)

		self.entry_frame = tk.LabelFrame(self, border = 2, text = "File")
		self.entry_frame.grid(row = 1, column = 1, padx = (65,2), pady = 8, rowspan = 2,ipadx = 3, ipady = 3, columnspan = 7)

		self.file_name_label = tk.Label(self.entry_frame, text = 'Selected File:', justify = "left", anchor = 'w')
		self.file_name_label.grid(row = 1, column = 1, padx = 10, pady = 0, ipadx = 5)

		self.file_name_canvas = tk.Canvas(self.entry_frame, bg = "white", height = 24, width = 320)
		self.file_name_canvas.grid(row = 2, column = 1, padx = 2, pady = 5, columnspan = 6)

		self.label1 = tk.Label(self.entry_frame, text="PDF Details", font=LARGE_FONT)
		self.label1.grid(row = 0, column = 1,pady=15, padx= 20)

		self.part_label = tk.Label(self.entry_frame, text = "Part Number:", justify = "left")
		self.part_label.grid(row = 3, column = 1, padx = 10, pady = 10)

		self.part_canvas = tk.Canvas(self.entry_frame, bg = "white", height = 18, width = 160) # adds a textarea widget
		self.part_canvas.grid(row = 3, column = 2, padx = 20 ,pady = 10,columnspan = 4)

		self.part_name_label = tk.Label(self.entry_frame, text = "Part Name:", justify = "left")
		self.part_name_label.grid(row = 4, column = 1, padx = 10, pady = 10)

		self.part_name_canvas = tk.Canvas(self.entry_frame, bg = "white", height = 18, width = 160) # adds a textarea widget
		self.part_name_canvas.grid(row = 4, column = 2, padx = 20 ,pady = 10,columnspan = 4)

		self.project_label = tk.Label(self.entry_frame, text = " Project:", justify = "left")
		self.project_label.grid(row = 5, column = 1, padx = 10, pady = 10, ipadx = 5)

		self.project_canvas = tk.Canvas(self.entry_frame, bg = "white", height = 18, width = 160) # adds a textarea widget
		self.project_canvas.grid(row = 5, column = 2, padx = 20 ,pady = 10,columnspan = 4)
		
		self.rev_num_label = tk.Label(self.entry_frame, text = "Drawing Revision Number:", justify ="left")
		self.rev_num_label.grid(row = 6, column = 0, ipadx = 5, padx = 10, pady = 10, columnspan = 2)

		self.rev_num_canvas = tk.Canvas(self.entry_frame, bg = "white", height = 18, width = 160)
		self.rev_num_canvas.grid(row = 6, column = 2, padx = 5, pady = 10,columnspan = 4)
		
		self.rev_date_label = tk.Label(self.entry_frame, text = "Drawing Revision Date:", justify = "left")
		self.rev_date_label.grid(row = 7, column = 0, padx = 5, pady = 10, columnspan = 2)

		self.rev_date_canvas = tk.Canvas(self.entry_frame, bg = "white", height = 18, width = 160)
		self.rev_date_canvas.grid(row = 7, column = 2, padx = 5, pady = 10,columnspan = 4)

		self.date_label = tk.Label(self.entry_frame, text = "Receipt Date:", justify = "left")
		self.date_label.grid(row = 8, column = 1, padx = 10, pady = 10)

		self.receipt_date_canvas = tk.Canvas(self.entry_frame, bg = "white", height = 18, width = 160)
		self.receipt_date_canvas.grid(row = 8, column = 2, padx = 5, pady = 10,columnspan = 4)

		self.f = tk.Frame(self, bg = "red")
		self.f.grid(row = 10, column = 12, columnspan = 10, pady = 3, padx = 0)
		logo_canvas = tk.Canvas(self.f, width = 120, height = 35, bg= "yellow")
		logo_canvas.grid(row = 10, column = 3, columnspan= 5, padx = 0, pady = 0)
		logo_canvas.background = tk.PhotoImage(file=logo_path)
		logo_canvas.create_image(60, 18,image=logo_canvas.background)#,anchor='nw')


		self.online_Frame = tk.LabelFrame(self, border = 2, text = "Browse Online",  width = 250, height = 385)
		self.online_Frame.grid(row = 1, column = 8, padx = 5, pady = 25, columnspan = 16)

		files =next(walk(path_of_Online_folder))[2] #from os
		scroll(self, files)

class View_PDF_Admin(tk.Frame):	

	def reset_fields(self):
		files =next(walk(path_of_Online_folder))[2]
		scroll(self, files)
		
	def back(self, controller):
		clear_canvas(self)
		controller.show_frame(Admin_Page)

	def __init__(self, parent, controller):

		tk.Frame.__init__(self, parent)
		call_view_gui(self, controller)
		
		self.backButton = tk.Button(self, border = 2, text = 'Back', relief = "flat", cursor = "hand2", foreground = 'red', font =("Verdana", 10))
		self.backButton["command"] = lambda: self.back(controller)
		self.backButton.grid(row = 0, column = 1, padx = 10, pady = 0, ipadx = 1, ipady = 0)

		self.viewButton = tk.Button(self.entry_frame, border = 2, text = 'Open PDF', relief = "groove", foreground ="blue")
		self.viewButton["command"] = lambda:view(self)
		self.viewButton.grid(column = 2, row = 15, padx = 16, pady = 3, rowspan = 2,ipadx = 20, ipady = 3)

class View_PDF_Viewer(tk.Frame):
	def reset_fields(self):
		files =next(walk(path_of_Online_folder))[2]
		scroll(self, files)
	
	def back(self, controller):
		clear_canvas(self)
		controller.show_frame(Viewer_Page)	
		
	def __init__(self, parent, controller):

		tk.Frame.__init__(self, parent)		
		call_view_gui(self, controller)

		self.backButton = tk.Button(self, border = 2, text = 'Back', relief = "flat", cursor = "hand2", foreground = 'red', font =("Verdana", 10))
		self.backButton["command"] = lambda: self.back(controller)
		self.backButton.grid(row = 0, column = 1, padx = 10, pady = 0, ipadx = 1, ipady = 0)

		self.viewButton = tk.Button(self.entry_frame, border = 2, text = 'Open PDF', relief = "groove", foreground ="blue")
		self.viewButton["command"] = lambda:view(self)
		self.viewButton.grid(column = 2, row = 15, padx = 16, pady = 3, rowspan = 2,ipadx = 20, ipady = 3)

class View_PDF_Restricted(tk.Frame):
	def reset_fields(self):
		files =next(walk(path_of_Online_folder))[2]
		scroll(self, files)	

	def back(self, controller):
		clear_canvas(self)
		controller.show_frame(Restricted_Page)
		
	def __init__(self, parent, controller):
		
		tk.Frame.__init__(self, parent)
		call_view_gui(self, controller)

		self.backButton = tk.Button(self, border = 2, text = 'Back', relief = "flat", cursor = "hand2", foreground = 'red', font =("Verdana", 10))
		self.backButton["command"] = lambda: self.back(controller)
		self.backButton.grid(row = 0, column = 1, padx = 10, pady = 0, ipadx = 1, ipady = 0)

		self.viewButton = tk.Button(self.entry_frame, border = 2, text = 'Open PDF', relief = "groove", foreground ="blue")
		self.viewButton.config(state = "disabled")
		self.viewButton["command"] = lambda:view(self)
		self.viewButton.grid(column = 2, row = 15, padx = 16, pady = 3, rowspan = 2,ipadx = 20, ipady = 3)


############################################ VIEWER PAGE ############################################################################################
#####################################################################################################################################################
def change_password_popup(self):
		self.w=password_change_popupWindow(self.master)
		self.master.wait_window(self.w.top)

def viewer_gui(self, controller):
	self.gray_frame= tk.Frame(self, bg = "gray", width = 780, pady = 0, padx = 0, height = 15)
	self.gray_frame.grid(row = 0, column = 0, columnspan = 18)
	
	label = tk.Label(self, text="Welcome User!", font=("Verdana", 10), justify = "right")
	label.grid(row = 0, column = 0, pady=10, padx=0, columnspan = 1)

	self.button_frame = tk.LabelFrame(self, border = 2, text = "Viewer Options")
	self.button_frame.grid(column = 0, row = 2, padx = 20, pady = 5, rowspan = 2,ipadx = 3, ipady = 3, columnspan = 5)

	self.change_pwrd = tk.Button(self.button_frame, border = 2, text = 'Change My Password', relief = "groove")
	self.change_pwrd["command"] = lambda: change_password_popup(self)
	self.change_pwrd.grid(column = 1, row = 1, padx = 5, pady = 5, rowspan = 2,ipadx = 10, ipady = 3)

	self.logoutButton = tk.Button(self, foreground = 'red', cursor = "hand2", border = 3, justify = "right", relief = "flat" , text = 'Sign Out', font =("Verdana", 10))
	self.logoutButton["command"] = lambda: controller.show_frame(LoginPage)
	self.logoutButton.grid(column = 12, row = 0, padx = 5, pady = 0, ipadx = 1, ipady = 0)

	self.f = tk.Frame(self, bg = "red")
	self.f.grid(row = 10, column = 1, columnspan = 15, pady = 50, padx = 10)
	logo_canvas = tk.Canvas(self.f, width = 370, height = 70, bg= "yellow")
	logo_canvas.grid(row = 10, column = 0, columnspan= 5, padx = 0, pady = 0)
	logo_canvas.background = tk.PhotoImage(file=logo2_path)
	logo_canvas.create_image(190,30,image=logo_canvas.background)#,anchor='nw')


class Viewer_Page(tk.Frame):
	def reset_fields(self):
		pass
	
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		viewer_gui(self, controller)
		#to open online PDFs
		self.viewer_page = tk.Button(self.button_frame, border = 2, text = 'PDF Viewer', relief = "groove")
		self.viewer_page["command"] = lambda: controller.show_frame(View_PDF_Viewer)
		self.viewer_page.grid(column = 0, row = 1, padx = 5, pady = 5, rowspan = 2,ipadx = 30, ipady = 3)

class Restricted_Page(tk.Frame):
	def reset_fields(self):
		pass
	
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		viewer_gui(self, controller)
		#to open online PDFs
		self.viewer_page = tk.Button(self.button_frame, border = 2, text = 'PDF Viewer', relief = "groove")
		self.viewer_page["command"] = lambda: controller.show_frame(View_PDF_Restricted)
		self.viewer_page.grid(column = 0, row = 1, padx = 5, pady = 5, rowspan = 2,ipadx = 30, ipady = 3)
	

#######################################################################################################################
#######################################################################################################################
			
app = Application()
app.maxsize(765,610)
app.maxsize(765,610)
app.mainloop()