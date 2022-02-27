from turtle import width
from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from kivy.uix.image import Image
from kivymd.uix.button import MDFillRoundFlatButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.toolbar import MDToolbar
from kivy.core.window import Window

from kivy.lang import Builder
Window.size = (800, 600)


class ConverterApp(MDApp):
    def flip(self):
        if self.state:
            self.state = not self.state
            self.toolbar.title = "Decimal to binary conversion"
            self.input.text = "Enter a decimal number"
        else:
            self.state = not self.state
            self.toolbar.title = "Binary to decimal conversion"
            self.input.text = "Enter a binary number"
        self.converted.text = ""
        self.label.text = ""
            

    def convert(self, var):
        try:
            if "." not in self.input.text and "," not in self.input.text:
                if self.state:      
                    val = int(self.input.text, 2)
                    self.converted.text = str(val)
                    self.label.text = "Decimal: "
                else:
                    val = bin(int(self.input.text))[2:]
                    self.converted.text = val
                    self.label.text = "Binary: "
            else:
                if "," in self.input.text:
                    index = self.input.text.index(",")
                    self.input.text = self.input.text[:index] + "." +self.input.text[index+1:]
                
                whole, fract = self.input.text.split(".")

                if self.state:
                    # bin -> dec
                    whole = int(whole, 2)
                    floating = 0
                    for idx, digit in enumerate(fract):
                        floating += int(digit)*2**(-(idx+1))

                    self.converted.text = str(whole+floating)
                    self.label.text = "Decimal: "

                else:
                    # dec -> bin
                    decimal_places = 10
                    whole = bin(int(whole))[2:]
                    fract = float("0."+fract)
                    floating = []
                    for i in range(decimal_places):
                        if fract*2 < 1:
                            floating.append("0")
                            fract *= 2
                        elif fract*2 > 1:
                            floating.append("1")
                            fract -= fract*2 - 1
                        elif fract*2 == 1.0:
                            floating.append("1")
                            break
                    self.converted.text = str(whole+"."+"".join(floating))
                    self.label.text = "Binary: "
        except Exception:
            self.label.text = ""
            if self.state:
                self.label.text = "Enter binary number"
            else:
                self.label.text = "Enter decimal number"


    def build(self):
        self.state = True
        self.theme_cls.primary_palette = "BlueGray"
        screen = MDScreen()

        self.toolbar = MDToolbar(title="Binary to Decimal")
        self.toolbar.pos_hint = {"top":1}
        self.toolbar.right_action_items = [["rotate-3d-variant", lambda x: self.flip()]]
        screen.add_widget(self.toolbar)

        screen.add_widget(Image
            (
            source="logo.png", 
            pos_hint={"center_x":0.5, "center_y":0.65}
            )
        )  

        self.input = MDTextField(
            text = "Enter a binary number", 
            width = 300,
            halign = "center",
            size_hint = (0.8, 1),
            pos_hint = {"center_x":0.5, "center_y":0.4},
            font_size = 50,
        )

        screen.add_widget(self.input)

        self.label = MDLabel(
            halign="center",
            pos_hint= {"center_x":0.5, "center_y":0.3},
            theme_text_color = "Secondary",
        )

        self.converted = MDLabel(
            halign="center",
            pos_hint= {"center_x":0.5, "center_y":0.25},
            theme_text_color = "Primary",
            font_style = "H5",
        )

        screen.add_widget(self.label)
        screen.add_widget(self.converted)

        screen.add_widget(MDFillRoundFlatButton(
            text= "convert".upper(),
            font_size = 17,
            pos_hint= {"center_x":0.5, "center_y":0.15},
            on_press = self.convert,
            )
        )

        return screen
    
if __name__ == '__main__':
    ConverterApp().run()
