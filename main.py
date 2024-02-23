#Импорт всех необходимых модулей
import sqlite3
import tkinter as tk
from tkinter import ttk

#Класс главного окна
class Main(tk.Frame):
    def __init__(self,root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()   

    #Хранениние и инициализация объектов GUI
    def init_main(self):
        #Создание панели инструментов
        toolbar = tk.Frame(bg = '#F0E68C', bd = 2)
        #Масштабируем и размещаем
        toolbar.pack(side=tk.TOP, fill=tk.X)
        
        #Создаём кнопку добавления
        self.add_img = tk.PhotoImage(file = 'img/add.png')
        btn_open_dialog = tk.Button(toolbar, bg = '#F0E68C', bd = 0, image=self.add_img, 
                                    command = self.open_dialog)
        btn_open_dialog.pack(side = tk.LEFT)

        #Создаём кнопку изменения
        self.update_image = tk.PhotoImage(file = 'img/update.png')
        btn_edit_dioalog = tk.Button(toolbar, bg = '#F0E68C', 
                                     bd = 0, image = self.update_image,
                                     command = self.open_update_dialog)
        btn_edit_dioalog.pack(side = tk.LEFT)

        #Создаём кнопку удаления
        self.delete_image = tk.PhotoImage(file = 'img/delete.png')
        button_delete = tk.Button(toolbar, bg = '#F0E68C', image = self.delete_image,
                                  bd = 0, command = self.delete_records)
        button_delete.pack(side = tk.LEFT)

        #Создаём кнопку поиска
        self.search_image = tk.PhotoImage(file = 'img/search.png')
        button_search = tk.Button(toolbar, bg = '#F0E68C', image = self.search_image,
                                  bd = 0, command = self.open_search_dialog)
        button_search.pack(side = tk.LEFT)

        #Создаём кнопку обновления
        self.refresh_image = tk.PhotoImage(file = 'img/refresh.png')
        button_refresh = tk.Button(toolbar, bg = '#F0E68C', image = self.refresh_image,
                                  bd = 0, command = self.view_records)
        button_refresh.pack(side = tk.LEFT)


        #Добавляем столбцы, высоту и скрываем пустую колонку таблицы
        self.tree = ttk.Treeview(self, columns = ['ID', 'name', 'number_phone', 'email', 'salary'], 
                            height = 45, show = 'headings')
        
        #Добавляем параметры
        self.tree.column('ID', width = 30, anchor = tk.CENTER)
        self.tree.column('name', width = 300, anchor = tk.CENTER)
        self.tree.column('number_phone', width = 150, anchor = tk.CENTER)
        self.tree.column('email', width = 150, anchor = tk.CENTER)
        self.tree.column('salary', width = 100, anchor = tk.CENTER)

        #Добавляем заголовки
        self.tree.heading('ID', text = 'ID')
        self.tree.heading('name', text = 'ФИО')
        self.tree.heading('number_phone', text = 'Номер телефона')
        self.tree.heading('email', text = 'Почта')
        self.tree.heading('salary', text = 'Зарплата')

        #Упаковываем
        self.tree.pack(side = tk.LEFT)
        
        scroll = tk.Scrollbar(self, command = self.tree.yview)
        scroll.pack(side = tk.LEFT, fill = tk.Y)
        self.tree.configure(yscrollcommand = scroll.set)

    #Вызов дочернего окна
    def open_dialog(self):
        Child()

    #Добавление данных
    def records(self, name, number_phone, email, salary):
        self.db.insert_data(name, number_phone, email, salary)
        self.view_records()

    #Вывод данных в виджет таблицы
    def view_records(self):
        #Выбираем информацию
        self.db.cursor.execute('''SELECT * FROM db''')
        #Удаляем всё из виджета таблицы
        [self.tree.delete(i) for i in self.tree.get_children()]
        #Добавляем в виджет информацию из базы данных
        [self.tree.insert('', 'end', values = row) for row in self.db.cursor.fetchall()]

    #Вызов окна редактирования
    def open_update_dialog(self):
        Update()

    #Обновление данных
    def update_record(self, name, number_phone, email, salary):
        self.db.connect.execute(
            '''
UPDATE db SET name=?, number_phone=?, email=?, salary=? WHERE ID = ?''', 
(name, number_phone, email, salary,
 self.tree.set(self.tree.selection()[0], '#1')))
        self.db.connect.commit()
        self.view_records()

    #Удаление записей
    def delete_records(self):
        #Выбор выделенных записей
        for selection_item in self.tree.selection():
            #Удаление из базы данных
            self.db.cursor.execute('''
DELETE FROM db WHERE id= ?''', (self.tree.set(selection_item, '#1'),))
        #Сохранение
        self.db.connect.commit()
        #Обновление изменённой информации
        self.view_records()

    #Вызов окна поиска
    def open_search_dialog(self):
        Search()

    #Поиск записи
    def search_records(self, name):
        name = ('%' + name + '%')
        self.db.cursor.execute('''SELECT * FROM db WHERE name LIKE ?''', (name,))
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.cursor.fetchall()]

#Класс дочерних окон
class Child(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_child()
        self.view = app

    def init_child(self):
        self.title('Добавить')
        self.geometry('450x250')
        self.iconbitmap('img/ico.ico')
        self.resizable(False, False)
        #Перехват событий в приложении
        self.grab_set()
        #Захват фокуса
        self.focus_set()

        #Создание фона окна
        self.refresh_image = tk.PhotoImage(file = 'img/fon.png')
        label_fon = tk.Label(self, image = self.refresh_image)
        label_fon.place(x = 0, y = 0)


        #Подписи
        label_name = tk.Label(self, text = 'ФИО')
        label_name.place(x = 50, y = 50)

        label_selest = tk.Label(self, text = 'Номер телефона')
        label_selest.place(x = 50, y = 80)

        label_selest = tk.Label(self, text = 'Почта')
        label_selest.place(x = 50, y = 110)

        label_selest = tk.Label(self, text = 'Зарплата')
        label_selest.place(x = 50, y = 140)


        #Добавление полей для ввода
        self.entry_name = ttk.Entry(self)
        self.entry_name.place(x = 200, y = 50)

        self.entry_email = ttk.Entry(self)
        self.entry_email.place(x = 200, y = 80)

        self.entry_number = ttk.Entry(self)
        self.entry_number.place(x = 200, y = 110)

        self.entry_salary = ttk.Entry(self)
        self.entry_salary.place(x = 200, y = 140)

        #Добавление кнопки "Закрыть" для дочернего окна
        self.button_cancel = ttk.Button(self, text = 'Закрыть', command = self.destroy)
        self.button_cancel.place(x = 270, y = 170)

        #Добавление кнопки "Добавить"
        self.button_ok = ttk.Button(self, text = 'Добавить')
        self.button_ok.place(x = 190, y = 170)
        #Передача значений из строк ввода
        self.button_ok.bind('<Button-1>',
                            lambda event: self.view.records(
                                self.entry_name.get(),
                                self.entry_email.get(),
                                self.entry_number.get(),
                                self.entry_salary.get()))
        

#Класс окна для добавления
class Update(Child):
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.view = app
        self.db = db
        self.defoult_data()

    def init_edit(self):
        self.title('Редактировать текст')
        btn_edit = ttk.Button(self, text = 'Редактировать')
        btn_edit.place(x = 175, y = 170)
        btn_edit.bind('<Button-1>', lambda event:
                      self.view.update_record(self.entry_name.get(),
                                              self.entry_email.get(),
                                              self.entry_number.get(),
                                              self.entry_salary.get()))
        #Закрываем окно редактирования
        btn_edit.bind('<Button-1>', lambda event:
                      self.destroy(), add='+')
        self.button_ok.destroy()

    def defoult_data(self):
        self.db.cursor.execute(
            '''
SELECT * FROM db WHERE id = ?''',
(self.view.tree.set(self.view.tree.selection()[0], '#1'),))
        #Получаем доступ к первой записи из выборки
        row = self.db.cursor.fetchone()
        self.entry_name.insert(0, row[1])
        self.entry_email.insert(0, row[2])
        self.entry_number.insert(0, row[3])
        self.entry_salary.insert(0, row[4])

#Класс для поиска контакта
class Search(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_search()
        self.view = app

    def init_search(self):
        self.title('Поиск')
        self.geometry('300x100')
        self.iconbitmap('img/ico_search.ico')
        self.resizable(False, False)
        
        #Создание поля ввода поиск
        label_search = tk.Label(self, text = 'Поиск')
        label_search.place(x = 50, y = 20)

        self.entry_search = ttk.Entry(self)
        self.entry_search.place(x = 105, y = 20, width = 150)

        #Создание кнопки закрыть
        button_cancel = ttk.Button(self, text = 'Закрыть', command = self.destroy)
        button_cancel.place(x=185, y=50)
        
        #Создание кнопки поиск
        button_search = ttk.Button(self, text = 'Поиск')
        button_search.place(x = 105, y = 50)
        button_search.bind('<Button-1>', lambda event:
                           self.view.search_records(self.entry_search.get()))
        button_search.bind('<Button-1>', lambda event: 
                           self.destroy(), add = '+')

#Класс базы данных
class DB:
    def __init__(self):
        #Подключаемся к нашей базе данных
        self.connect = sqlite3.connect('Contacts.db')
        #Создаём объект для взаимодействия с базой данных
        self.cursor = self.connect.cursor()
        #Создание таблицы
        self.cursor.execute('''
CREATE TABLE IF NOT EXISTS db 
                            (id integer primary key, name text, number_phone text, email text, salary text)
                            ''')
        #Сохранение
        self.connect.commit()

    #Добавление контакта в базу данных
    def insert_data(self, name, number_phone, email, salary):
        self.cursor.execute('''
INSERT INTO db (name, number_phone, email, salary) VALUES(?, ?, ?, ?)''', 
(name, number_phone, email, salary))
        self.connect.commit()


if __name__ == '__main__':
    #Инициализируем Tkinter
    root = tk.Tk()
    #Экземпляр класса DB
    db = DB()
    #Экземпляр главного класса Main
    app = Main(root)
    #"Запаковываем" для получения интерфейса
    app.pack()
    #Заголовок окна
    root.title('Список сотрудников компании')
    #Иконка
    root.iconbitmap('img/ico.ico')
    #Размер окна
    root.geometry('770x500')
    #Запрет на изменение размера экрана
    root.resizable(False, False)
    #Цикл для постоянного отображения окна
    root.mainloop()