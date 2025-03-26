from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.label import Label
from engine import Scene, Actor
from engine.config import config
from kivy.core.audio import SoundLoader
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen

class Game(App):

    scenes = {}
    first_scene_name = "default"
    current_scene_name= "default"
    update = None
    _keyboard = None
    bg_music = None
    screen_manager = ScreenManager()
    configuration = config

    def __init__(self, **kwargs): # , bg_music=None
        super(Game, self).__init__(**kwargs)
        self.size = Window.size
        Window.bind(on_resize=self._update_size)
        self.bg_music = None
        self.play_bg_music()

        # Bind keyboard events

    def play_bg_music(self):
        if self.bg_music:
            sound = SoundLoader.load(self.bg_music)  # Replace with your file path
            if sound:
                sound.loop=True
                sound.play()

    def add_scene(self, scene):
        scene.game = self
        self.scenes[scene.name] = scene
        self.screen_manager.add_widget(scene)
        if self.first_scene_name == "default" and scene.name != 'default':
            self.first_scene_name = scene.name
            self.current_scene_name = scene.name
            self.screen_manager.current = scene.name

    def activate_scene(self, name):
        if name in self.scenes:
            self.current_scene_name = name
            self.screen_manager.current = name

    def get_current_scene(self):
        return self.scenes[self.current_scene_name]

    def build(self):
        if len(self.scenes) == 0:
            self.add_default_scene()
        Clock.schedule_interval(self.loop, 1 / self.configuration.fps)
        return self.screen_manager

    def add_default_scene(self):
        default_scene = Scene(name="default", background_color=(0.5, 0.5, 1, 1))
        # Actor as a label
        label1 = Label(text="Hello, this is Eason game engine!", font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.5})
        label1.color = (0,0,0,1)
        label2 = Label(text="Hello, this is Eason game engine!", font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.5})
        label2.color = (1,0,0,1)
        label3 = Label(text="Hello, this is Eason game engine!", font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.5})
        label3.color = (0,1,0,1)
        label4 = Label(text="Hello, this is Eason game engine!", font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.5})
        label4.color = (0,0,1,1)
        label5 = Label(text="Hello, this is Eason game engine!", font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.5})
        label5.color = (1,1,1,1)
        label_actor = Actor(
            frames=[label1, label2, label3, label4, label5],
            fps=5,
            name="label",
            anchor_x='center',  # Horizontal anchor at center
            anchor_y='center',  # Vertical anchor at center
            size_hint=(1, 1),  # Make AnchorLayout fill the FloatLayout
            pos_hint={'center_x': 0.5, 'center_y': 0.5}  # Center it in FloatLayout
        )
        default_scene.add_actor(label_actor)
        self.add_scene(default_scene)
        self.screen_manager.current = default_scene.name

    def _update_size(self, window, width, height):
        pass
        for scene in self.scenes:
            scene.size = (width, height)

    def loop(self, dt):
        self.get_current_scene().update()
        # if self.update:
        #     self.update()
        # if self.update_function:
        #     self.update_function()

        # for scene in self.scenes:
        #     scene.update()


