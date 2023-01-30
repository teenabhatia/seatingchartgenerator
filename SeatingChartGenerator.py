from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import math
import mysql.connector
from PIL import ImageTk, Image
import pyautogui

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Rajesh@20",
    database="SeatingChartGenerator"
)

mycursor = mydb.cursor()


def start():
    my_w = Tk()
    my_w.title("All Student Records")
    my_w.configure(bg="#f4e9dc")

    # Adding style
    style = ttk.Style()
    style.configure("Treeview", background="#EFDDC9", foreground="#675951", rowheight=25, fieldbackground="#EFDDC9")

    # Create Treeview Frame
    tree_frame = Frame(my_w)
    tree_frame.pack(pady=20)

    # Treeview Scrollbar
    tree_scroll = Scrollbar(tree_frame)
    tree_scroll.pack(side=RIGHT, fill=Y)

    # Create Treeview
    trv = ttk.Treeview(tree_frame, selectmode='browse', yscrollcommand=tree_scroll.set)

    # Configure the scrollbar
    tree_scroll.config(command=trv.yview)

    # Add Menu
    my_menu = Menu(my_w)
    my_w.config(menu=my_menu)

    # number of columns
    trv["columns"] = ("1", "2", "3", "4", "5", "6", "7")

    # Defining heading
    trv['show'] = 'headings'

    # width of columns and alignment
    trv.column("1", width=190, anchor='c')
    trv.column("2", width=210, anchor='c')
    trv.column("3", width=210, anchor='c')
    trv.column("4", width=210, anchor='c')
    trv.column("5", width=210, anchor='c')
    trv.column("6", width=210, anchor='c')
    trv.column("7", width=210, anchor='c')

    # Headings
    # respective columns
    trv.heading("1", text="ID")
    trv.heading("2", text="Name")
    trv.heading("3", text="Completed Assignments")
    trv.heading("4", text="Test 1")
    trv.heading("5", text="Test 2")
    trv.heading("6", text="Attendance")
    trv.heading("7", text="Behaviour Rating")

    # Create striped row tags
    trv.tag_configure('oddrow', background="#f4e9dc")
    trv.tag_configure('evenrow', background="white")

    # getting data from MySQL student table
    mycursor.execute("SELECT * FROM Student")

    myresult = mycursor.fetchall()
    global count
    count = 0
    for dt in myresult:
        if count % 2 == 0:
            trv.insert("", 'end', iid=dt[0], text=dt[0],
                       values=(dt[0], dt[1], dt[2], dt[3], dt[4], dt[5], dt[6]), tags=('evenrow',))
        else:
            trv.insert("", 'end', iid=dt[0], text=dt[0],
                       values=(dt[0], dt[1], dt[2], dt[3], dt[4], dt[5], dt[6]), tags=('oddrow',))
        count += 1
    trv.pack()

    frame = Frame(my_w, bg="#f4e9dc")
    frame.pack(pady=20)

    # labels
    student_id = Label(frame, text="Student ID", fg="#675951", borderwidth=3, relief="ridge", padx=58)
    student_id.grid(row=1, column=0)

    student_name = Label(frame, text="Student Name", fg="#675951", borderwidth=3, relief="ridge", padx=45)
    student_name.grid(row=1, column=1)

    compl_assignments = Label(frame, text="Completed assignments", fg="#675951", borderwidth=3, relief="ridge", padx=17)
    compl_assignments.grid(row=1, column=2)

    test_1 = Label(frame, text="Test 1", fg="#675951", borderwidth=3, relief="ridge", padx=65)
    test_1.grid(row=1, column=3)

    test_2 = Label(frame, text="Test 2", fg="#675951", borderwidth=3, relief="ridge", padx=65)
    test_2.grid(row=1, column=4)

    attendance = Label(frame, text="Attendance %", fg="#675951", borderwidth=3, relief="ridge", padx=45)
    attendance.grid(row=1, column=5)

    behaviour = Label(frame, text="Behaviour Rating", fg="#675951", borderwidth=3, relief="ridge", padx=40)
    behaviour.grid(row=1, column=6)

    # Entry boxes
    studentid_entry = Entry(frame, fg="#675951", borderwidth=3, relief="sunken")
    studentid_entry.grid(row=2, column=0)

    studentname_entry = Entry(frame, fg="#675951", borderwidth=3, relief="sunken")
    studentname_entry.grid(row=2, column=1)

    compl_assignments_entry = Entry(frame, fg="#675951", borderwidth=3, relief="sunken")
    compl_assignments_entry.grid(row=2, column=2)

    test_1_entry = Entry(frame, fg="#675951", borderwidth=3, relief="sunken")
    test_1_entry.grid(row=2, column=3)

    test_2_entry = Entry(frame, fg="#675951", borderwidth=3, relief="sunken")
    test_2_entry.grid(row=2, column=4)

    attendance_entry = Entry(frame, fg="#675951", borderwidth=3, relief="sunken")
    attendance_entry.grid(row=2, column=5)

    behaviour_entry = Entry(frame, fg="#675951", borderwidth=3, relief="sunken")
    behaviour_entry.grid(row=2, column=6)

    def clear_entries():
        studentid_entry.delete(0, END)
        studentname_entry.delete(0, END)
        compl_assignments_entry.delete(0, END)
        test_1_entry.delete(0, END)
        test_2_entry.delete(0, END)
        attendance_entry.delete(0, END)
        behaviour_entry.delete(0, END)

    def query_database():
        # Clear the Treeview
        for record in trv.get_children():
            trv.delete(record)
        # getting data from MySQL student table
        mycursor.execute("SELECT * FROM Student")
        myresult = mycursor.fetchall()
        global count
        count = 0
        for dt in myresult:
            if count % 2 == 0:
                trv.insert("", 'end', iid=dt[0], text=dt[0],
                           values=(dt[0], dt[1], dt[2], dt[3], dt[4], dt[5], dt[6]), tags=('evenrow',))
            else:
                trv.insert("", 'end', iid=dt[0], text=dt[0],
                           values=(dt[0], dt[1], dt[2], dt[3], dt[4], dt[5], dt[6]), tags=('oddrow',))
            count += 1
        trv.pack()

    def search_records():
        lookup_record = search_entry.get()
        # close the search box
        search.destroy()

        # Clear the Treeview
        for record in trv.get_children():
            trv.delete(record)

        choice = v.get()

        if choice == 1:
            sql = "SELECT * FROM Student WHERE StudentName LIKE '" + lookup_record + "'"
        else:
            sql = "SELECT * FROM Student WHERE StudentID = '" + lookup_record + "'"
        mycursor.execute(sql, lookup_record)
        records = mycursor.fetchall()

        # Add data to the screen
        global count
        count = 0

        for record in records:
            if count % 2 == 0:
                trv.insert(parent='', index='end', iid=record[0], text=record[0],
                           values=(record[0], record[1], record[2], record[3], record[4], record[5], record[6]),
                           tags=('evenrow',))
            else:
                trv.insert(parent='', index='end', iid=record[0], text=record[0],
                           values=(record[0], record[1], record[2], record[3], record[4], record[5], record[6]),
                           tags=('oddrow',))
            count += 1

        mydb.commit()

    def lookup_records():
        global search_entry, search, v

        search = Toplevel(root)
        search.title("Lookup Records")
        search.geometry("400x200")

        # Create label frame
        search_frame = LabelFrame(search, text="How do you want to search?")
        search_frame.pack(padx=10, pady=10)

        v = IntVar()

        searchName = Radiobutton(search_frame, text="By Name", padx=20, variable=v, value=1)
        searchName.pack(anchor=W)

        searchID = Radiobutton(search_frame, text="By Student ID", padx=20, variable=v, value=2)
        searchID.pack(anchor=W)

        search_entry = Entry(search_frame, font=("Helvetica", 18))
        search_entry.pack(pady=20, padx=20)

        search_button = Button(search, text="Search Records", command=search_records, borderwidth=3, relief="ridge",
                               font=("Helvetica", 13))
        search_button.pack(padx=5, pady=5)

    # Search Menu
    search_menu = Menu(my_menu, tearoff=0)
    my_menu.add_cascade(label="Search", menu=search_menu)
    # Drop down menu
    search_menu.add_command(label="Search", command=lookup_records)
    search_menu.add_separator()
    search_menu.add_command(label="Reset", command=query_database)

    # Select Record
    def edit_record():
        # clear entry boxes
        clear_entries()

        # grab record
        selected = trv.focus()
        # grab record values
        values = trv.item(selected, 'values')
        # temp_label.config(text=selected)

        # output to entry boxes
        studentid_entry.insert(0, values[0])
        studentname_entry.insert(0, values[1])
        compl_assignments_entry.insert(0, values[2])
        test_1_entry.insert(0, values[3])
        test_2_entry.insert(0, values[4])
        attendance_entry.insert(0, values[5])
        behaviour_entry.insert(0, values[6])

    def update_record():
        # Update single record
        selected = trv.focus()
        sql = "UPDATE Student SET StudentName = %s, Compl = %s, Test_1 = %s, Test_2 = %s, Attendance = %s, Behaviour = %s WHERE StudentID = %s"
        val = (studentname_entry.get(), compl_assignments_entry.get(), test_1_entry.get(), test_2_entry.get(),
               attendance_entry.get(), behaviour_entry.get(), studentid_entry.get())
        mycursor.execute(sql, val)

        mydb.commit()
        trv.item(selected, text="",
                 values=(
                     studentid_entry.get(), studentname_entry.get(), compl_assignments_entry.get(), test_1_entry.get(),
                     test_2_entry.get(), attendance_entry.get(), behaviour_entry.get()))

        clear_entries()

        print(mycursor.rowcount, "record(s) affected")

    # delete one Record
    def delete_record():
        selected = trv.focus()
        selected_item = str(trv.selection()[0])
        trv.item(selected, text="", values=(
            studentid_entry.get(), studentname_entry.get(), compl_assignments_entry.get(), test_1_entry.get(),
            test_2_entry.get(), attendance_entry.get(), behaviour_entry.get()))

        mycursor.execute("DELETE FROM Student WHERE StudentID=%s", (selected_item,))
        mydb.commit()

        print(mycursor.rowcount, "record deleted.")
        messagebox.showinfo("Alert", "Record Deleted.")

    def input_record():
        global count

        if len(studentid_entry.get()) == 0 or len(studentname_entry.get()) == 0 or len(
                compl_assignments_entry.get()) == 0 or len(test_1_entry.get()) == 0 or len(
            test_2_entry.get()) == 0 or len(attendance_entry.get()) == 0 or len(behaviour_entry.get()) == 0:
            messagebox.showinfo("Alert", "Please enter all values.")
        try:
            float(studentid_entry.get())  # Tries to convert the value to a float.
        except ValueError:
            messagebox.showinfo("Alert", "Wrong Value Entered. Please recheck.")

        val = (studentid_entry.get(), studentname_entry.get(), compl_assignments_entry.get(), test_1_entry.get(),
               test_2_entry.get(), attendance_entry.get(), behaviour_entry.get())

        sql = "INSERT INTO Student (StudentID, StudentName, Compl, Test_1, Test_2, Attendance, Behaviour) VALUES (%s, %s, %s, %s, %s, %s, %s)"

        mycursor.execute(sql, val)

        mydb.commit()

        print(mycursor.rowcount, "record inserted.")
        trv.insert(parent='', index='end', text='',
                   values=(
                       studentid_entry.get(), studentname_entry.get(), compl_assignments_entry.get(),
                       test_1_entry.get(),
                       test_2_entry.get(), attendance_entry.get(), behaviour_entry.get()))

        clear_entries()

    def show_record():
        my_w = Tk()
        my_w.title("All Student Records")
        # Using treeview widget
        trv = ttk.Treeview(my_w, selectmode='browse')

        trv.grid(row=1, column=1, padx=20, pady=20)
        # number of columns
        trv["columns"] = ("1", "2", "3", "4", "5", "6", "7")

        # Defining heading
        trv['show'] = 'headings'

        # width of columns and alignment
        trv.column("1", width=30, anchor='c')
        trv.column("2", width=120, anchor='c')
        trv.column("3", width=120, anchor='c')
        trv.column("4", width=120, anchor='c')
        trv.column("5", width=120, anchor='c')
        trv.column("6", width=120, anchor='c')
        trv.column("7", width=120, anchor='c')

        # Headings
        # respective columns
        trv.heading("1", text="Student ID")
        trv.heading("2", text="Name")
        trv.heading("3", text="Completed Assignments")
        trv.heading("4", text="Test 1")
        trv.heading("5", text="Test 2")
        trv.heading("6", text="Attendance")
        trv.heading("7", text="Behaviour Rating")

        # getting data from MySQL student table
        mycursor.execute("SELECT * FROM Student")
        myresult = mycursor.fetchall()
        for dt in myresult:
            trv.insert("", 'end', iid=dt[0], text=dt[0],
                       values=(dt[0], dt[1], dt[2], dt[3], dt[4], dt[5], dt[6]))
        my_w.mainloop()

    def weighted_scores():
        global scores_names
        mycursor = mydb.cursor()
        sql = "SELECT Compl from Student"
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        mylist = [row[0] for row in myresult]

        # Calculate percentage of assignments completed
        assignments_completed = []
        for x in range(len(mylist)):
            assignments_completed.append(int(mylist[x]) / 15)

        sql = "SELECT Attendance from Student"
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        mylist1 = [row[0] for row in myresult]
        # Percent of school days attended
        attendance = []
        for x in range(len(mylist1)):
            attendance.append(int(mylist1[x]) / 100)

        sql = "SELECT Behaviour from Student"
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        mylist2 = [row[0] for row in myresult]
        # Monthly class behaviour rating
        behaviour = []
        for x in range(len(mylist2)):
            class_behaviour = int(mylist2[x]) / 10
            behaviour.append(class_behaviour)

        sql = "SELECT Test_1 from Student"
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        mylist3 = [row[0] for row in myresult]

        sql = "SELECT Test_2 from Student"
        mycursor.execute(sql)
        myresult1 = mycursor.fetchall()
        mylist4 = [row[0] for row in myresult1]

        # Calculate average of best 2 tests
        best_two_tests = []
        for x in range(len(mylist3)):
            avg = (mylist3[x] + mylist4[x]) / 2
            avg = (avg / 20)
            best_two_tests.append(avg)

        # Calculated the weighted score out of 1
        # Assignments Completed = 15%
        # Attendance = 20%
        # Best Two Tests = 35%
        # Monthly Class Behaviour = 30%
        weighted_scores = []
        for i in range(0, len(behaviour)):
            final_score = assignments_completed[i] * 0.15 + attendance[i] * 0.2 + best_two_tests[i] * 0.35 + behaviour[
                i] * 0.3
            final_score = round(final_score, 2)
            weighted_scores.append(final_score)

        # Names
        sql = "SELECT StudentName from Student"
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        names = [row[0] for row in myresult]

        scores_names = []
        for x in range(len(names)):
            scores_names.append([weighted_scores[x], names[x]])

        scores_names.sort()

        global new_w

        new_w = Tk()
        new_w.title("Student Weighted Records")
        # Using treeview widget
        trv = ttk.Treeview(new_w, selectmode='browse')

        trv.grid(row=1, column=1, padx=20, pady=20)
        # number of columns
        trv["columns"] = ("1", "2", "3")

        # Defining heading
        trv['show'] = 'headings'

        # width of columns and alignment
        trv.column("1", width=120, anchor='c')
        trv.column("2", width=140, anchor='c')
        trv.column("3", width=120, anchor='c')

        # Headings
        # respective columns
        trv.heading("1", text="Student ID")
        trv.heading("2", text="Name")
        trv.heading("3", text="Weighted Score")

        # getting data from MySQL student table
        mycursor.execute("SELECT StudentID, StudentName FROM Student")
        myresult = mycursor.fetchall()
        count = 0
        for dt in myresult:
            trv.insert("", 'end', iid=dt[0], text=dt[0], values=(dt[0], dt[1], weighted_scores[count]))
            count += 1

        new_w.mainloop()

    def find_rows_cols(num):
        cr = math.sqrt(num)
        if isinstance(cr, int) == True:
            col = cr
            row = cr
            return col, row
        else:
            cr = math.ceil(cr)
            col = cr
            row = cr
            return col, row

    global new_window

    def screenshot():
        myScreenshot = pyautogui.screenshot(region=(790, 52, 1400, 700))

        file_path = filedialog.asksaveasfilename(defaultextension='.png')

        myScreenshot.save(file_path)

    def generate():
        generate_new = Tk()
        generate_new.title("Choose division")
        text = Label(generate_new, text="Divide students into groups of: ", pady=10, font=("Calibri", 20))
        text.grid(row=0,
                  column=0, padx=10)
        options = ["2", "3", "4"]

        # datatype of menu text
        entry = StringVar()
        # initial menu text
        entry.set("2")

        drop = OptionMenu(generate_new, entry, *options)
        drop.grid(row=1, column=0, padx=10)

        def calculate():
            generate_new.destroy()
            groupSize = int(entry.get())

            if groupSize == 2:
                new_window = Toplevel()
                new_window.geometry("1280x800")
                new_window.title("Seating Chart")
                pairs = []
                length = len(scores_names)
                label = Label(new_window, text="Front of class", justify="center")
                label.pack()
                seatLayout = Canvas(new_window)
                seatLayout.pack()
                save_button = Button(new_window, text='Save', command=screenshot, borderwidth=3,
                                     relief="ridge",
                                     padx=35,
                                     pady=10)
                save_button.pack(side=BOTTOM)

                col, row = find_rows_cols(length)

                if length % 2 == 0:
                    for x in range(length // 2):
                        pairs.append((scores_names[x], scores_names[length - 1]))
                        length -= 1
                    count = 0
                    while count != length - 1:
                        for x in range(2, col):
                            for y in range(2, row):
                                seatMaker = Button(seatLayout, text='%s\n%s' % (pairs[count][0][1], pairs[count][1][1]))
                                # Making the actual grid
                                seatLayout.grid_rowconfigure(x, weight=1)
                                seatLayout.grid_columnconfigure(y, weight=1)
                                seatMaker.grid(row=x, column=y, sticky=N + S + E + W, padx=10, pady=10)
                                count += 1
                else:
                    temp = scores_names[(length - 1) // 2]
                    scores_names.pop((length - 1) // 2)
                    length = len(scores_names)
                    for x in range(length // 2):
                        pairs.append([scores_names[x], scores_names[length - 1]])
                        length -= 1
                    pairs[0] = pairs[0] + [temp]

                    seatMaker = Button(seatLayout,
                                       text='%s\n%s\n%s' % (pairs[0][0][1], pairs[0][1][1], pairs[0][2][1]))
                    seatLayout.grid_rowconfigure(row - 1, weight=1)
                    seatLayout.grid_columnconfigure(col - 1, weight=1)
                    seatMaker.grid(row=row - 1, column=col - 1, sticky=N + S + E + W, padx=10, pady=10)
                    count = 1
                    while count != length - 1:
                        for x in range(2, col):
                            for y in range(2, row):
                                seatMaker = Button(seatLayout, text='%s\n%s' % (pairs[count][0][1], pairs[count][1][1]))
                                # Making the actual grid
                                seatLayout.grid_rowconfigure(x, weight=1)
                                seatLayout.grid_columnconfigure(y, weight=1)
                                seatMaker.grid(row=x, column=y, sticky=N + S + E + W, padx=10, pady=10)
                                count += 1
                new_window.mainloop()
            elif groupSize == 3:
                new_window = Toplevel()
                new_window.geometry("1280x800")
                new_window.title("Seating Chart")
                triples = []
                length = len(scores_names)
                label = Label(new_window, text="Front of class", justify="center")
                label.pack()
                seatLayout = Canvas(new_window)
                seatLayout.pack()
                save_button = Button(new_window, text='Save', command=screenshot, borderwidth=3,
                                     relief="ridge",
                                     padx=35,
                                     pady=10)
                save_button.pack(side=BOTTOM)
                col, row = find_rows_cols(length)
                if length % 3 == 0:
                    for x in range(length // 3):
                        triples.append((scores_names[x], scores_names[length - 2], scores_names[length - 1]))
                        length -= 2
                    count = 0
                    while count != length - 1:
                        for x in range(2, col):
                            for y in range(2, row):
                                seatMaker = Button(seatLayout, text='%s\n%s\n%s' % (
                                    triples[count][0][1], triples[count][1][1], triples[count][2][1]))
                                # Making the actual grid
                                seatLayout.grid_rowconfigure(x, weight=1)
                                seatLayout.grid_columnconfigure(y, weight=1)
                                seatMaker.grid(row=x, column=y, sticky=N + S + E + W, padx=10, pady=10)
                                count += 1
                elif length % 3 == 1:
                    temp = scores_names[(length - 1) // 2]
                    scores_names.pop((length - 1) // 2)
                    length = len(scores_names)
                    for x in range(length // 3):
                        triples.append([scores_names[x], scores_names[length - 2], scores_names[length - 1]])
                        length -= 2
                    triples[0] = triples[0] + [temp]
                    seatMaker = Button(seatLayout,
                                       text='%s\n%s\n%s\n%s' % (
                                           triples[0][0][1], triples[0][1][1], triples[0][2][1], triples[0][3][1]))
                    seatLayout.grid_rowconfigure(row - 1, weight=1)
                    seatLayout.grid_columnconfigure(col - 1, weight=1)
                    seatMaker.grid(row=row - 2, column=col - 2, sticky=N + S + E + W, padx=10, pady=10)
                    count = 1
                    while count != length - 1:
                        for x in range(2, col):
                            for y in range(2, row):
                                seatMaker = Button(seatLayout, text='%s\n%s\n%s' % (
                                    triples[count][0][1], triples[count][1][1], triples[count][2][1]))
                                # Making the actual grid
                                seatLayout.grid_rowconfigure(x, weight=1)
                                seatLayout.grid_columnconfigure(y, weight=1)
                                seatMaker.grid(row=x, column=y, sticky=N + S + E + W, padx=10, pady=10)
                                count += 1
                else:
                    index = (length - 1) // 2
                    temp, temp1 = scores_names[index], scores_names[index + 1]
                    scores_names.pop(index)
                    scores_names.pop(index + 1)
                    length = len(scores_names)
                    for x in range(length // 3):
                        triples.append([scores_names[x], scores_names[length - 2], scores_names[length - 1]])
                        length -= 2
                    triples.append([temp, temp1])
                    seatMaker = Button(seatLayout,
                                       text='%s\n%s' % (
                                           triples[len(triples) - 1][0][1], triples[len(triples) - 1][1][1]))
                    seatLayout.grid_rowconfigure(row - 1, weight=1)
                    seatLayout.grid_columnconfigure(col - 1, weight=1)
                    seatMaker.grid(row=row - 2, column=col - 2, sticky=N + S + E + W, padx=10, pady=10)
                    count = 0
                    while count != length - 1:
                        for x in range(2, col):
                            for y in range(2, row):
                                seatMaker = Button(seatLayout,
                                                   text='%s\n%s\n%s' % (
                                                       triples[count][0][1], triples[count][1][1],
                                                       triples[count][2][1]))
                                # Making the actual grid
                                seatLayout.grid_rowconfigure(x, weight=1)
                                seatLayout.grid_columnconfigure(y, weight=1)
                                seatMaker.grid(row=x, column=y, sticky=N + S + E + W, padx=10, pady=10)
                                count += 1

                for x in range(len(triples)):
                    print(triples[x])
                new_window.mainloop()
            elif groupSize == 4:
                new_window = Toplevel()
                new_window.geometry("1280x800")
                new_window.title("Seating Chart")
                quadruple = []
                length = len(scores_names)
                label = Label(new_window, text="Front of class", justify="center")
                label.pack()
                seatLayout = Canvas(new_window)
                seatLayout.pack()
                save_button = Button(new_window, text='Save', command=screenshot, borderwidth=3,
                                     relief="ridge",
                                     padx=35,
                                     pady=10)
                save_button.pack(side=BOTTOM)
                col, row = find_rows_cols(length)

                if length % 4 == 0:
                    for x in range(length // 4):
                        quadruple.append(
                            (scores_names[x], scores_names[length - 3], scores_names[length - 2],
                             scores_names[length - 1]))
                        length -= 3
                    count = 0
                    while count != length - 1:
                        for x in range(2, col):
                            for y in range(2, row):
                                seatMaker = Button(seatLayout, text='%s\n%s\n%s\n%s' % (
                                    quadruple[count][0][1], quadruple[count][1][1], quadruple[count][2][1],
                                    quadruple[count][3][1]))
                                # this part just makes the grid itself
                                seatLayout.grid_rowconfigure(x, weight=1)
                                seatLayout.grid_columnconfigure(y, weight=1)
                                seatMaker.grid(row=x, column=y, sticky=N + S + E + W, padx=10, pady=10)
                                count += 1
                elif length % 4 == 1:
                    temp = scores_names[(length - 1) // 2]
                    scores_names.pop((length - 1) // 2)
                    length = len(scores_names)
                    for x in range(length // 4):
                        quadruple.append(
                            [scores_names[x], scores_names[length - 3], scores_names[length - 2],
                             scores_names[length - 1]])
                        length -= 3
                    quadruple[0] = quadruple[0] + [temp]

                    seatMaker = Button(seatLayout,
                                       text='%s\n%s\n%s\n%s\n%s' % (
                                           quadruple[0][0][1], quadruple[0][1][1], quadruple[0][2][1],
                                           quadruple[0][3][1],
                                           quadruple[0][4][1]))
                    seatLayout.grid_rowconfigure(row - 3, weight=1)
                    seatLayout.grid_columnconfigure(col - 2, weight=1)
                    seatMaker.grid(row=row - 3, column=col - 2, sticky=N + S + E + W, padx=10, pady=10)
                    count = 1
                    while count != length - 1:
                        for x in range(2, col):
                            for y in range(2, row):
                                seatMaker = Button(seatLayout, text='%s\n%s\n%s\n%s' % (
                                    quadruple[count][0][1], quadruple[count][1][1], quadruple[count][2][1],
                                    quadruple[count][3][1]))
                                # Making the actual grid
                                seatLayout.grid_rowconfigure(x, weight=1)
                                seatLayout.grid_columnconfigure(y, weight=1)
                                seatMaker.grid(row=x, column=y, sticky=N + S + E + W, padx=10, pady=10)
                                count += 1
                elif length % 4 == 2:
                    index = (length - 1) // 2
                    temp, temp1 = scores_names[index], scores_names[index + 1]
                    scores_names.pop(index)
                    scores_names.pop(index + 1)
                    length = len(scores_names)
                    for x in range(length // 4):
                        quadruple.append(
                            [scores_names[x], scores_names[length - 3], scores_names[length - 2],
                             scores_names[length - 1]])
                        length -= 3
                    quadruple[0] = quadruple[0] + [temp]
                    quadruple[1] = quadruple[1] + [temp1]

                    seatMaker = Button(seatLayout,
                                       text='%s\n%s\n%s\n%s\n%s' % (
                                           quadruple[0][0][1], quadruple[0][1][1], quadruple[0][2][1],
                                           quadruple[0][3][1],
                                           quadruple[0][4][1]))
                    seatLayout.grid_rowconfigure(row - 3, weight=1)
                    seatLayout.grid_columnconfigure(col - 1, weight=1)
                    seatMaker.grid(row=row - 3, column=col - 1, sticky=N + S + E + W, padx=10, pady=10)

                    seatMaker = Button(seatLayout,
                                       text='%s\n%s\n%s\n%s\n%s' % (
                                           quadruple[1][0][1], quadruple[1][1][1], quadruple[1][2][1],
                                           quadruple[1][3][1],
                                           quadruple[1][4][1]))
                    seatLayout.grid_rowconfigure(row - 3, weight=1)
                    seatLayout.grid_columnconfigure(col - 2, weight=1)
                    seatMaker.grid(row=row - 3, column=col - 2, sticky=N + S + E + W, padx=10, pady=10)
                    count = 2
                    while count != length - 1:
                        for x in range(2, col):
                            for y in range(2, row):
                                seatMaker = Button(seatLayout, text='%s\n%s\n%s\n%s' % (
                                    quadruple[count][0][1], quadruple[count][1][1], quadruple[count][2][1],
                                    quadruple[count][3][1]))
                                # Making the actual grid
                                seatLayout.grid_rowconfigure(x, weight=1)
                                seatLayout.grid_columnconfigure(y, weight=1)
                                seatMaker.grid(row=x, column=y, sticky=N + S + E + W, padx=10, pady=10)
                                count += 1
                elif length % 4 == 3:
                    index = (length - 1) // 2
                    temp, temp1, temp2 = scores_names[0], scores_names[index], scores_names[length - 1]
                    scores_names.pop(0)
                    scores_names.pop(index)
                    scores_names.pop(-1)
                    length = len(scores_names)
                    for x in range(length // 4):
                        quadruple.append(
                            [scores_names[x], scores_names[length - 3], scores_names[length - 2],
                             scores_names[length - 1]])
                        length -= 3
                    quadruple.append([temp, temp1, temp2])
                    print(quadruple)

                    seatMaker = Button(seatLayout,
                                       text='%s\n%s\n%s' % (
                                           quadruple[-1][0][1], quadruple[-1][1][1], quadruple[-1][2][1]))
                    seatLayout.grid_rowconfigure(row - 3, weight=1)
                    seatLayout.grid_columnconfigure(col - 1, weight=1)
                    seatMaker.grid(row=row - 3, column=col - 1, sticky=N + S + E + W, padx=10, pady=10)
                    count = 0
                    while count != length - 1:
                        for x in range(2, col):
                            for y in range(2, row):
                                seatMaker = Button(seatLayout, text='%s\n%s\n%s\n%s' % (
                                    quadruple[count][0][1], quadruple[count][1][1], quadruple[count][2][1],
                                    quadruple[count][3][1]))
                                # Making the actual grid
                                seatLayout.grid_rowconfigure(x, weight=1)
                                seatLayout.grid_columnconfigure(y, weight=1)
                                seatMaker.grid(row=x, column=y, sticky=N + S + E + W, padx=10, pady=10)
                                count += 1
                new_window.mainloop()

        calc = Button(generate_new, text="Generate", command=calculate, width=19, height=1, padx=10, pady=10,
                      font=("Calibri", 15))
        calc.grid(row=2,
                  column=0,
                  padx=5,
                  pady=5)

    def destroy():
        root.destroy()
        my_w.destroy()
        new_w.destroy()

    # Buttons
    frame_b = Frame(my_w, bg="#f4e9dc")
    frame_b.pack(pady=20)

    select_button = Button(frame_b, text="Update Record", fg="#675951", command=edit_record, borderwidth=3,
                           relief="ridge",
                           padx=25, pady=10)
    select_button.grid(row=0, column=0, padx=10, pady=10)

    update_button = Button(frame_b, text="Save Update", fg="#675951", command=update_record, borderwidth=3,
                           relief="ridge",
                           padx=32,
                           pady=10)
    update_button.grid(row=1, column=0, padx=10, pady=10)

    delete_button = Button(frame_b, text="Delete Record", fg="#675951", command=delete_record, borderwidth=3,
                           relief="ridge", padx=25,
                           pady=10)
    delete_button.grid(row=0, column=1, padx=10, pady=10)

    Input_button = Button(frame_b, text="Input Record", fg="#675951", command=input_record, borderwidth=3,
                          relief="ridge",
                          padx=30,
                          pady=10)
    Input_button.grid(row=1, column=1, padx=10, pady=10)

    show_scores = Button(frame_b, text="Refresh Weighted Scores", fg="#675951", command=weighted_scores, borderwidth=3,
                         relief="ridge",
                         padx=25, pady=10)
    show_scores.grid(row=0, column=2, padx=10, pady=10)

    generate_button = Button(frame_b, text="Generate Seating Chart", fg="#675951", command=generate, borderwidth=3,
                             relief="ridge",
                             padx=35,
                             pady=10)
    generate_button.grid(row=1, column=2, padx=10, pady=10)

    clear_button = Button(frame_b, text="Clear Entry Boxes", fg="#675951", command=clear_entries, borderwidth=3,
                          relief="ridge",
                          padx=35,
                          pady=10)
    clear_button.grid(row=2, column=1, padx=10, pady=10)

    destroy_button = Button(frame_b, text="Exit", fg="#675951", command=destroy, borderwidth=3,
                            relief="ridge",
                            padx=35,
                            pady=10)
    destroy_button.grid(row=2, column=2, padx=10, pady=10)

    my_w.mainloop()


root = Tk()
root.title("Seating Chart Generator: Login")

canvas = Canvas(root, width=300, height=300)


def showpassword():
    if var.get() == True:
        password_box.configure(show="")
    else:
        password_box.configure(show="*")


# Giving function to login process
login_completed = IntVar()


def login_user():
    global teacher
    user_id = username_box.get()
    pswrd = password_box.get()
    query = """ SELECT * FROM `Login` """
    mycursor.execute(query)
    result = mycursor.fetchall()
    temp = False
    for x in result:
        if user_id in x and pswrd in x:
            temp = True
            mycursor.execute("SELECT id FROM Login WHERE username=%s", (user_id,))
            teacher = mycursor.fetchall()

    if temp == True:
        root.withdraw()
        print("Successful Login", user_id)
        messagebox.showinfo(user_id, "Successful Login")

        window = Toplevel()
        window.title("Seating Chart Generator")
        window.minsize(450, 600)

        img = Image.open(
            "/Users/teenabhatia/Desktop/Grade_11/Computer_science/SeatingChartProgram/Artboard4@IAScreen.png")
        resized = img.resize((425, 300), Image.ANTIALIAS)
        new_img = ImageTk.PhotoImage(resized)
        my_label = Label(window, image=new_img)
        my_label.grid(row=0, column=3)
        bg = "#DCC1A0"
        welcome = Label(window, text="Welcome!", fg="#DCC1A0", width=50, height=2, padx=10, pady=10,
                        font=("Calibri", 40)).grid(row=3, column=3, padx=5, pady=10)
        input_students = Button(window, text="Click Here to Start", fg="#DCC1A0", width=30, height=2, command=start,
                                padx=10, pady=10,
                                font=("Calibri", 20)).grid(row=4, column=3, padx=5, pady=10)
        window.mainloop()
    else:
        messagebox.showwarning("Invalid", "Login Error")


def exit_login():
    msg = messagebox.askyesno("Exit login page", "Do you really want to exit?")
    if (msg):
        exit()


def mainloop_window():  # This is the class function that helps me to mainloop the window
    root.mainloop()


root.protocol("WM_DELETE_WINDOW", exit)
root.title("Login")
root.geometry("450x230+450+170")

message = Label(width="300", text="Please enter details below", bg="orange", fg="white").pack()
username = Label(root, text="Username:")
username.place(relx=0.285, rely=0.298, height=20, width=76)

password = Label(root, text="Password:")
password.place(relx=0.285, rely=0.468, height=20, width=80)

# Creating Buttons

login_button = Button(root, text="Login")
login_button.place(relx=0.440, rely=0.638, height=30, width=60)
login_button.configure(command=login_user)

exit_button = Button(root, text="Exit")  # , command=master.quit)
exit_button.place(relx=0.614, rely=0.638, height=30, width=60)
exit_button.configure(command=exit_login)

# Creating entry boxes

username_box = Entry(root)
username_box.place(relx=0.440, rely=0.298, height=20, relwidth=0.35)

password_box = Entry(root)
password_box.place(relx=0.440, rely=0.468, height=20, relwidth=0.35)
password_box.configure(show="*")
password_box.configure(background="white")

# Creating checkbox

var = IntVar()
show_password = Checkbutton(root)
show_password.place(relx=0.285, rely=0.650, relheight=0.100, relwidth=0.125)
show_password.configure(justify='left')
show_password.configure(text='''Show''')
show_password.configure(variable=var, command=showpassword)

root.mainloop()
