import pandas as pd
import random

class User:
    def __init__(self, name, grade, mail, department):
        self.name = name
        self.grade = grade
        self.mail = mail
        self.department = department

    def __eq__(self, other):
        return self.mail == other.mail

df = pd.read_csv('/Users/homdanil153/Downloads/AL.tsv', sep='\t')
names = list(df['ФИО'])
grades = [random.randint(13, 20) for i in range(len(df))]
emails = list(df['Почта'])
departments = [str(i) for i in list(df['группа'])]

list_users = [User(name, grade, email, dep) for name, grade, email, dep in zip(names, grades, emails, departments)]
list_departs = list(set(departments))

class Calendar:
    def __init__(self, events=[], current_time=0, log_events=[]):
        self.events = events
        self.current_time = current_time
        self.log_events = log_events

    def clear_calendar(self):
        rem_events = []
        for event in self.events:
            if event.end < self.current_time:
                self.log_events.append(event)
                rem_events.append(event)
        for event in rem_events:
            self.events.remove(event)

    def send_mail_to_user(self, mail, message):
        print(f"Напоминание отправленно пользователю {mail}")


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
        if self.current_time > event.start:
            return False, "Вы не можете поставить встречу в прошлое!"
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
        if name == "Календарь" or name == '':
            return self.events
        else:
            for dep in list_departs:
                if dep == name:
                    return [i for i in self.events if i.check_department_event(dep)]
            for user in list_users:
                if name == user.mail:
                    return [i for i in self.events if i.is_participant(user)]
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