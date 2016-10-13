from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.bubble import Bubble
from kivy.uix.screenmanager import ScreenManager, SwapTransition, Screen, SlideTransition


class DownloaderScreen(Screen):
    def __init__(self, **kwargs):
        super(DownloaderScreen, self).__init__(**kwargs)
        self.urlBox.focus = True

    def addUrl(self):
        print self.urlBox.text
        self.urlBox.text = ""

    # def callWindowControls(self):
    #     if not hasattr(self, 'bubb'):
    #         self.bubb = bubb = WindowControls()
    #         self.add_widget(bubb)
    #     else:
    #         values = ('left_top', 'left_mid', 'left_bottom', 'top_left',
    #                   'top_mid', 'top_right', 'right_top', 'right_mid',
    #                   'right_bottom', 'bottom_left', 'bottom_mid', 'bottom_right')
    #         index = values.index(self.bubb.arrow_pos)
    #         self.bubb.arrow_pos = values[(index + 1) % len(values)]


class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super(SettingsScreen, self).__init__(**kwargs)


class Controller(App):

    def __init__(self, **kwargs):
        super(Controller, self).__init__(**kwargs)

    def build(self):

        # Window.size = (700, 200)
        Window.borderless = True
        self.title = "T90"

        self.root = ScreenManager()
        self.screens = [
            DownloaderScreen(name='downloader'),
            SettingsScreen(name='settings')
        ]
        for screen in self.screens:
            self.root.add_widget(screen)

        self.root.transition = SlideTransition()
        self.root.current_screen = self.screens[0]

        return self.root


if __name__ == '__main__':
    app = Controller()
    app.run()