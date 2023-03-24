import PySimpleGUI as sg
import main

sg.theme("DefaultNoMoreNagging")
sg.set_options(font=("Courier New", 12))

goal_headings = ["GOAL", "TASKS", "DONE"]
tasks_headings = ["DONE", "TASK"]

def open_todo_window(goal_id):
    col_layout = [
    [sg.Button("MARK DONE", key="mark_btn"),
     sg.Button("ADD", key="add_btn"),
     sg.Button("EDIT", key="edit_btn"),
     sg.Button("DELETE", key="delete_btn")],
    [sg.Text("Task(s):"), sg.Multiline(key="task", size=(32,3), enable_events=True)],
    [sg.Table(values=main.Tasks().getTasks(goal_id), headings=tasks_headings, key="tasks_table",
              justification='center', expand_x=True, expand_y=True,
              col_widths=[5,25], auto_size_columns=False, max_col_width=25)]
    ]

    layout = [
        [sg.Column(col_layout, scrollable=False, element_justification='center',
                   expand_x=True, expand_y=True)]
    ]

    window = sg.Window("TODO LIST", layout, size=(500, 300), modal=True,
                       resizable=True, finalize=True)
    while True:
        event, values = window.read()
        if event in ("Exit", sg.WIN_CLOSED):
            break
        elif event == "mark_btn":
            if len(values['tasks_table']):
                current_entries = window['tasks_table'].get()
                indexes = values['tasks_table']
                for index in indexes:
                    isFinished = False
                    if current_entries[index][0] == 'X': isFinished = True
                    main.Tasks().finishTask(current_entries[index][-1], isFinished)
                window['tasks_table'].update(main.Tasks().getTasks(goal_id))
        elif event == "add_btn":
            tasksSTR = values['task']
            tasksList = str(tasksSTR).split('\n')
            for t in tasksList:
                main.Tasks().addTask(t, goal_id)
            window['task'].update(value='')
            window['tasks_table'].update(main.Tasks().getTasks(goal_id))
        elif event == "edit_btn":
            newTask = values['task']
            current_entries = window['tasks_table'].get()
            index = values['tasks_table'][0]
            main.Tasks().editTask(newTask, current_entries[index][-1])
            window['task'].update(value='')
            window['tasks_table'].update(main.Tasks().getTasks(goal_id))
        elif event == "delete_btn":
            current_entries = window['tasks_table'].get()
            index = values['tasks_table'][0]
            main.Tasks().deleteTask(current_entries[index][-1])
            window['tasks_table'].update(main.Tasks().getTasks(goal_id))
    window.close()


col_layout = [
    [sg.Button("OPEN TODO LIST", key="open_btn"),
     sg.Button("ADD", key="add_btn"),
     sg.Button("EDIT", key="edit_btn"),
     sg.Button("DELETE", key="delete_btn")],
    [sg.Text("Title:"), sg.Input(key="title", size=(32,1))],
    [sg.Table(values=main.Goals().getGoals(), headings=goal_headings, key="goals_table",  
              justification='center', expand_x=True, expand_y=True,
              col_widths=[25,5,5], auto_size_columns=False, max_col_width=25)]
]

layout = [
    [sg.Column(col_layout, scrollable=False, element_justification='center',
               expand_x=True, expand_y=True)]
]

window = sg.Window("Goals TODO List", layout, size=(500, 300), resizable=True, finalize=True)

def clear_values(): window['title'].update(value='')

while True:
    event, values = window.read()
    if event in ("Exit", sg.WIN_CLOSED):
        break
    elif event == "open_btn":
        if len(values['goals_table']) != 0:
            current_entries = window['goals_table'].get()
            indexes = values['goals_table']
            for index in indexes:
                open_todo_window(current_entries[index][-1])
            window['goals_table'].update(main.Goals().getGoals())
    elif event == "add_btn":
        title = values['title']
        main.Goals().addGoal(title)
        clear_values()
        window['goals_table'].update(main.Goals().getGoals())
    elif event == "edit_btn":
        current_entries = window['goals_table'].get()
        index = values['goals_table'][0]
        newTitle = title = values['title']
        main.Goals().editGoal(newTitle, current_entries[index][-1])
        clear_values()
        window['goals_table'].update(main.Goals().getGoals())
    elif event == "delete_btn":
        current_entries = window['goals_table'].get()
        index = values['goals_table'][0]
        main.Goals().deleteCourse(current_entries[index][-1])
        clear_values()
        window['goals_table'].update(main.Goals().getGoals())
window.close()
