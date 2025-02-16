from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivy.uix.screenmanager import Screen,ScreenManager
from kivy.lang import Builder
from kivy.app import App
from kivymd.uix.textfield import MDTextField
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from kivy.core.window import Window
import sqlite3
from kivy.clock import Clock
from datetime import datetime, timedelta
from plyer import notification
import os


class LoginPage(Screen):
    pass

class History(Screen):
    pass

class ModifyCarPage(Screen):
    pass

class HomePage(Screen):
    pass

class ForgotUsername(Screen):
    pass

class AddCarPage(Screen):
    pass

class WindowManager(ScreenManager):
    pass

class MyCars(MDApp):

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"

        conn = sqlite3.connect('car_test.db')
        cursor = conn.cursor()

        # Create user table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS user(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email VARCHAR(50) UNIQUE,
            password VARCHAR(50)
        )
        ''')

        cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS masini( 
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_user INTEGER,
            marca VARCHAR(50),
            tipul_masinii VARCHAR(50),
            numar_de_inmatriculare VARCHAR(50) UNIQUE,
            seria VARCHAR(20) UNIQUE,
            ITP VARCHAR(50),
            rovineta VARCHAR(50),
            asigurare VARCHAR(50),
            licenta VARCHAR(50),
            tahograf VARCHAR(50),
            FOREIGN KEY (id_user) REFERENCES user(id)
        )
        ''')

        conn.commit()
        conn.close()
        self.user_id = None
        return Builder.load_file('MyCars.kv')

    def logger(self):
        app=MyCars.get_running_app()
        self.ids = app.root.get_screen('login').ids
        email=self.ids.email.text
        password=self.ids.password.text
        conn = sqlite3.connect('car_test.db')
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM user WHERE email = :email AND password = :password",
            {
                'email': email,
                'password': password
            }
        )
        users = cursor.fetchall()
        if users:
            self.user_id = users[0][0]
            app.root.current = "home"
        else:
            self.dialog = MDDialog(title='Utilizator', text="Nu exista utilizator cu aceste date",
                                   buttons=[MDRectangleFlatButton(text='Inapoi', on_press=self.close_dialog)])
            self.dialog.open()
        conn.commit()
        conn.close()


    def add_user(self):
        app = MyCars.get_running_app()
        self.ids = app.root.get_screen('forgot').ids
        email = self.ids.new_email.text
        password = self.ids.new_password.text
        confirm_password = self.ids.confirm_password.text
        conn = sqlite3.connect('car_test.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user WHERE email = :email",
                       {
                           'email': email
                       })
        users = cursor.fetchall()
        if password != confirm_password :
            self.dialog = MDDialog(title='Incercati din nou',
                                   buttons=[MDRectangleFlatButton(text='Inapoi', on_press=self.close_dialog)])
            self.dialog.open()
        else:
            if email is not "":
                cursor.execute("INSERT INTO user(email, password) VALUES (:email, :password)",
                {
                    'email': email,
                    'password': password
                })
                self.dialog = MDDialog(title='Bun venit ',
                                       buttons=[MDRectangleFlatButton(text='Inapoi', on_press=self.close_dialog)])
                self.dialog.open()

            else:
                self.dialog = MDDialog(title='Incercati din nou',
                                       buttons=[MDRectangleFlatButton(text='Inapoi', on_press=self.close_dialog)])
                self.dialog.open()
        conn.commit()
        conn.close()

    def close_dialog(self, obj):
        self.dialog.dismiss()

    def add_car(self):
        app = MyCars.get_running_app()
        self.ids = app.root.get_screen('addcar').ids
        marca = self.ids.marca.text
        tip = self.ids.tip.text
        inmatriculare = self.ids.inmatriculare.text
        id = self.ids.identificare.text
        itp = self.ids.itp.text
        rovineta = self.ids.rovineta.text
        asigurare = self.ids.asigurare.text
        licenta = self.ids.licenta.text
        tahograf = self.ids.tahograf.text
        conn = sqlite3.connect('car_test.db')
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO masini(id_user, marca, tipul_masinii, numar_de_inmatriculare, seria, ITP, rovineta, asigurare, licenta, tahograf)
                       VALUES (:id_user, :marca, :tip, :inmatriculare, :seria, :itp, :rovineta, :asigurare, :licenta, :tahograf)''',
        {   "marca":marca,
            "tip":tip,
            "inmatriculare":inmatriculare,
            "seria":id,
            "itp":itp,
            "rovineta":rovineta,
            "asigurare":asigurare,
            "licenta":licenta,
            "tahograf":tahograf,
            'id_user': self.user_id
         })
        self.ids.label_add.text=''
        self.ids.marca.text=''
        self.ids.tip.text=''
        self.ids.inmatriculare.text=''
        self.ids.identificare.text=''
        self.ids.itp.text=''
        self.ids.rovineta.text=''
        self.ids.asigurare.text=''
        self.ids.licenta.text=''
        self.ids.tahograf.text=''
        conn.commit()
        conn.close()

    def show_records(self):
        app = MyCars.get_running_app()
        screen = app.root.get_screen('istoric')

        conn = sqlite3.connect('car_test.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * from masini where id_user=:id_user", {'id_user': self.user_id})
        records = cursor.fetchall()

        column_data = [
            ("Marca", dp(30)),
            ("Tipul", dp(30)),
            ("Numarul de inmatriculare", dp(30)),
            ("Seria", dp(30))
        ]

        row_data = [
            (str(record[2]), str(record[3]), str(record[4]), str(record[5])) for record in records
        ]
        table = MDDataTable(
            size_hint=(0.9, 0.6),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            column_data=column_data,
            row_data=row_data,
        )

        screen.add_widget(table)
        conn.close()

    def find_car(self):
        self.dialog = MDDialog(title='Cauta masina dupa: ',
                               buttons=[MDRectangleFlatButton(text='Inapoi', on_press=self.close_dialog),MDRectangleFlatButton(text='Numar de inmatriculare', on_press=self.nr_matriculare),MDRectangleFlatButton(text='Seria', on_press=self.seria)])
        self.dialog.open()

    def nr_matriculare(self, obj):
        self.dialog.dismiss()
        self.nr_input = MDTextField(
            hint_text='Introduceti un numar de inmatriculare',
            helper_text="",
            helper_text_mode="on_focus",
            multiline=False,
            mode="fill",
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        button1 = MDRectangleFlatButton(text='Inapoi', on_press=self.close_dialog)
        button2 = MDRectangleFlatButton(text='Cautati', on_press=self.search_nr_matriculare)
        self.dialog = MDDialog(
            text='Cauta masina dupa numarul de inmatriculare',
            buttons=[button1, button2],
            type="custom",
            content_cls=self.nr_input
        )
        self.dialog.open()

    def modify(self):
        app = MyCars.get_running_app()
        self.ids = app.root.get_screen('modifica').ids
        marca = self.ids.marca.text
        tip = self.ids.tip.text
        inmatriculare = self.ids.inmatriculare.text
        id = self.ids.identificare.text
        itp = self.ids.itp.text
        rovineta = self.ids.rovineta.text
        asigurare = self.ids.asigurare.text
        licenta = self.ids.licenta.text
        tahograf = self.ids.tahograf.text

        conn = sqlite3.connect('car_test.db')
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE masini 
            SET marca=:marca,
                tipul_masinii=:tip,
                numar_de_inmatriculare=:inmatriculare,
                seria=:id,
                ITP=:itp,
                rovineta=:rovineta,
                asigurare=:asigurare,
                licenta=:licenta,
                tahograf=:tahograf
            WHERE numar_de_inmatriculare=:inmatriculare
            """, {
                'marca': marca,
                'tip': tip,
                'inmatriculare': inmatriculare,
                'id': id,
                'itp': itp,
                'rovineta': rovineta,
                'asigurare': asigurare,
                'licenta': licenta,
                'tahograf': tahograf
            }
        )
        self.ids.label_add.text = ''
        self.ids.marca.text = ''
        self.ids.tip.text = ''
        self.ids.inmatriculare.text = ''
        self.ids.identificare.text = ''
        self.ids.itp.text = ''
        self.ids.rovineta.text = ''
        self.ids.asigurare.text = ''
        self.ids.licenta.text = ''
        self.ids.tahograf.text = ''

        conn.commit()
        conn.close()

    def search_nr_matriculare(self, obj):
        nr_matriculare_value = self.nr_input.text
        conn = sqlite3.connect('car_test.db')
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM masini WHERE id_user=:id_user AND numar_de_inmatriculare=:nr_matriculare",
            {'id_user': self.user_id, 'nr_matriculare': nr_matriculare_value}
        )
        car = cursor.fetchone()
        conn.close()
        if car:
            app = MyCars.get_running_app()
            self.ids = app.root.get_screen('modifica').ids
            self.ids.marca.text = car[2]
            self.ids.tip.text = car[3]
            self.ids.inmatriculare.text = car[4]
            self.ids.identificare.text = car[5]
            self.ids.itp.text = car[6]
            self.ids.rovineta.text = car[7]
            self.ids.asigurare.text = car[8]
            self.ids.licenta.text = car[9]
            self.ids.tahograf.text = car[10]
            self.dialog.dismiss()
            app.root.current = 'modifica'
        else:
            self.dialog = MDDialog(
                title='Rezultat Cautare',
                text="Nu exista aceasta masina",
                buttons=[MDRectangleFlatButton(text='Inapoi', on_press=self.close_dialog)]
            )
            self.dialog.open()

    def close_dialog(self, obj):
        self.dialog.dismiss()

    def seria(self,obj):
        self.dialog.dismiss()
        self.nr_input = MDTextField(
            hint_text='Introduceti seria masinii',
            helper_text="",
            helper_text_mode="on_focus",
            multiline=False,
            mode="fill",
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        button1 = MDRectangleFlatButton(text='Inapoi', on_press=self.close_dialog)
        button2 = MDRectangleFlatButton(text='Cautati', on_press=self.search_seria)
        self.dialog = MDDialog(
            text='Cauta masina dupa serie',
            buttons=[button1, button2],
            type="custom",
            content_cls=self.nr_input
        )
        self.dialog.open()

    def search_seria(self, obj):
        seria = self.nr_input.text
        conn = sqlite3.connect('car_test.db')
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM masini WHERE id_user=:id_user AND seria=:seria",
            {'id_user': self.user_id, 'seria': seria}
        )
        car = cursor.fetchone()
        conn.close()
        if car:
            app = MyCars.get_running_app()
            self.ids = app.root.get_screen('modifica').ids
            self.ids.marca.text = car[2]
            self.ids.tip.text = car[3]
            self.ids.inmatriculare.text = car[4]
            self.ids.identificare.text = car[5]
            self.ids.itp.text = car[6]
            self.ids.rovineta.text = car[7]
            self.ids.asigurare.text = car[8]
            self.ids.licenta.text = car[9]
            self.ids.tahograf.text = car[10]
            self.dialog.dismiss()
            app.root.current = 'modifica'
        else:
            self.dialog = MDDialog(
                title='Rezultat Cautare',
                text="Nu exista aceasta masina",
                buttons=[MDRectangleFlatButton(text='Inapoi', on_press=self.close_dialog)]
            )
            self.dialog.open()
    def sterge_nr_matriculare(self,obj):
        self.dialog.dismiss()
        self.nr_input = MDTextField(
            hint_text='Introduceti numarul de inmatriculare al masinii',
            helper_text="",
            helper_text_mode="on_focus",
            multiline=False,
            mode="fill",
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        button1 = MDRectangleFlatButton(text='Inapoi', on_release=self.close_dialog)
        button2 = MDRectangleFlatButton(text='Stergeti', on_release=self.sterge_dupa_nrm)
        self.dialog = MDDialog(
            text='Stergere masina dupa numarul de inmatriculare',
            buttons=[button1, button2],
            type="custom",
            content_cls=self.nr_input
        )
        self.dialog.open()

    def sterge_seria(self, obj):
        self.dialog.dismiss()
        self.nr_input = MDTextField(
            hint_text='Introduceti seria masinii',
            helper_text="",
            helper_text_mode="on_focus",
            multiline=False,
            mode="fill",
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        button1 = MDRectangleFlatButton(text='Inapoi', on_release=self.close_dialog)
        button2 = MDRectangleFlatButton(text='Stergeti', on_release=self.sterge_dupa_serie)
        self.dialog = MDDialog(
            text='Stergere masina dupa serie',
            buttons=[button1, button2],
            type="custom",
            content_cls=self.nr_input
        )
        self.dialog.open()

    def sterge_dupa_serie(self, obj):
        seria = self.nr_input.text
        conn = sqlite3.connect('car_test.db')
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM masini WHERE id_user=:id_user AND seria=:seria",
            {'id_user': self.user_id, 'seria': seria}
        )
        car = cursor.fetchone()
        if car:
            cursor.execute('''DELETE FROM masini WHERE seria=:seria''', {'seria': seria})
            conn.commit()
            self.dialog.dismiss()
            self.dialog = MDDialog(
                title='Rezultat Stergere',
                text="Stergere realizata cu succes",
                buttons=[MDRectangleFlatButton(text='Inapoi', on_release=self.close_dialog)]
            )
            self.dialog.open()
        else:
            self.dialog.dismiss()
            self.dialog = MDDialog(
                title='Rezultat Stergere',
                text="Nu exista aceasta masina",
                buttons=[MDRectangleFlatButton(text='Inapoi', on_release=self.close_dialog)]
            )
            self.dialog.open()
        conn.close()

    def sterge_dupa_nrm(self,obj):
        numar_de_inmatriculare = self.nr_input.text
        conn = sqlite3.connect('car_test.db')
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM masini WHERE id_user=:id_user AND numar_de_inmatriculare=:numar_de_inmatriculare",
            {'id_user': self.user_id, 'numar_de_inmatriculare': numar_de_inmatriculare}
        )
        car = cursor.fetchone()
        if car:
            cursor.execute('''DELETE FROM masini WHERE numar_de_inmatriculare=:numar_de_inmatriculare''', {'numar_de_inmatriculare': numar_de_inmatriculare})
            conn.commit()
            self.dialog.dismiss()
            self.dialog = MDDialog(
                title='Rezultat Stergere',
                text="Stergere realizata cu succes",
                buttons=[MDRectangleFlatButton(text='Inapoi', on_release=self.close_dialog)]
            )
            self.dialog.open()
        else:
            self.dialog.dismiss()
            self.dialog = MDDialog(
                title='Rezultat Stergere',
                text="Nu exista aceasta masina",
                buttons=[MDRectangleFlatButton(text='Inapoi', on_release=self.close_dialog)]
            )
            self.dialog.open()
        conn.close()

    def delete_car(self,obj=None):
        self.dialog = MDDialog(title='Sterge masina dupa: ',
                               buttons=[MDRectangleFlatButton(text='Inapoi', on_press=self.close_dialog),
                                        MDRectangleFlatButton(text='Numar de inmatriculare',
                                                              on_press=self.sterge_nr_matriculare),
                                        MDRectangleFlatButton(text='Seria', on_press=self.sterge_seria)])
        self.dialog.open()


if __name__ == '__main__':
    MyCars().run()

