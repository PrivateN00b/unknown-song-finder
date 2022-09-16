import sys
sys.path.append('/home/toth-peter/Codes/Others/unknown-song-finder')

import kivymd
from kivy.lang import Builder
from kivymd.app import MDApp
from SpotifyScripts.ClientCreatePlaylist import AppCreatePlaylist
from pubsub import pub

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
                    on_release: app.exit_app()

                MDLabel:
                    id: resultLabel
                    adaptive_height: True
                    text: "Insert results here:"
                    halign: "center"
'''

class MainApp(MDApp):

    # Functions which are kinda logic but are necessary for displaying output
    def SelectCorrectTrackID(self, arg: list(dict()), item: str, type: str, offset: int):
        """Makes the user to choose a track out of the found ones with the same names.
        
        Returns: Selected track's ID
        """    
        for currentTrack in arg:
            print(f"Number: {currentTrack['idx']}, Name: {currentTrack['name']}, Info: {currentTrack['extra_info']}")
        
        # Displaying to resultLabel (Create own MDLabel widget instead)
        self.root.ids.resultLabel.text = """
            The algorithm have found numerous tracks with the same name.
            Navigation options (things you can write in):
            'back' key: List the previous song options
            'next' or any type of input key: List the next song options
            """

        # This will try to convert the input into -1. If you didn't write -1, for example an ENTER then it will catch it and convert to -1
        selectedNum = input("Select the correct track by inserting the corresponding number: ")
        try:
            selectedNum = int(selectedNum)
        except ValueError:
            print('') # This is just a placeholder.
        
        # Checks if the user responded with -1. (If the algorithm included the correct track in the list)
        if isinstance(selectedNum, int):        
            print("-"*20+"\n")
            
            # Sends back the selected track's ID to DoesItemExists for returning the ID
            pub.sendMessage('getSelectedTrackID', selectedID=arg[selectedNum - 1]['itemID'])
        elif selectedNum == 'back' and offset >= 50:
            print("Checking the previous list...\n")
            pub.sendMessage('rerunCorrectTrackSearch', item=item, type=type, offset=(offset-50))
        elif selectedNum == 'back' and offset < 50:
            print("There is no previous list to check into!\n")
        else:
            print("Checking the next list...\n")
            pub.sendMessage('rerunCorrectTrackSearch', item=item, type=type, offset=(offset+50))



    def build(self):
        self.api: AppCreatePlaylist = AppCreatePlaylist()
        # Theme style
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Orange"
        # The screen variable contains the UI
        screen = Builder.load_string(KV)  
        return screen
    
    def select_items(self):
        # DoesItemExists will send a message to here
        pub.subscribe(self.SelectCorrectTrackID, 'selectCorrectTrack')

        # Calls the api's InspectItemsDecorator to get the input items ID's
        item_label_text = str.lower(self.root.ids.itemLabel.text[:-2])
        itemTextField_text = self.root.ids.itemTextField.text
        self.api.InspectItemsDecorator(item_label_text, itemTextField_text)
        # Displaying the selectable options?

    def get_songs(self):
        pass
    
    def on_start(self):
        pass

    def exit_app(self):
        """Exits from the application duuuuhhh"""
        MDApp.get_running_app().stop()
    
if __name__ == '__main__':
    MainApp().run()