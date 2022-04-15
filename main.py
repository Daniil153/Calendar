from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
import sys
from GUI import UIEvent, UICalendar
from UI import Calendar

new_line = '\n'


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
        messagebox.showinfo(title='Help',
                            message="1) Чтобы добавить или удалить событие обязательно заполните поля Название, Начало, Участники, Место. \n\n"
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
