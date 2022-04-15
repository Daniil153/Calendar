from collections import defaultdict
from utils import find_user_by_login, parse_partisipants
from UI import MyEvent
from tkinter import *
from tkinter import messagebox


class UIEvent:
    def __init__(self, fr):
        self.event_params = defaultdict(StringVar)
        self.my_name = StringVar()
        [self.event_params[i] for i in
         ['name_event_val', 'start_event_val', 'end_event_val', 'participatns_val', 'descr_val', 'place_val',
          'prior_val', 'rem_val']],
        self.set_null_values()
        self.fr = fr
        self.necess = {'name_event_val': 'Название', 'start_event_val': 'Начало', 'participatns_val': 'Участники',
                       'place_val': 'Место'}
        self.printUI()

    def add_event(self):
        if sum([self.event_params[key].get() == '' for key in self.necess.keys()]) != 0:
            messagebox.showwarning(title='Warning!',
                                   message=f"Вы не заполнили все обязательные поля:{new_line} {new_line.join(self.necess.values())}")
        else:
            self.set_default_values()
            new_event = MyEvent(name=self.event_params['name_event_val'].get(),
                                start=int(self.event_params['start_event_val'].get()),
                                end=int(self.event_params['end_event_val'].get()),
                                participants=parse_partisipants(self.event_params['participatns_val'].get()),
                                description=self.event_params['descr_val'].get(),
                                place=self.event_params['place_val'].get(),
                                priority=int(self.event_params['prior_val'].get()),
                                remind_value=int(self.event_params['rem_val'].get()))
            bad_users = self.check_part(self.event_params['participatns_val'].get())
            if len(bad_users) != 0:
                messagebox.showwarning(title='Warning!',
                                       message=f"Следующих пользователей нет в базе данных:{new_line}{f'{new_line}'.join(list(set(bad_users)))}")
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
            messagebox.showwarning(title='Warning!',
                                   message=f"Вы не заполнили все обязательные поля:{new_line} {new_line.join(self.necess.values())}")
        else:
            if self.my_name.get() == '':
                messagebox.showwarning(title='Warning!', message=f"Вы не представились")
            else:
                rem_event = MyEvent(name=self.event_params['name_event_val'].get(),
                                    start=int(self.event_params['start_event_val'].get()),
                                    end=int(self.event_params['end_event_val'].get()),
                                    participants=parse_partisipants(self.event_params['participatns_val'].get()),
                                    description=self.event_params['descr_val'].get(),
                                    place=self.event_params['place_val'].get(),
                                    priority=int(self.event_params['prior_val'].get()),
                                    remind_value=int(self.event_params['rem_val'].get()))
                user = find_user_by_login(self.my_name.get())
                if user.name == 'NoUser':
                    messagebox.showwarning(title='Warning!',
                                           message=f"Не существует пользователя с логином {self.my_name.get()}")
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
            entries[-1].grid(row=i + 1, column=1)

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


class UICalendar:
    def __init__(self, fr):
        self.fr = fr
        self.out_cal = StringVar()
        self.printUI()

    def write_calendar(self):
        name = self.out_cal.get()
        events = self.fr.calendar.get_information(name)
        if events is None:
            messagebox.showwarning(title='Warning!', message=f"Вы ввели некорретный департамент или пользователя")
        else:
            Window_events(self.fr, [str(i.to_json()) for i in events])

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
