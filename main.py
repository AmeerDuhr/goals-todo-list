import sqlite3

class Goals:
    def __init__(self):
        self.db = sqlite3.connect("./goals.db")
        self.cr = self.db.cursor()
        self.cr.execute(
            "CREATE TABLE if not exists 'goals' (id INTEGER NOT NULL, title TEXT NOT NULL, CONSTRAINT courses_pk PRIMARY KEY(id));")
        self.cr.execute(
            "CREATE TABLE if not exists 'tasks' (id INTEGER NOT NULL, task TEXT NOT NULL, goal INTEGER NOT NULL, done TEXT NOT NULL, CONSTRAINT courses_pk PRIMARY KEY(id), FOREIGN KEY(goal) REFERENCES 'goals'(id));")

    def getGoals(self):
        self.cr.execute("SELECT * FROM goals")
        goals = self.cr.fetchall()

        filteredGoals = []
        for g in goals:
            self.cr.execute(f"SELECT * FROM tasks WHERE goal={g[0]}")
            tasks = self.cr.fetchall()
            numberOfTasks = len(tasks)
            done = '-'
            doneTasks = 0
            for t in tasks:
                if t[3] == 'X':
                    doneTasks = doneTasks + 1
            if doneTasks == numberOfTasks: done = 'X'

            filteredGoal = [g[1], numberOfTasks, done, g[0]] # title, tasks, done, id
            filteredGoals.append(filteredGoal)

        self.db.commit()
        self.db.close()

        return filteredGoals

    def addGoal(self, title):
        self.cr.execute(f"INSERT INTO goals (title) VALUES ('{title}');")
        self.db.commit()
        self.db.close()

    def editGoal(self, newTitle, id):
        self.cr.execute(f"UPDATE goals SET title='{newTitle}' WHERE id={id};")
        self.db.commit()
        self.db.close()

    def deleteCourse(self, id):
        self.cr.execute(f"DELETE FROM goals WHERE id={id};")
        self.db.commit()
        self.db.close()

class Tasks:
    def __init__(self):
        self.db = sqlite3.connect("./goals.db")
        self.cr = self.db.cursor()
        self.cr.execute(
            "CREATE TABLE if not exists 'goals' (id INTEGER NOT NULL, title TEXT NOT NULL, CONSTRAINT courses_pk PRIMARY KEY(id));")
        self.cr.execute(
            "CREATE TABLE if not exists 'tasks' (id INTEGER NOT NULL, task TEXT NOT NULL, goal INTEGER NOT NULL, done TEXT NOT NULL, CONSTRAINT courses_pk PRIMARY KEY(id), FOREIGN KEY(goal) REFERENCES 'goals'(id));")

    def getTasks(self, goal_id):
        self.cr.execute(f"SELECT * FROM tasks WHERE goal={goal_id}")
        tasks = self.cr.fetchall()

        filteredTasks = []
        for t in tasks:
            filteredTask = [t[3], t[1], t[0]] # done, task, id
            filteredTasks.append(filteredTask)

        self.db.commit()
        self.db.close()

        return filteredTasks

    def addTask(self, task, goal_id):
        self.cr.execute(f"INSERT INTO tasks (task, goal, done) VALUES ('{task}', {goal_id}, '-');")
        self.db.commit()
        self.db.close()

    def editTask(self, newTask, id):
        self.cr.execute(f"UPDATE tasks SET task='{newTask}' WHERE id={id};")
        self.db.commit()
        self.db.close()

    def finishTask(self, id, isFinished):
        if isFinished == False:
            self.cr.execute(f"UPDATE tasks SET done='X' WHERE id={id};")
        else:
            self.cr.execute(f"UPDATE tasks SET done='-' WHERE id={id};")
        self.db.commit()
        self.db.close()

    def deleteTask(self, id):
        self.cr.execute(f"DELETE FROM tasks WHERE id={id};")
        self.db.commit()
        self.db.close()