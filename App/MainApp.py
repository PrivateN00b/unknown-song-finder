import sys
sys.path.append('/home/toth-peter/Codes/Others/unknown-song-finder')

import kivymd
from kivy.lang import Builder
from kivymd.app import MDApp
from SpotifyScripts.ClientCreatePlaylist import AppCreatePlaylist
KV = '''
MDScreen:

    ScrollView:

        MDList:

            MDTopAppBar:
                title: "MDLabel"

            MDList:
                padding: "24dp"
                spacing: "24dp"

                MDLabel:
                    id: itemLabel
                    adaptive_height: True
                    text: "Artists:"
                    halign: "center"

                MDTextField:
                    id: itemTextField
                    adaptive_height: True
                    mode: "round"
                    hint_text: "Insert the artists here separated with commas"
                    helper_text: "Correct format: Artist1,Artist2,Artist3"
                    helper_text_mode: "persistent"
                        
                MDRoundFlatButton:
                    adaptive_height: True
                    text: "Select artists"
                    text_color: "white"
                    halign: "center"
                    on_press: app.select_items()

                MDLabel:
                    id: resultLabel
                    adaptive_height: True
                    text: "Insert results here:"
                    halign: "center"
'''

class MainApp(MDApp):

    api: AppCreatePlaylist

    def build(self):
        # Theme style
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Orange"
        # The screen variable contains the UI
        screen = Builder.load_string(KV)  
        return screen
    
    def select_items(self):
        item_label_text = self.root.ids.itemLabel.text
        self.api.AskForItemAndInspectDecorator(item_label_text)
        print(self.api.inputArtistIDs)


    def get_songs(self):
        # This initialization will indirectly run the BaseCreatePlaylist's
        # __init__ which will run the entire playlist fabrication process
        self.api = AppCreatePlaylist()
    
    def on_start(self):
        pass
    
if __name__ == '__main__':
    MainApp().run()