from kivy.animation import Animation
from kivy.graphics.transformation import Matrix
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle, Line, PushMatrix, Rotate, PopMatrix, Translate
from kivy.clock import Clock
from kivy.uix.anchorlayout import AnchorLayout
from engine.config import DEFAULT_FPS
from kivy.uix.label import Label
from kivy.properties import NumericProperty

def process_content(content):
    if isinstance(content, str):
        return Image(source=content, )
    else:
        return content

class Actor(AnchorLayout):

    def __init__(self, name, frames, group = "default", size_hint=(0.1, 0.1), background_color=(0, 0, 0, 0), fps=DEFAULT_FPS, rotation_angle = 0, **kwargs):
        super().__init__(**kwargs)
        self.scene = None
        self.colliding_actors = []
        self._on_collide = None
        self.group = group
        self.current_frame = None
        self.move_speed = 0
        self.move_auto_y = 0
        self.move_auto_x = 0
        self.move_up_on_key = None
        self.move_down_on_key = None
        self.move_left_on_key = None
        self.move_right_on_key = None
        self.after_move = None
        self.stop_at_edge = True
        self.destroy_at_edge = False
        # self.name = None
        # self.rotation_angle = NumericProperty(0)
        # translate = None
        # rotate = None

        self.name = name
        self.size_hint = size_hint

        # self.matrix = Matrix()
        self.rotation_angle = rotation_angle

        with self.canvas.before:
            self.push_matrix = PushMatrix()  # Isolate transformations
            Color(*background_color)
            self.rotate = Rotate(angle=self.rotation_angle, origin=self.center)
            self.bg_rect = Rectangle(size=self.size, pos=self.pos)
            self.border = Line(rectangle=(self.x, self.y, self.width, self.height), width=50)

        # if self.rotation_angle != 0:
        #     print("Actor ", self.name, " has rotation_angel: ", self.rotation_angle)
        #     with self.canvas.after:
        #         # self.translate = Translate()  # Adjust for rotation center
        #         # self.rotate = Rotate(angle=self.rotation_angle, origin=self.center)  # Rotation
        #         self.pop_matrix = PopMatrix()  # End isolation

        with self.canvas.after:
            self.pop_matrix = PopMatrix()

        self.bind(pos=self._update_graphics, size=self._update_graphics)
        self.frames=[]
        for f in frames:
            self.frames.append(process_content(f))



        # if not isinstance(self.frames, list):
        #     self.frames = [process_content(self.frames)]
        # else:
        #     for f in frames:
        #         self.frames.append(process_content(f))

        self.fps = fps
        self.current_frame_index = 0
        self.draw()

    def set_collide_handler(self, handler):
        self._on_collide = handler

    def collide(self, colliding_actor):
        if self._on_collide:
            self._on_collide(self, colliding_actor)


    def _update_graphics(self, *args):
        """Update graphics when position or size changes."""
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
        self.border.rectangle = (self.x, self.y, self.width, self.height)
        if self.current_frame:
            self.current_frame.pos = self.pos
        self.rotate.origin = self.center  # Ensure rotation is around center
        # self.translate.xy = self.center  # Adjust translation origin

    def draw(self):
        if len(self.frames) == 0:
            return

        if len(self.frames) > 1:
            duration = (1 / self.fps) if self.fps > 0 else 60
            Clock.schedule_interval(self.next_frame, duration)
        else:
            self.current_frame_index = (self.current_frame_index + 1) % len(self.frames)
            frame = self.frames[self.current_frame_index]
            self.add_widget(frame)
            self.current_frame = frame
            # print("self.rotation: ", self.rotation)
            # if self.rotation != 0:
            #     self.current_frame._apply_transform(self.matrix)

    # def on_rotation_angle(self, instance, rotation):
    #     print("on_rotation: ", rotation)
    #     self.rotation.angle = self.rotation_angle
    #     self.rotation.origin = self.center  # Ensure rotation is around the center
    #     # self.matrix.identity()
    #     # self.matrix.translate(self.center_x, self.center_y, 0)
    #     self.matrix.rotate(rotation, 0, 0, 1)
    #     # self.matrix.translate(-self.center_x, -self.center_y, 0)

    def next_frame(self, dt):
        self.clear_widgets()
        last_frame = self.frames[self.current_frame_index]
        self.remove_widget(last_frame)
        self.current_frame_index = (self.current_frame_index + 1) % len(self.frames)
        frame = self.frames[self.current_frame_index]
        self.add_widget(frame)
        self.current_frame = frame
        # if self.rotation != 0:
        #     self.current_frame._apply_transform(self.matrix)

    def destroy(self, callback = None):
        # print("destroying ", self.name)
        for frame in self.frames:
            self.remove_widget(frame)
        if self.parent:
            self.parent.remove_widget(self)
        if self in self.scene.actors:
            self.scene.actors.remove(self)
        if callback:
            callback()

    def move_on_keys(self, pressed_keys):
        """Move the actor based on key inputs."""
        # if self.rotation != 0:
        #     self.current_frame._apply_transform(self.matrix)
        if self.move_speed > 0:
            current_x, current_y = self.pos
            new_x, new_y = current_x, current_y

            if self.move_up_on_key in pressed_keys:
                # print("moving up")
                new_y += self.move_speed
            if self.move_down_on_key in pressed_keys:
                # print("moving down")
                new_y -= self.move_speed
            if self.move_left_on_key in pressed_keys:
                # print("moving left")
                new_x -= self.move_speed
            if self.move_right_on_key in pressed_keys:
                # print("moving right")
                new_x += self.move_speed

            if self.move_auto_x != 0:
                new_x += self.move_speed * self.move_auto_x
            if self.move_auto_y != 0:
                new_y += self.move_speed * self.move_auto_y

            if self.stop_at_edge:
                new_x = max(0, min(new_x, self.parent.width - self.width))
                new_y = max(0, min(new_y, self.parent.height - self.height))

            if self.destroy_at_edge and self.parent and (new_x < 0 or new_x > self.parent.width or new_y < 0 or new_y > self.parent.height):
                self.destroy(False)

            if new_x != current_x or new_y != current_y:
                self.pos = (new_x, new_y)

            if self.after_move:
                self.after_move()

            # anim = Animation(x=new_x, y=new_y, duration=1 / self.scene.game.fps)
            # anim.start(self)

            # self.move(new_y, new_x)
            # Update the position
            # self.pos = (new_x, new_y)
            # print('self.pos: ', self.pos)
            # print('self.currentframe.pos', self.current_frame.pos)
    #
    # def move(self, pressed_keys):
    #     if self.move_speed > 0:
    #         if self.move_up_on_key in pressed_keys and self.pos_hint["y"] < 1.0:
    #             print("moving up")
    #             self.pos_hint["y"] += self.move_speed
    #         if self.move_down_on_key in pressed_keys and self.pos_hint["y"] > 0:
    #             print("moving down")
    #             self.pos_hint["y"] -= self.move_speed
    #         if self.move_left_on_key in pressed_keys and self.pos_hint["x"] > 0:
    #             print("moving left")
    #             self.pos_hint["x"] -= self.move_speed
    #         if self.move_right_on_key in pressed_keys and self.pos_hint["x"] < 1.0:
    #             print("moving right")
    #             self.pos_hint["x"] += self.move_speed
    #         self.pos_hint = self.pos_hint.copy()

    # def collides_with(self, other):
    #     """Check collision with another Actor."""
    #     x1, y1 = self.pos
    #     w1, h1 = self.size
    #     x2, y2 = other.pos
    #     w2, h2 = other.size
    #
    #     return (
    #         x1 < x2 + w2 and
    #         x1 + w1 > x2 and
    #         y1 < y2 + h2 and
    #         y1 + h1 > y2
    #     )