import turtle
import math

ANGLE_DEG = 45
SCALE = math.sqrt(2)/2

def draw_branch(t: turtle.Turtle, length: float, level: int, max_level: int):
    if level == 0:
        return

    shade = int(200 * (max_level - level) / max_level) + 55
    t.pencolor(0, shade, 0)

    t.forward(length)

    pos = t.pos()
    heading = t.heading()

    t.left(ANGLE_DEG)
    draw_branch(t, length * SCALE, level - 1, max_level)

    t.penup(); t.setpos(pos); t.setheading(heading); t.pendown()

    t.right(ANGLE_DEG)
    draw_branch(t, length * SCALE, level - 1, max_level)

    t.penup(); t.setpos(pos); t.setheading(heading); t.pendown()

def main():
    try:
        level = int(input("Вкажіть рівень рекурсії (1–12): ").strip())
    except Exception:
        level = 8
    level = max(1, min(level, 12))

    screen = turtle.Screen()
    screen.title("Фрактал: Дерево Піфагора (рекурсія)")
    screen.bgcolor("white")
    screen.setup(width=900, height=900)
    screen.colormode(255)

    t = turtle.Turtle(visible=False)
    t.pensize(2)
    t.speed(0)
    turtle.tracer(0, 0)

    t.penup()
    t.goto(0, -320)
    t.setheading(90)
    t.pendown()

    draw_branch(t, length=140, level=level, max_level=level)

    turtle.update()
    screen.mainloop()

if __name__ == "__main__":
    main()
