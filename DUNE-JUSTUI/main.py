from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.uix.menu import MDDropdownMenu
from kivy.network.urlrequest import UrlRequest
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.spinner import MDSpinner
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.label import MDLabel
from kivy.core.window import Window
from kivy.clock import Clock
import certifi as cfi
import socket
from math import ceil

class Main(Screen):
    pass
  
class Content(BoxLayout):
    pass

class MainApp(MDApp):
    def check_internet(self):
        try:
            # Attempt to connect to a well-known website
            socket.create_connection(("www.google.com", 80))
            return True
        except OSError:
            return False

    def clear_helper_text(self, instance):
        if instance.helper_text_mode == "on_error" and not instance.error:
            instance.helper_text = ""
        elif instance.error and not instance.focus:
            instance.helper_text = "Enter numbers only."

    def is_float(self, string):
            try:
                float(string)
                return True
            except ValueError:
                return False
                
    def validate_inputs(self):
        input_fields = [
            self.root.get_screen('main').ids.input_1, 
            self.root.get_screen('main').ids.input_2,
            self.root.get_screen('main').ids.input_6, 
            self.root.get_screen('main').ids.input_7, 
            self.root.get_screen('main').ids.input_8,
            ]

        for field in input_fields:
            if not field.text:
                self.show_missing_input_dialog()
                return False
        flag=0
        for field in input_fields:
            if not self.is_float(field.text):
                field.error = True
                field.helper_text = "Enter in numbers."
                flag=1
        if flag==1:
            return False
        else:
            return True
    

    def show_missing_input_dialog(self):
        self.dialog = MDDialog(
            title="Missing Inputs",
            text="Please fill all the fields.",
            md_bg_color=(105/256, 105/256, 105/256, 0.24),
            buttons=[MDRectangleFlatButton(text="OK", on_release=self.dismiss_dialog)],
            auto_dismiss=False,
        )
        self.dialog.open()

    def dismiss_dialog(self,obj):
        self.dialog.dismiss()

    def show_fuel_menu(self, item, id):
        menu_items = [
            {
                "text": "Petrol",
                "on_release": lambda x="Petrol": self.menu_callback(x, id,dropdown)
            },
            {
                "text": "Diesel",
                "on_release": lambda x="Diesel": self.menu_callback(x, id,dropdown)
            }
        ]
        dropdown=MDDropdownMenu(caller=item, items=menu_items,position="bottom", width=4)
        dropdown.open()

    def show_Transmission_menu(self, item, id):
        menu_items = [
            {
                "text": "Manual",
                "on_release": lambda x="Manual": self.menu_callback(x, id,dropdown)
            },
            {
                "text": "Auto",
                "on_release": lambda x="Auto": self.menu_callback(x, id,dropdown)
            }
        ]
        dropdown=MDDropdownMenu(caller=item, items=menu_items,position="bottom", width=4)
        dropdown.open()
    def show_Owner_menu(self, item, id):
        menu_items = [
            {
                "text": "1",
                "on_release": lambda x="1": self.menu_callback(x, id,dropdown)
            },
            {
                "text": "2",
                "on_release": lambda x="2": self.menu_callback(x, id,dropdown)
            },
            {
                "text": "3",
                "on_release": lambda x="3": self.menu_callback(x, id,dropdown)
            },
        ]
        dropdown=MDDropdownMenu(caller=item, items=menu_items,position="bottom", width=4)
        dropdown.open()

    def menu_callback(self, text_item, id,dropdown):
        self.root.get_screen('main').ids[id].text = text_item
        dropdown.dismiss()

    def build(self):
        self.msg=None
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        self.dialogs = MDDialog(type="custom",content_cls=Content(),auto_dismiss=False)
        Clock.schedule_interval(self.check_and_notify, 5)
        sm = ScreenManager()
        sm.add_widget(Main(name='main'))
        return sm
    
    def check_and_notify(self, dt):
        if not self.check_internet() and not self.msg:
            
            self.msg = MDDialog(
                text=" No Internet",
                md_bg_color=(1, 0, 0, 0.6),
                pos_hint={'top':1},
                auto_dismiss=False,
            )
            self.msg.open()
        elif self.check_internet():
            self.dismiss_dialogs()
    def dismiss_dialogs(self, *args):
        if self.msg:
            self.msg.dismiss()
            self.msg = None

    def predict(self):
        
        if not self.validate_inputs():
            return
        input_1 = self.root.get_screen('main').ids.input_1.text #year
        input_2 = self.root.get_screen('main').ids.input_2.text #kilometers_driven
        selected_fuel = self.root.get_screen('main').ids.drop_item.text #fuel_Type
        input_3 = 1 if selected_fuel == 'Petrol' else 0
        selected_transmission = self.root.get_screen('main').ids.drop_item1.text #transmisson
        input_4 = 0 if selected_transmission == 'Manual' else 1
        selected_owner = self.root.get_screen('main').ids.drop_item2.text #owner_Type
        input_5 = int(selected_owner) - 1
        input_6 = self.root.get_screen('main').ids.input_6.text #Mileage
        input_7 = self.root.get_screen('main').ids.input_7.text #Engine_capacity
        input_8 = self.root.get_screen('main').ids.input_8.text #Power
        self.dialogs.open()
        url = f'https://flask-api-xgb-new.onrender.com/predict?input_1={input_1}&input_2={input_2}&input_3={input_3}&input_4={input_4}&input_5={input_5}&input_6={input_6}&input_7={input_7}&input_8={input_8}'
        self.request = UrlRequest(url=url, on_success=self.res,on_failure=self.fail,ca_file=cfi.where(), verify=True)
    def res(self, *args):       
        self.data = self.request.result
        if(len(self.data)):
            self.dialogs.dismiss()                
        ans = self.data
        prediction_text = (ceil(ans['prediction']))
        number =  prediction_text
        rounded_number = round(number / 100000, 1)

        self.dialog=MDDialog(text=f"Price of the car is  {rounded_number} Lakhs",elevation=10,
        md_bg_color=(105/256, 105/256, 105/256, 0.4),
        buttons=[MDFlatButton(text="OK", on_release=self.dismiss_dialog,md_bg_color=[0, 1, 0, 0.5]),],auto_dismiss=False)
        self.dialog.open()
    def fail(self, *args):
        self.dialog = MDDialog(
            title="Service Request Failed",
            text="Retry by giving inputs again",
            buttons=[MDRectangleFlatButton(text="OK", on_release=self.dismiss_dialog)],
            auto_dismiss=False,
        )
        self.dialog.open()
        self.dialogs.dismiss() 
        self.dialog = MDDialog(
            title="Check Internet",
            buttons=[MDRectangleFlatButton(text="OK", on_release=self.dismiss_dialog)],
            auto_dismiss=False,
        )
        self.dialog.open()
        self.dialogs.dismiss() 

MainApp().run()

