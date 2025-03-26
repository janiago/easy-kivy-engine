from engine import Game, Scene, Actor
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import SlideTransition, FadeTransition, SwapTransition

game = Game()

def show_welcome(self):
    game.activate_scene("welcome")

launch_scene = Scene(name="launch", background_color=(0.5, 0.5, 1, 1))
launch_btn = Button(text="launch")
launch_btn.bind(on_press=show_welcome)
launch_scene.add_widget(launch_btn)

game.add_scene(launch_scene)

welcome_scene = Scene(name="welcome", background_color=(0.5, 0.5, 1, 1))
# Actor as a label
label1 = Label(text="Hello, this is Eason game engine!", font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.5})
label1.color = (0, 0, 0, 1)
label2 = Label(text="Hello, this is Eason game engine!", font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.5})
label2.color = (1, 0, 0, 1)
label3 = Label(text="Hello, this is Eason game engine!", font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.5})
label3.color = (0, 1, 0, 1)
label4 = Label(text="Hello, this is Eason game engine!", font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.5})
label4.color = (0, 0, 1, 1)
label5 = Label(text="Hello, this is Eason game engine!", font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.5})
label5.color = (1, 1, 1, 1)
label_actor = Actor(
    frames=[label1, label2, label3, label4, label5],
    fps=5,
    name="label",
    anchor_x='center',  # Horizontal anchor at center
    anchor_y='center',  # Vertical anchor at center
    size_hint=(1, 1),  # Make AnchorLayout fill the FloatLayout
    pos_hint={'center_x': 0.5, 'center_y': 0.5}  # Center it in FloatLayout
)
welcome_scene.add_actor(label_actor)
game.add_scene(welcome_scene)
# game.screen_manager.transition = FadeTransition()
# game.screen_manager.transition = SlideTransition()
game.screen_manager.transition = SwapTransition()

if __name__ == "__main__":
    game.run()