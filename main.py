import pandas as pd
import random
from collections import defaultdict
df = pd.read_csv('/Users/homdanil153/Downloads/AL.tsv', sep='\t')
names = list(df['ФИО'])
grades = [random.randint(13, 20) for i in range(len(df))]
emails = list(df['Почта'])
departments = list(df['группа'])
new_line = '\n'

class User:
    def __init__(self, name, grade, mail, department):
        self.name = name
        self.grade = grade
        self.mail = mail
        self.department = department

    def __eq__(self, other):
        return self.mail == other.mail


list_users = [User(name, grade, email, dep) for name, grade, email, dep in zip(names, grades, emails, departments)]
list_departs = list(set(departments))


class Calendar:
    def __init__(self, events=[], current_time=0, log_events=[]):
        self.events = events
        self.current_time = current_time
        self.log_events = log_events

    def clear_calendar(self):
        for event in self.events:
            if event.end < self.current_time:
                self.log_events.append(event)
                self.events.remove(event)

    def send_mail_to_user(self, mail, message):
        pass


    def send_notification_to_user(self, user, event):
        self.send_mail_to_user(user.mail, f"Через {event.remind_value} дней у вас будет встреча {event}")

    def send_notification(self):
        for event in self.events:
            if event.start == self.current_time + event.remind_value:
                for user in event.participants:
                    self.send_notification_to_user(user, event)

    def check_intersection(self, event1, event2):
        inter_users = []
        if (event1.start < event2.end and event1.end > event2.start) or \
                (event2.start < event1.end and event2.end > event1.start):
            if event1.place == event2.place:
                return False, f"Переговорка {event1.place} занята в данное время"
            intersection_users = []
            for par1 in event1.participants:
                for par2 in event2.participants:
                    if par1 == par2:
                        intersection_users.append(par1)
            for user in intersection_users:
                inter_users.append(user.mail)
        mess = ''
        if len(inter_users) != 0:
            mess = " ".join(inter_users)
        return True, mess

    def add_event(self, event):
        # +
        flag = True
        all_mes = ''
        for temp_event in self.events:
            flag1, mes = self.check_intersection(event, temp_event)
            all_mes = all_mes + ' ' + mes
            flag = flag and flag1
            if not flag:
                break
        if flag:
            self.events.append(event)
            return True, all_mes.strip(' ')
        else:
            return False, mes

    def remove_event(self, event, user):
        # +
        if event.check_change_user(user):
            self.events.remove(event)
            return True, "Событие удалено"
        else:
            return False, "У вас недостаточно прав для удаления события"

    def change_event(self, old_event, new_event, user):
        if old_event.check_change_user(user):
            self.events.remove(old_event)
            self.add_event(new_event)

    def get_information(self, name):
        if name == "Календарь":
            return self.events
        else:
            for dep in list_departs:
                if dep == name:
                    return [i for i in self.events if i.check_department_event(dep)]
            for user in list_users:
                if name == user.mail:
                    print([])
                    return [i for i in self.events if user in i.participants]
            return None


class MyEvent:
    def __init__(self, name, start, end, participants, description, place, priority, remind_value):
        self.name = name
        self.start = start
        self.end = end
        self.participants = participants
        self.description = description
        self.place = place
        self.priority = priority
        self.remind_value = remind_value

    def __eq__(self, other):
        return self.name == other.name and self.start == other.start and self.end == other.end and self.place == other.place

    def check_change_user(self, user):
        return user.grade == max([i.grade for i in self.participants])

    def is_participant(self, user):
        for temp_user in self.participants:
            if temp_user == user:
                return True
        return False

    def check_department_event(self, department):
        flag = True
        for participant in self.participants:
            flag = flag and participant.department == department
        return flag

    def to_json(self):
        return f"Название: {self.name}{new_line}Начало: {self.start}{new_line}Конец: {self.end}{new_line}Участники: {', '.join([i.mail for i in self.participants])}{new_line}" \
               f"Описание: {self.description}{new_line}Место: {self.place}{new_line}Приоритет: " \
               f"{self.priority}{new_line}Напоминалка: {self.remind_value}{new_line}{new_line}"

from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
import sys

def find_user_by_login(login):
    for user in list_users:
        if user.mail == login:
            return user
    return User("NoUser", 'NoUser', 'NoUser', 'NoUser')

def parse_partisipants(s):
    return [find_user_by_login(i.strip(',')) for i in s.split(' ')]


class UIEvent:
    def __init__(self, fr):
        self.event_params = defaultdict(StringVar)
        self.my_name = StringVar()
        [self.event_params[i] for i in ['name_event_val', 'start_event_val', 'end_event_val', 'participatns_val', 'descr_val', 'place_val', 'prior_val', 'rem_val']]
        self.set_null_values()
        self.fr = fr
        self.necess = {'name_event_val': 'Название', 'start_event_val': 'Начало', 'participatns_val': 'Участники', 'place_val': 'Место'}
        self.printUI()

    def add_event(self):
        if sum([self.event_params[key].get() == '' for key in self.necess.keys()]) != 0:
            messagebox.showwarning(title='Warning!', message=f"Вы не заполнили все обязательные поля:{new_line} {new_line.join(self.necess.values())}")
        else:
            self.set_default_values()
            new_event = MyEvent(name=self.event_params['name_event_val'].get(), start=int(self.event_params['start_event_val'].get()),
                              end=int(self.event_params['end_event_val'].get()), participants=parse_partisipants(self.event_params['participatns_val'].get()),
                              description=self.event_params['descr_val'].get(), place=self.event_params['place_val'].get(),
                              priority=int(self.event_params['prior_val'].get()), remind_value=int(self.event_params['rem_val'].get()))
            bad_users = self.check_part(self.event_params['participatns_val'].get())
            if len(bad_users) != 0:
                messagebox.showwarning(title='Warning!', message=f"Следующих пользователей нет в базе данных:{new_line}{f'{new_line}'.join(list(set(bad_users)))}")
                return False
            flag, mes = self.fr.calendar.add_event(new_event)
            if flag:
                if mes == '':
                    temp_text = "Вы успешно добавили соыбтие"
                else:
                    temp_text = f'Вы успешно добавили соыбтие, но у следующих пользователей в это время уже есть встреча:{new_line} {new_line.join(list(set(mes)).split(" "))}'
                messagebox.showinfo(title='Ok', message=temp_text)
            else:
                messagebox.showwarning(title='Warning!', message=f"Не получилось добавить соыбтие: {mes}")

    def remove_event(self):
        if sum([self.event_params[key].get() == '' for key in self.necess.keys()]) != 0:
            messagebox.showwarning(title='Warning!', message=f"Вы не заполнили все обязательные поля:{new_line} {new_line.join(self.necess.values())}")
        else:
            if self.my_name.get() == '':
                messagebox.showwarning(title='Warning!', message=f"Вы не представились")
            else:
                rem_event = MyEvent(name=self.event_params['name_event_val'].get(), start=int(self.event_params['start_event_val'].get()),
                              end=int(self.event_params['end_event_val'].get()), participants=parse_partisipants(self.event_params['participatns_val'].get()),
                              description=self.event_params['descr_val'].get(), place=self.event_params['place_val'].get(),
                              priority=int(self.event_params['prior_val'].get()), remind_value=int(self.event_params['rem_val'].get()))
                user = find_user_by_login(self.my_name.get())
                if user.name == 'NoUser':
                    messagebox.showwarning(title='Warning!', message=f"Не существует пользователя с логином {self.my_name.get()}")
                else:
                    flag, mes = self.fr.calendar.remove_event(rem_event, user)
                    if flag:
                        messagebox.showinfo(title='Ok', message="Осбытие успешно удалено")
                    else:
                        messagebox.showwarning(title='Warning!', message=f"Событие не добавлено: {new_line}{mes}")

    def printUI(self):
        name_event = Label(self.fr, text='Название события')
        start_event = Label(self.fr, text='Начало события')
        end_event = Label(self.fr, text='Конец события')
        participatns = Label(self.fr, text='Участники события')
        descr = Label(self.fr, text='Описание события')
        place = Label(self.fr, text='Место события')
        prior = Label(self.fr, text='Важность события')
        rem = Label(self.fr, text='Напоминалка события')
        name_event.grid(row=1, column=0)
        start_event.grid(row=2, column=0)
        end_event.grid(row=3, column=0)
        participatns.grid(row=4, column=0)
        descr.grid(row=5, column=0)
        place.grid(row=6, column=0)
        prior.grid(row=7, column=0)
        rem.grid(row=8, column=0)

        entries = []
        for i, key in enumerate(self.event_params.keys()):
            entries.append(Entry(self.fr, textvariable=self.event_params[key]))
            entries[-1].grid(row=i+1, column=1)

        my_name = Label(self.fr, text='Мой логин')
        my_name.grid(row=1, column=4)
        my_name_text = Entry(self.fr, textvariable=self.my_name)
        my_name_text.grid(row=2, column=4)

        addev = Button(self.fr, text="Добавить событие", command=self.add_event)
        addev.grid(row=2, column=3)

        remev = Button(self.fr, text="Удалить событие", command=self.remove_event)
        remev.grid(row=3, column=3)

    def set_null_values(self):
        for key in self.event_params.keys():
            self.event_params[key].set('')
        self.my_name.set('')

    def set_default_values(self):
        if self.event_params['prior_val'].get() == '':
            self.event_params['prior_val'].set('5')
        if self.event_params['rem_val'].get() == '':
            self.event_params['rem_val'].set('30')
        if self.event_params['end_event_val'].get() == '':
            self.event_params['end_event_val'].set(str(30 + int(self.event_params['start_event_val'].get())))

    def check_part(self, participants):
        parts = [i.strip(',') for i in participants.split(' ')]
        bad_users = []
        for participant in parts:
            part = find_user_by_login(participant)
            if part.name == 'NoUser':
                bad_users.append(participant)
        return bad_users




class UICalendar():
    def __init__(self, fr):
        self.fr = fr
        self.out_cal = StringVar()
        self.printUI()

    def write_calendar(self):
        name = self.out_cal.get()
        if name == '':
            messagebox.showwarning(title='Warning!', message=f"Вы не ввели для кого показывать календарь")
        else:
            events = self.fr.calendar.get_information(name)
            if not events:
                messagebox.showwarning(title='Warning!', message=f"Вы ввели некорретный департамент или пользователя(или 'Календарь')")
            else:
                Window_events(self.fr, [str(i.to_json()) for i in self.fr.calendar.events])


    def pring_log(self):
        Window_events(self.fr, [str(i.to_json()) for i in self.fr.calendar.log_events])

    def printUI(self):
        log = Button(self.fr, text="Вывести прошедшие события", command=self.pring_log)
        log.grid(row=4, column=3)

        type_pr2 = Label(self.fr, text="  Введите логин пользователя/\nназвание отдела или 'Календарь'")
        type_pr2.grid(row=5, column=4)

        type_pr3 = Entry(self.fr, textvariable=self.out_cal)
        type_pr3.grid(row=6, column=4)

        printcal = Button(self.fr, text="Вывести календарь", command=self.write_calendar)
        printcal.grid(row=5, column=3)

class Window_events(Toplevel):
    def __init__(self, parent, events=None):
        super().__init__(parent)
        self.events = events
        self.initUI()

    def initUI(self):

        log = Text(self)
        log.insert(1.0, "\n".join(self.events))
        log.grid(row=0, column=5, columnspan=3, rowspan=4)

        obtn = Button(self, text="Закрыть", command=self.destroy)
        obtn.grid(row=10, column=10)

class Example(Frame):

    def __init__(self):
        super().__init__()
        self.calendar = Calendar()
        self.UIevent = UIEvent(self)
        self.UICalendar = UICalendar(self)
        self.initUI()

    def click_step(self):
        self.calendar.current_time += 30
        self.a.set(f"Текущее время: {self.calendar.current_time}")
        self.calendar.clear_calendar()


    def close_simul(self):
        sys.exit()

    def open_help(self):
        messagebox.showinfo(title='Help', message="1) Чтобы добавить или удалить событие обязательно заполните поля Название, Начало, Участники, Место. \n\n"
                                                  "2) Чтобы удалить событие нужно указать свой логин\n\n"
                                                  "3) Чтобы вывести календарь необходимо указать для кого вы выводите: Пользователь, Департамент, Весь")


    def initUI(self):
        self.master.title("Календарь")
        self.pack(fill=BOTH, expand=True)

        self.columnconfigure(1, weight=1)
        self.columnconfigure(3, pad=7)
        self.rowconfigure(3, weight=3)
        self.rowconfigure(5, pad=7)

        self.a = StringVar()
        self.a.set('Текущее время: 0')
        self.curtime = Label(self, textvariable=self.a)

        self.curtime.grid(row=0, column=1, pady=4, padx=5)

        abtn = Button(self, text="Сделать шаг (30 минут).", command=self.click_step)
        abtn.grid(row=1, column=3)

        obtn = Button(self, text="Закрыть", command=self.close_simul)
        obtn.grid(row=0, column=0)

        help = Button(self, text="Помощь", command=self.open_help)
        help.grid(row=9, column=0)

def main():
    root = Tk()
    app = Example()
    root.mainloop()

if __name__ == '__main__':

    main()
