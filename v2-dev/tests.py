from kivy.adapters.dictadapter import DictAdapter
from kivy.adapters.listadapter import ListAdapter
from kivy.adapters.simplelistadapter import SimpleListAdapter
from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.listview import ListView, ListItemButton, ListItemLabel
from kivy.uix.modalview import ModalView
from kivy.uix.progressbar import ProgressBar
from kivy.uix.screenmanager import ScreenManager, Screen, SwapTransition
from kivy.uix.textinput import TextInput
from kivy.uix.listview import CompositeListItem

class newWidget(BoxLayout):
    pass

class selectList(ModalView):
    def __init__(self, **kwargs):
        super(selectList, self).__init__(**kwargs)

        data = [str(i) for i in range(100)]
        item_strings = ["{0}".format(index) for index in range(100)]

        dict_adapter = SimpleListAdapter(sorted_keys=item_strings,
                                   data=data,
                                   selection_mode='multiple',
                                   allow_empty_selection=False,
                                   cls=ListItemButton)

        # Use the adapter in our ListView:
        list_view = ListView(adapter=dict_adapter)

        self.layout.add_widget(list_view)
        def getText(self):
            print self.inp.text

class TestKVfile(BoxLayout):
    ind, tot = 0,0

    def addUrl(self):
        print self.url_box.text
        url = newWidget()
        self.add_widget(url)
        url.hello.text = self.url_box.text
        self.url_box.text = ""
        self.list_adapter = ListAdapter(data=["Item #{0}".format(i) for i in range(10)], cls=ListItemButton,
                                        sorted_keys=[])
        self.list_adapter.bind(on_selection_change=self.selection_change)
        list_view = ListView(adapter=self.list_adapter, multiselect=True)
        self.add_widget(list_view)

    def selection_change(self, args):
        print args

    def sayHello(self):
        print self.url_box.text
        print "Hellooooooo"
        self.ind += 1
        if(self.ind == 5):
            self.ind, self.tot = 0, self.tot+1
        self.current_progress.value, self.total_progress.value = self.ind, self.tot
        self.a = selectList()
        self.a.open()

Builder.load_string("""
<MenuScreen>:
    BoxLayout:
        Button:
            text: 'Goto settings'
            on_press: root.manager.current = 'settings'
        Button:
            text: 'Quit'

<SettingsScreen>:
    BoxLayout:
        Button:
            text: 'My settings button'
        Button:
            text: 'Back to menu'
            on_press: root.manager.current = 'menu'
""")

# Declare both screens
class MenuScreen(Screen):
    pass

class SettingsScreen(Screen):
    pass


class MyApp2(App):

    # def build(self):
    #     return TestKVfile()

    def build(self):
        Window.size = (500, 300)
        # Window.borderless = True
    
        sm = ScreenManager()
        screens = [
            MenuScreen(name='menu'),
            SettingsScreen(name='settings')
        ]
        sm.add_widget(screens[0])
        sm.add_widget(screens[1])
        sm.transition = SwapTransition()
        sm.current_screen = screens[0]
        # # later
        # sm.switch_to(screens[1], direction='right')
        return sm




if __name__ == '__main__':
    MyApp2().run()