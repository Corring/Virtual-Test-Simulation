# Ning Yi, CIS 345, TUTH10:30, FinalProject
from difflib import get_close_matches
from tkinter import *
from tkinter import ttk, messagebox
import json
import random




class Question:
    """Has question text, 4 choices, correct answer number and formed question_list"""

    # correct is for xth is correct choice
    # question_list is formed format of the Question
    def __init__(self, question=''):
        self.__correct_feedback = ''
        self.__incorrect_feedback = ''
        self.__point_value = int()
        self.question = question
        self.__choice1 = ''
        self.__choice2 = ''
        self.__choice3 = ''
        self.__choice4 = ''
        self.__correct = int()
        self.__question_list = None

    # Get and Set the question
    @property
    def question(self):
        return self.__question

    @question.setter
    def question(self, question):
        self.__question = question

    # Set and get the first choice
    @property
    def choice1(self):
        return self.__choice1

    @choice1.setter
    def choice1(self, choice):
        self.__choice1 = choice

    # Set and get the second choice
    @property
    def choice2(self):
        return self.__choice2

    @choice2.setter
    def choice2(self, choice):
        self.__choice2 = choice

    # Set and get the third choice
    @property
    def choice3(self):
        return self.__choice3

    @choice3.setter
    def choice3(self, choice):
        self.__choice3 = choice

    # Set and get the forth choice
    @property
    def choice4(self):
        return self.__choice4

    @choice4.setter
    def choice4(self, choice):
        self.__choice4 = choice

    # Set and get the correct number of the question
    @property
    def correct(self):
        return self.__correct

    @correct.setter
    def correct(self, correct):
        self.__correct = correct

    # Getter of the question list
    @property
    def questionlist(self):
        return self.__question_list

    @property
    def correctfeedback(self):
        return self.__correct_feedback

    @correctfeedback.setter
    def correctfeedback(self, correct_feedback):
        self.__correct_feedback = correct_feedback

    @property
    def incorrectfeedback(self):
        return self.__incorrect_feedback

    @incorrectfeedback.setter
    def incorrectfeedback(self, incorrect_feedback):
        self.__incorrect_feedback = incorrect_feedback

    @property
    def point(self):
        return self.__point_value

    @point.setter
    def point(self, point):
        self.__point_value = point

    # Form a question list
    def set_questionlist(self):
        self.__question_list = {self.question: {'Choice': [self.choice1, self.choice2,
                                                           self.choice3, self.choice4],
                                                'Correct': self.correct,
                                                'Correct_feedback': self.__correct_feedback,
                                                'Incorrect_feedback': self.__incorrect_feedback,
                                                'Point_value': self.point}}


def clean_window():
    win.geometry('500x500')
    for widgets in win.winfo_children():
        if isinstance(widgets, Menu) is False:
            widgets.grid_forget()


correct_times = 0
play_time = 0
gained_point = 0


# each start generate three times question,
# but only one time question index list generated
def start():
    global correct_times, play_time, gained_point
    gained_point = 0
    correct_times = 0
    play_time = 0
    existing_list, ask_ques = question_index_generate()
    question_generate(existing_list, ask_ques)


# Generate indexes for questions which will be used one time per test
def question_index_generate():
    fileHandle = open('Question.json')
    existing_list = json.load(fileHandle)
    fileHandle.close()
    count = -1
    # get question index stored in the file
    for i in existing_list:
        count += 1
    # Store the index to the list
    quest_index = [x for x in range(count)]
    # randomly pick three index from the list for test
    ask_ques = random.sample(quest_index, k=3)
    return existing_list, ask_ques


# generate question depend on the index from question_index_generate()
def question_generate(existing_list, ask_ques):
    global play_time
    if play_time < 3:
        for k, v in existing_list[ask_ques[play_time]].items():
            questions.set(k)
            choice1.set(v["Choice"][0])
            choice2.set(v["Choice"][1])
            choice3.set(v["Choice"][2])
            choice4.set(v["Choice"][3])
            correct = v["Correct"]
            cor_fed = v["Correct_feedback"]
            incor_fed = v["Incorrect_feedback"]
            pv = v["Point_value"]
        play_time += 1
        clean_window()
        # points_label = Label(win, text=pv, bg='sky blue')
        # points_label.grid(row=0)
        title_label = Label(win, text=f'Question {play_time} out of 3', bg='sky blue', font=2)
        title_label.grid(row=2, column=0, columnspan=3, ipadx=140, sticky=N)
        gainedpoint_label = Label(win, text=f'You have earned {gained_point} point', bg='sky blue', font=2)
        gainedpoint_label.grid(row=1, column=0, columnspan=3, ipadx=120, sticky=N)
        question_box = Frame(win, width=300, height=200, bg='white', relief=SUNKEN)
        question_box.grid(row=4, column=0, columnspan=3, ipadx=60, padx=30, sticky=NSEW)
        question_box.pack_propagate(0)

        questions_label = Label(question_box, text=f'Question: {questions.get()}', bg='white')
        questions_label.grid(row=1, column=0, sticky=W)
        c1_label = Label(question_box, text=f'Choice 1: {choice1.get()}', bg='white')
        c1_label.grid(row=2, sticky=W)
        c2_label = Label(question_box, text=f'Choice 2: {choice2.get()}', bg='white')
        c2_label.grid(row=3, sticky=W)
        c3_label = Label(question_box, text=f'Choice 3: {choice3.get()}', bg='white')
        c3_label.grid(row=4, sticky=W)
        c4_label = Label(question_box, text=f'Choice 4: {choice4.get()}', bg='white')
        c4_label.grid(row=5, sticky=W)

        pv_label = Label(win, text=f'Point Value for this question: {pv}', bg='sky blue')
        pv_label.grid(row=3, column=2, sticky=E, pady=5)

        answer_label = Label(win, text='Please select your answer: ', bg='sky blue', font=2)
        answer_label.grid(row=7, column=1, sticky=E)

        combo_answer = ttk.Combobox(win, values=['Choice 1', 'Choice 2', 'Choice 3', 'Choice 4'])
        combo_answer.grid(row=7, column=2, padx=20, pady=25)

        ctn_btn = Button(win, text='Continue', command=lambda: feedback(existing_list, cor_fed, incor_fed, ask_ques,
                                                                        correct, combo_answer,
                                                                        ctn_btn, pv, gainedpoint_label,
                                                                        answer_label))
        ctn_btn.grid(row=8,columnspan=3, padx=50, pady=20)

    else:
        clean_window()
        if correct_times ==2:
            title_label = Label(win, text=f'Good job,\nYou answered 2 question correctly!'
                                          f'\nYou get {gained_point} point.', bg='sky blue', font=2)
            try:
                filename = 'gj.jpg'
                img = cv2.imread(filename)
                cv2.imshow('Thank you', img)
                cv2.waitKey(0)
            except:
                pass
        elif correct_times ==3:
            title_label = Label(win, text=f'Congratulation!\nYou got all question correctly!'
                                          f'\nYou get {gained_point} point.', bg='sky blue', font=2)
            try:
                filename = 'WD.jpg'
                img = cv2.imread(filename)
                cv2.imshow('Thank you', img)
                cv2.waitKey(0)
            except:
                pass
        elif correct_times ==1:
            title_label = Label(win, text=f'Well!\nUnless you got 1 question correct!\nYou get {gained_point} point.',
                                bg='sky blue', font=2)
            try:
                filename = '.jpg'
                img = cv2.imread(filename)
                cv2.imshow('Thank you', img)
                cv2.waitKey(0)
            except:
                pass
        else:
            title_label = Label(win, text=f'Good job! You missed all the question!'
                                          f'\nYou get {gained_point} point.', bg='sky blue', font=2)
            try:
                filename = 'hahahaha.png'
                img = cv2.imread(filename)
                cv2.imshow('Thank you', img)
                cv2.waitKey(0)
            except:
                pass
        title_label.grid(row=2, column=0, columnspan=3, ipadx=80, pady=100)
        ctn_btn = Button(win, text='Start another test', command=start)
        ctn_btn.grid(row=8, columnspan=3, padx=50, pady=20)


# Generate feedback for each question
def feedback(existing_list, cor_fed, incor_fed, ask_ques, correct, combo_answer, ctn_btn, pv, gainedpoint_label,
             answer_label):
    global correct_times, gained_point
    # delete the answer button
    ctn_btn.grid_forget()
    combo_answer.grid_forget()
    answer_label.grid_forget()
    if correct - 1 == combo_answer.current():
        try:
            list = cor_fed.split('-')
            if list[0] == 'PIC':
                filename = list[1]
                cv2.namedWindow('Correct Feedback')
                img = cv2.imread(filename)
                cv2.imshow('Correct Feedback', img)
                cv2.waitKey(0)
            else:
                feedback_text.set(f'Correct Feedback: {cor_fed}')
                feedback_box['bg'] = 'green'
                feedback_label['bg'] = 'green'
                feedback_label['bg'] = 'green'
        except:
            feedback_text.set('Correct')
            feedback_box['bg'] = 'green'
            feedback_label['bg'] = 'green'
            feedback_label['bg'] = 'green'
        correct_times += 1
        gained_point += pv
        gainedpoint_label['text'] = f'Gained point value: {gained_point}'
    else:
        try:
            list = incor_fed.split('-')
            if list[0] == 'PIC':
                filename = list[1]
                cv2.namedWindow('Incorrect Feedback')
                img = cv2.imread(filename)
                cv2.imshow('Incorrect Feedback', img)
                cv2.waitKey(0)
            else:
                feedback_text.set(f'Incorrect Feedback: {incor_fed}')
                feedback_box['bg'] = 'red'
                feedback_label['bg'] = 'red'
        except:
            feedback_text.set('Incorrect')
            feedback_box['bg'] = 'red'
            feedback_label['bg'] = 'red'

    feedback_box.grid(row=8, column=0, columnspan=3, ipadx=60, pady=30, sticky=NSEW)
    feedback_box.pack_propagate(0)

    feedback_label.grid(row=0, columnspan=3, sticky=N)
    ok_btn = Button(win, text='Continue', command=lambda: question_generate(existing_list, ask_ques))
    ok_btn.grid(row=10, columnspan=3)


# List all the question
def list(*args):
    global list_box
    clean_window()
    list_box.delete(0, END)
    list_box['height'] = 25
    list_box.bind('<Double-Button-1>', list)
    fileHandle = open('Question.json')
    existing_list = json.load(fileHandle)
    fileHandle.close()
    main_title = Label(win, text='Below is list of all questions', bg='sky blue', font=2)
    main_title.grid(row=0, column=0, columnspan=3, sticky=W, ipadx=100, pady=10)
    scrollbar.config(command=list_box.yview)
    scrollbar.grid(row=1, column=1, sticky=W, ipady=176)
    list_box.grid(row=1, column=0, ipadx=90)
    for i in existing_list:
        for k, v in i.items():
            list_box.insert(END, k)
    return main_title


# delete question in the file and clean the deleted question on the window
def del_question(event):
    global list_box
    fileHandle = open('Question.json')
    existing_list = json.load(fileHandle)
    fileHandle.close()
    questions = []
    for i in existing_list:
        for k, v in i.items():
            questions.append(k)
    existing_list.pop(list_box.curselection()[0])
    with open('Question.json', 'w') as fp:
        json.dump(existing_list, fp)
    clean_window()
    delete()
    messagebox.showinfo('Completed', 'The question has been deleted')


# after click the button, delete the question choose
def delete():
    clean_window()
    main_title = list()
    main_title['text'] = 'Double click the question\nyou want to delete'
    list_box['height'] = 15
    list_box.bind('<Double-Button-1>', del_question)
    scrollbar.grid(row=1, column=1, sticky=W, ipady=95)


# after click button, jump into change_question method
def edit():
    global list_box
    clean_window()
    main_title = list()
    main_title['text'] = 'Double click the question\nyou want to edit'
    list_box['height'] = 15
    list_box.bind('<Double-Button-1>', change_question)
    scrollbar.grid(row=1, column=1, sticky=W, ipady=95)


# edit question
# delete the needed change one and add the changed new one
def change_question(event):
    # global questions, choice1, choice2, choice3, choice4, correct, correctfed, incorrectfed, point
    clean_window()
    # question_change = combo_questions.get()
    fileHandle = open('Question.json')
    existing_list = json.load(fileHandle)
    fileHandle.close()
    index = list_box.curselection()[0]
    for k, v in existing_list[index].items():
        questions.set(k)
        choice1.set(v["Choice"][0])
        choice2.set(v["Choice"][1])
        choice3.set(v["Choice"][2])
        choice4.set(v["Choice"][3])
        correct.set(v["Correct"])
        correctfed.set(v["Correct_feedback"])
        incorrectfed.set(v["Incorrect_feedback"])
        point.set(v["Point_value"])
    edit_label = Label(win, text='You can edit the question below.', bg='sky blue', font=2)
    edit_label.grid(row=0, column=0, columnspan=2, sticky=W, pady=10, ipadx=80)
    question_enter()
    # continue to pop the old question and store the new editted one
    ctn_btn = Button(win, text='Save Question', command=
    lambda: pop_add(existing_list, list_box.curselection()[0]))
    ctn_btn.grid(row=10, column=1, sticky=W, pady=50, padx=20, ipadx=10)


def question_enter():
    # Create question label and entry box
    question_label.grid(row=1, column=0, sticky=W)
    question_entry.grid(row=1, column=1, sticky=W)
    # Create 4 choice label and entry box
    choice1_label.grid(row=2, column=0, sticky=W)
    choice1_entry.grid(row=2, column=1, sticky=W)
    choice2_label.grid(row=3, column=0, sticky=W)
    choice2_entry.grid(row=3, column=1, sticky=W)
    choice3_label.grid(row=4, column=0, sticky=W)
    choice3_entry.grid(row=4, column=1, sticky=W)
    choice4_label.grid(row=5, column=0, sticky=W)
    choice4_entry.grid(row=5, column=1, sticky=W)
    # Create label and entry box for correct answer
    correct_label.grid(row=6, column=0, columnspan=1, sticky=W)
    correct_entry.grid(row=6, column=1, sticky=W)
    # Feedback for wrong and correct answer
    correctfed_label.grid(row=7, column=0, columnspan=1, sticky=W)
    correctfed_entry.grid(row=7, column=1, sticky=W)
    incorrectfed_label.grid(row=8, column=0, columnspan=1, sticky=W)
    incorrectfed_entry.grid(row=8, column=1, sticky=W)
    # point value label and entry box
    point_label.grid(row=9, column=0, columnspan=1, sticky=W)
    point_entry.grid(row=9, column=1, sticky=W)


# before pop the old question
# check if the user have enter the valid question and choice and etc
# then store the new questions
def pop_add(existing_list, index):
    if questions.get() == '':
        messagebox.showinfo('ERROR', 'Please input valid question.')
    elif choice1.get() == '' or choice2.get() == '' or choice3.get() == '' or choice4.get() == '':
        messagebox.showinfo('ERROR', 'Please input valid choice.')
    elif correct.get() not in [1, 2, 3, 4] or correct.get() == '':
        messagebox.showinfo('ERROR', 'Please input valid correct answer number.')
    elif correctfed.get() == '':
        messagebox.showinfo('ERROR', 'Please input valid correct answer feedback.')
    elif incorrectfed.get() == '':
        messagebox.showinfo('ERROR', 'Please input valid incorrect answer feedback.')
    elif point.get() not in [1, 2, 3] or point.get() == '':
        messagebox.showinfo('ERROR', 'Please input valid point value')
    else:
        existing_list.pop(index)
        with open('Question.json', 'w') as fp:
            json.dump(existing_list, fp)
        store_question()


# store new question to the question file
# before store the question, check the valid of the question
def store_question():
    # make sure user enter
    if questions.get() == '':
        messagebox.showinfo('ERROR', 'Please input valid question.')
    elif choice1.get() == '' or choice2 == '' or choice3 == '' or choice4 == '':
        messagebox.showinfo('ERROR', 'Please input valid choice.')
    elif correct.get() not in [1, 2, 3, 4]:
        messagebox.showinfo('ERROR', 'Please input valid correct answer number.')
    elif correctfed.get() == '':
        messagebox.showinfo('ERROR', 'Please input valid correct answer feedback.')
    elif incorrectfed.get() == '':
        messagebox.showinfo('ERROR', 'Please input valid incorrect answer feedback.')
    elif point.get() not in [1, 2, 3]:
        messagebox.showinfo('ERROR', 'Please input valid point value')
    else:
        # Create a temporary Question object
        temp_ques = Question()
        temp_ques.question = questions.get()
        temp_ques.choice1 = choice1.get()
        temp_ques.choice2 = choice2.get()
        temp_ques.choice3 = choice3.get()
        temp_ques.choice4 = choice4.get()
        temp_ques.correct = correct.get()
        temp_ques.correctfeedback = correctfed.get()
        temp_ques.incorrectfeedback = incorrectfed.get()
        temp_ques.point = point.get()
        # Get the formed question list
        temp_ques.set_questionlist()
        # Append the new list to the file
        new_add = temp_ques.questionlist
        fileHandle = open('Question.json')
        existing_list = json.load(fileHandle)
        fileHandle.close()
        existing_list.append(new_add)
        with open('Question.json', 'w') as fp:
            json.dump(existing_list, fp)
    messagebox.showinfo('Completed', 'Question stored.')


# reset the question information
def default():
    clean_window()
    questions.set('')
    choice1.set('')
    choice2.set('')
    choice3.set('')
    choice4.set('')
    correct.set(1)
    correctfed.set('')
    incorrectfed.set('')
    point.set(1)


# add new question into json file
def add():
    # reset the value of the question, choices, corrects and feedback
    default()
    # display the main title for add page
    main = Label(win, text='Please Enter the Question Below.', bg='sky blue',font=2)
    main.grid(row=0, column=0, columnspan=2, sticky=W, pady=10, ipadx=80)
    question_enter()
    # Save question by using the store function
    save_btn.grid(row=10, column=1, sticky=W, pady=50, padx=20, ipadx=10)


def search():
    clean_window()
    search.set('')
    main_search.grid(row=0, column=0, sticky=E, padx=140, pady=25)
    search_entry.grid(row=1, column=0, columnspan=2)
    search.get()
    search_btn.grid(row=2, column=0, pady=50, padx=200, ipadx=10, columnspan=2)


def search_question(data):
    global searchResults
    clean_window()
    main_result.grid(row=0, columnspan=2)
    edit_result.grid(row=1, columnspan=2)
    fileHandle = open('Question.json')
    existing_list = json.load(fileHandle)
    fileHandle.close()
    question_list = []
    for i in existing_list:
        for k, v in i.items():
            question_list.append(k)
    searchResults = get_close_matches(data, question_list, n=3, cutoff=0.5)
    print(searchResults, question_list)
    list_box.delete(0, END)
    list_box['height'] = 25
    list_box.grid_forget()
    list_box.bind('<Double-Button-1>', edit_search_question)
    scrollbar.config(command=list_box.yview)
    scrollbar.grid(row=2, column=1, sticky=W, ipady=176)
    list_box.grid(row=2, column=0, ipadx=90)
    for i in searchResults:
        list_box.insert(END, i)


def edit_search_question(event):
    clean_window()
    global searchResults
    index = int(list_box.curselection()[0])
    question_edit = searchResults[index]
    print(question_edit)
    fileHandle = open('Question.json')
    existing_list = json.load(fileHandle)
    fileHandle.close()
    # use count to get the index of the edit_question from the existing_list
    count = -1
    for i in existing_list:
        count += 1
        for k, v in i.items():
            if k == question_edit:
                questions.set(k)
                print(i, k)
                choice1.set(v["Choice"][0])
                choice2.set(v["Choice"][1])
                choice3.set(v["Choice"][2])
                choice4.set(v["Choice"][3])
                correct.set(v["Correct"])
                correctfed.set(v["Correct_feedback"])
                incorrectfed.set(v["Incorrect_feedback"])
                point.set(v["Point_value"])
                break
    edit_label = Label(win, text='You can edit the question below.', bg='sky blue', font=2)
    edit_label.grid(row=0, column=0, columnspan=2, sticky=W, pady=10,ipadx=80)
    question_enter()
    # Save question by using the store function
    countinue_btn = Button(win, text='Save the Change', command=lambda:pop_add(existing_list, count))
    countinue_btn.grid(row=10, column=1, sticky=W, pady=50, padx=20, ipadx=10)


# Home page for Mental Anguish
def homepage():
    clean_window()
    welcome_label = Label(win, text='Welcome to use Mental Anguish', bg='sky blue', font=30)
    welcome_label.grid(row=0, column=0, pady=100, padx=100, ipadx=10)
    start_btn = Button(win, text='Start Test', command=start)
    start_btn.grid(row=1, column=0,ipadx=13)
    edit_btn = Button(win, text='Add Question', command=add)
    edit_btn.grid(row=2, column=0, pady=6)
    list_btn = Button(win, text='Question List', command=list)
    list_btn.grid(row=3, column=0,  ipadx=1)
    exit_btn = Button(win, text='Exit', command=win.quit)
    exit_btn.grid(row=4, column=0, ipadx=26, pady=6)


# create a template Question object
temp_question = Question()

# create window
win = Tk()
win.config(bg='sky blue')
win.title('Mental Anguish')
win.geometry('500x500')

# menu bar for the window
# menu bar include file and edit menu
menu_bar = Menu(win)
win.config(menu=menu_bar)
win['menu'] = menu_bar
# file menu include restart, list, search and exit
file_menu = Menu(menu_bar, tearoff=False)
menu_bar.add_cascade(label='File', menu=file_menu)
file_menu.add_command(label='Restart', command=start)
file_menu.add_command(label='List', command=list)
file_menu.add_command(label='Search', command=search)
file_menu.add_command(label='EXIT', command=win.quit)
# edit menu include edit, add and delete
edit_menu = Menu(menu_bar, tearoff=False)
menu_bar.add_cascade(label='Edit', menu=edit_menu)
edit_menu.add_command(label='Add', command=add)
edit_menu.add_command(label='Edit', command=edit)
edit_menu.add_command(label='Delete', command=delete)
# save button, for saving question usage
save_btn = Button(win, text='Save Question', command=store_question)

# list box and related scrollbar for delete, edit and list questions
scrollbar = Scrollbar(win)
list_box = Listbox(win, width=50, height=25, yscrollcommand=scrollbar.set)
scrollbar.config(command=list_box.yview)

# search button and entry, used for searching question
search = StringVar()
searchResults = []
main_search = Label(win, text='Please Enter the Question you want to search.', bg='sky blue')
search_entry = Entry(win, textvariable=search, width=60)
search_btn = Button(win, text='Search', command=lambda: search_question(search.get()))
# main title of the result page
main_result = Label(win, text='Below is the results.', bg='sky blue', font=2)
edit_result = Label(win, text='Double click to edit', bg='sky blue')
back_result = Label(win, text='Enter BACK button to search another question.', bg='sky blue')

# Label and entry for the questions and its relative information
# the entry and label won't be showed in window directly
# Only edit and add function can show them on the window
questions = StringVar()
choice1 = StringVar()
choice2 = StringVar()
choice3 = StringVar()
choice4 = StringVar()
correct = IntVar()
correctfed = StringVar()
incorrectfed = StringVar()
point = IntVar()
# label and entry for question
question_label = Label(win, text='Question', bg='sky blue')
question_entry = Entry(win, textvariable=questions, width=50)
# Create 4 choice label and entry box
choice1_label = Label(win, text='Choice 1', bg='sky blue')
choice1_entry = Entry(win, textvariable=choice1, width=50)
choice2_label = Label(win, text='Choice 2', bg='sky blue')
choice2_entry = Entry(win, textvariable=choice2, width=50)
choice3_label = Label(win, text='Choice 3', bg='sky blue')
choice3_entry = Entry(win, textvariable=choice3, width=50)
choice4_label = Label(win, text='Choice 4', bg='sky blue')
choice4_entry = Entry(win, textvariable=choice4, width=50)
# Create label and entry box for correct answer
correct_label = Label(win, text='Which is Correct answer #', bg='sky blue')
correct_entry = Entry(win, textvariable=correct, width=50)
# Feedback for wrong and correct answer
correctfed_label = Label(win, text='Feedback for corect answer: ', bg='sky blue')
correctfed_entry = Entry(win, textvariable=correctfed, width=50)
incorrectfed_label = Label(win, text='Feedback for corect answer: ', bg='sky blue')
incorrectfed_entry = Entry(win, textvariable=incorrectfed, width=50)
# point value label and entry box
point_label = Label(win, text='What is point value for the question', bg='sky blue')
point_entry = Entry(win, textvariable=point, width=50)


feedback_text = StringVar()
feedback_box = Frame(win, width=30, height=200, bg='sky blue', relief=SUNKEN)
feedback_label = Label(feedback_box, textvariable=feedback_text, bg='sky blue')

homepage()


win.mainloop()
