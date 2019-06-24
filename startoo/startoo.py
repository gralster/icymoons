from box import Box

def main():
    density = 0.5
    box1 = Box(18)
    box1.fill()
    box1.shake()
    box2 = Box(6)
    box2.fill(proportion = 0)
    box2.shake()
    box1.superpose(box2)
    box1.writecellfile()

main()
