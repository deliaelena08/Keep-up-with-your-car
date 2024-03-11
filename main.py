from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivy.uix.screenmanager import Screen,ScreenManager
from kivy.lang import Builder
from kivy.app import App
from kivymd.uix.textfield import MDTextField
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRectangleFlatButton
from kivy.core.window import Window
import sqlite3


class LoginPage(Screen):
    pass

class History(Screen):
    pass

class HomePage(Screen):
    pass

class ForgotUsername(Screen):
    pass

class AddCarPage(Screen):
    pass

class WindowManager(ScreenManager):
    pass

username_list=[]
class MyCars(MDApp):

    def build(self):
        self.theme_cls.theme_style="Dark"
        self.theme_cls.primary_palette="BlueGray"
        conn=sqlite3.connect('car_data2.db')
        cursor=conn.cursor()
        cursor.execute(''' CREATE TABLE if not exists masini( 
        Marca varchar(50),
        Tipul_masinii varchar(50),
        Numar_de_inmatriculare varchar(50),
        Seria varchar(20),
        ITP varchar(50),
        Rovineta varchar(50),
        Asigurare varchar(50),
        Licenta varchar(50),
        Tahograf varchar(50)
        )
        ''')

        conn.commit()
        conn.close()

        conn = sqlite3.connect('car_data2.db')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE if not exists user(
                Id integer PRIMARY KEY,
                Username varchar(50)
                )
                ''')
        conn.commit()
        conn.close()

        return Builder.load_file('MyCars.kv')


    def logger(self):
        app=MyCars.get_running_app()
        self.ids=app.root.get_screen('login').ids
        name=self.ids.username.text
        conn = sqlite3.connect('car_data2.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * from user")
        users=cursor.fetchall()
        for u in users:
            username_list.append(u[1])
        conn.commit()
        conn.close()
        if name not in username_list:
            self.dialog = MDDialog(title='Numele utilizatorului:', text="Nu este valid",
                                   buttons=[MDRectangleFlatButton(text='Inapoi', on_press=self.close_dialog)])
            self.dialog.open()
        else:
            app.root.current="home"


    def add_user(self):
        app = MyCars.get_running_app()
        self.ids = app.root.get_screen('forgot').ids
        name = self.ids.new_username.text
        conn = sqlite3.connect('car_data2.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * from user")
        users = cursor.fetchall()
        if name is not "":
            cursor.execute("INSERT INTO user(username) VALUES (:username)",
            {
                "username":name
            })
            self.dialog = MDDialog(title='Bun venit ', text=name,
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
        tip=self.ids.tip.text
        inmatriculare=self.ids.inmatriculare.text
        id=self.ids.identificare.text
        itp=self.ids.itp.text
        rovineta=self.ids.rovineta.text
        asigurare=self.ids.asigurare.text
        licenta=self.ids.licenta.text
        tahograf= self.ids.tahograf.text
        conn = sqlite3.connect('car_data2.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO masini VALUES (:marca,:tip,:inmatriculare,:seria,:itp,:rovineta,:asigurare,:licenta,:tahograf)",
        {   "marca":marca,
            "tip":tip,
            "inmatriculare":inmatriculare,
            "seria":id,
            "itp":itp,
            "rovineta":rovineta,
            "asigurare":asigurare,
            "licenta":licenta,
            "tahograf":tahograf
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
        screen=app.root.get_screen('istoric')
        conn = sqlite3.connect('car_data2.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * from masini")
        '''
        cursor.execute("SELECT * from masini where Numar_de_inmatriculare = :nr", {
        
            "nr" : numar_de_in...
        })
        '''
        records=cursor.fetchall()
        text=''
        for record in records:
            word = "Marca= " + str(record[0]) + ',' + "Tipul= " + str(record[1]) + ',' + "Numarul de inmatriculare= " + str(
                record[2]) +','+"Seria= "+str(record[3])+ '\n'
            text += word
        label=MDLabel(pos_hint= {"center_x": 0.5, "center_y": .9},text=text,font_size='16sp')
        screen.add_widget(label)
        conn.commit()
        conn.close()

    def find_car(self):
        self.dialog = MDDialog(title='Cauta masina dupa: ',
                               buttons=[MDRectangleFlatButton(text='Inapoi', on_press=self.close_dialog),MDRectangleFlatButton(text='Numar de inmatriculare', on_press=self.nr_matriculare),MDRectangleFlatButton(text='Seria', on_press=self.seria)])
        self.dialog.open()

    def nr_matriculare(self,obj):
        self.dialog.dismiss()
        text_field=MDTextField(id='nrmatricol',hint_text='Introduceti un numar de inmatricuare',helper_text="",
            helper_text_mode="on_focus",multiline=False,mode="fill",pos_hint={'x':0.5,'y':0.5})
        button1=MDRectangleFlatButton(text='Inapoi', on_press=self.close_dialog)
        button2=MDRectangleFlatButton(text='Cautati')
        self.dialog=MDDialog(text='',buttons=[button1,button2],type="custom",content_cls=text_field)
        self.dialog.open()

    def seria(self,obj):
        self.dialog.dismiss()
        text_field=MDTextField(id='seria',hint_text="Introduceti o serie",helper_text=''
                               ,helper_text_mode="on_focus",multiline=False,mode="fill")
        button1 = MDRectangleFlatButton(text='Inapoi', on_press=self.close_dialog)
        button2 = MDRectangleFlatButton(text='Cautati')
        self.dialog = MDDialog(text='', buttons=[button1, button2],type="custom",content_cls=text_field)
        self.dialog.open()

if __name__ == '__main__':
    MyCars().run()

