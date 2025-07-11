import tkinter as tk
from PIL import Image, ImageTk
import random

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

root = tk.Tk()
root.title("Bouncing Burger Animation")
root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
root.resizable(False, False)

canvas = tk.Canvas(root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
canvas.pack()

image_path = 'burjer.png'
try:
    original_image = Image.open(image_path)
    resized_image = original_image.resize((150, 150), Image.Resampling.LANCZOS)
    burger_image = ImageTk.PhotoImage(resized_image)
except FileNotFoundError:
    print(f"Error: The image file '{image_path}' was not found.")
    print("Please make sure the image file is in the same folder as your Python script.")
    root.destroy()
    exit()

x_pos, y_pos = WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2
x_velocity, y_velocity = 5, 4

burger_on_canvas = canvas.create_image(x_pos, y_pos, image=burger_image)

name_text = canvas.create_text(
    x_pos, y_pos,
    text="Kit Herbert Obo",
    font=("Arial", 24, "bold"),
    fill="white"
)

is_paused = False

def bounce_animation():
    global x_pos, y_pos, x_velocity, y_velocity, is_paused

    if is_paused:
        root.after(16, bounce_animation)
        return

    coords = canvas.coords(burger_on_canvas)
    current_x = coords[0]
    current_y = coords[1]
    
    new_x = current_x + x_velocity
    new_y = current_y + y_velocity

    did_collide = False
    
    if new_x + 75 > WINDOW_WIDTH or new_x - 75 < 0:
        x_velocity *= -1
        did_collide = True
    
    if new_y + 75 > WINDOW_HEIGHT or new_y - 75 < 0:
        y_velocity *= -1
        did_collide = True

    if did_collide:
        # Generate two different random colors
        text_color = f"#{random.randint(0, 0xFFFFFF):06x}"
        bg_color = f"#{random.randint(0, 0xFFFFFF):06x}"

        # Ensure the colors are not the same
        while text_color == bg_color:
            bg_color = f"#{random.randint(0, 0xFFFFFF):06x}"
            
        canvas.itemconfig(name_text, fill=text_color)
        canvas.config(bg=bg_color)

    canvas.move(burger_on_canvas, x_velocity, y_velocity)
    canvas.move(name_text, x_velocity, y_velocity)

    root.after(16, bounce_animation)

def toggle_pause(event):
    global is_paused
    is_paused = not is_paused
    print(f"Animation is {'Paused' if is_paused else 'Resumed'}")

root.bind("<space>", toggle_pause)

bounce_animation()

root.mainloop()