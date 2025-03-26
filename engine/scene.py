from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Rectangle, Color
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen


class Scene(Screen):

    # Class properties

    def __init__(self, name, background_color=None, background_image=None, **kwargs):
        super(Screen, self).__init__(**kwargs)
        self.name = name
        self.root_layout = FloatLayout()
        self.add_widget(self.root_layout)
        self.root_layout.bg_rect = None
        self.bg_sound = None
        self.actors = []
        self.dead_actors = []
        self.pressed_keys = set()
        self.game = None

        # Draw the background
        with self.canvas.before:
            if background_image:
                self.root_layout.bg_rect = Rectangle(source=background_image, size=self.root_layout.size, pos=self.root_layout.pos)
            elif background_color:
                Color(*background_color)  # Background color (e.g., (1, 0, 0, 1) for red)
                self.root_layout.bg_rect = Rectangle(size=self.root_layout.size, pos=self.root_layout.pos)

        # Bind size and position changes to redraw background
        self.root_layout.bind(size=self._update_background, pos=self._update_background)

        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_key_down)
        self._keyboard.bind(on_key_up=self._on_key_up)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_key_down)
        self._keyboard = None

    def _on_key_down(self, keyboard, keycode, text, modifiers):
        # print("On key down: ", keycode)
        self.pressed_keys.add(keycode)
        return True  # Indicate the event was handled

    def _on_key_up(self, keyboard, keycode):
        # print("On key up: ", keycode)
        self.pressed_keys.discard(keycode)
        return True

    def _update_background(self, *args):
        if hasattr(self.root_layout, 'bg_rect'):
            self.root_layout.bg_rect.size = self.root_layout.size
            self.root_layout.bg_rect.pos = self.root_layout.pos

    def actors_colliding(self):
        for actor in self.actors:
            actor.colliding_actors = []
        for i in range(0, len(self.actors) - 1):
            actor_i = self.actors[i]
            for j in range(0, len(self.actors)):
                if i == j:
                    continue
                actor_j = self.actors[j]
                if actor_i in actor_j.colliding_actors:
                    continue
                if actor_i.collide_widget(actor_j):
                    actor_i.collide(actor_j)
                    actor_j.collide(actor_i)

    def remove_dead_actors(self):
        for actor in self.dead_actors:
            # if actor in self.actors:
            #     self.actors.remove(actor)
            actor.destroy()
        self.dead_actors.clear()

    def update(self):
        self.move_actors(self.pressed_keys)
        self.actors_colliding()
        self.remove_dead_actors()

    def set_bg_sound(self, bg_sound):
        self.bg_sound = bg_sound
        # should play this sound

    def add_actor(self, actor):
        self.actors.append(actor)
        self.root_layout.add_widget(actor)
        actor.scene = self

    def move_actors(self, pressed_keys):
        for actor in self.actors:
            actor.move_on_keys(pressed_keys)
            # pass