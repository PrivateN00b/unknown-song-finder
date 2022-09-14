import sys
sys.path.append('/home/toth-peter/Codes/Others/unknown-song-finder')

import kivymd
from kivy.lang import Builder
from kivymd.app import MDApp
from SpotifyScripts import Main
KV = '''
MDScreen:

    MDBoxLayout:
        orientation: "vertical"
        
        MDTopAppBar:
            title: "MDLabel"
            
        MDLabel:
            text: "Artist(s):"
            halign: "center"

        MDTextField:
            id: kaga
            hint_text: "Insert the artists here separated with commas"
            helper_text: "Correct format: Artist1,Artist2,Artist3"
            helper_text_mode: "persistent"
            size_hint_x: .3
            
        MDRoundFlatButton:
            text: "Get recommended songs"
            text_color: "white"
            on_press: app.get_songs()
'''

class MainApp(MDApp):

    def build(self):
        # Theme style
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Orange"
        # The screen variable contains the UI
        screen = Builder.load_string(KV)  
        return screen
    
    def get_songs(self):
        print(self.root.ids['kaga'].text)
        Main.Main()
    
    def on_start(self):
        pass
    
if __name__ == '__main__':
    MainApp().run()