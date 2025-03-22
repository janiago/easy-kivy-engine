from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.label import Label
from engine import Scene, Actor
from engine.config import DEFAULT_FPS
from kivy.core.audio import SoundLoader


class Game:

    scenes = []
    current_scene_index = 0
    fps = 60 # frames per second
    update = None
    _keyboard = None
    bg_music = None

    def __init__(self, fps = DEFAULT_FPS, bg_music=None):
        self.fps = fps
        self.size = Window.size
        Window.bind(on_resize=self._update_size)
        self.bg_music = bg_music
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
        self.scenes.append(scene)

    def get_current_scene(self):
        return self.scenes[self.current_scene_index]

    def start(self):
        if len(self.scenes) == 0:
            self.add_default_scene()
        Clock.schedule_interval(self.loop, 1 / self.fps)
        return self.get_current_scene()

    def add_default_scene(self):
        default_scene = Scene(background_color=(0.5, 0.5, 1, 1))
        # Actor as a label
        label1 = Label(text="Hello, this is Eason game engine!", font_size=40)
        label1.color = (0,0,0,1)
        label2 = Label(text="Hello, this is Eason game engine!", font_size=40)
        label2.color = (1,0,0,1)
        label3 = Label(text="Hello, this is Eason game engine!", font_size=40)
        label3.color = (0,1,0,1)
        label4 = Label(text="Hello, this is Eason game engine!", font_size=40)
        label4.color = (0,0,1,1)
        label5 = Label(text="Hello, this is Eason game engine!", font_size=40)
        label5.color = (1,1,1,1)
        label_actor = Actor(
            frames=[label1, label2, label3, label4, label5],
            fps=5
        )
        default_scene.add_actor(label_actor)
        self.add_scene(default_scene)

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


