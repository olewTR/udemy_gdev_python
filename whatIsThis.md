
## Section 1 - Setup and Installation
this project requires
- python - v3
- pygames library
- assets will be taken from the web, free.

## Section 2 - Basic pygame tutorial
1. display surface created
2. game loop created
3. adding condition that allows game end and closing the surface
4. unloading initialized pygame library in the end
   
all in the file called : "1_display_surface.py" in repo

### drawing on the display

1. filename 2_drawing_on_display.py
    - pygame allows to draw on the display with simple shapes like square, rectangle etc and using colors
    - using colors as tuples `BLACK = (0,0,0)` etc
    - to update display there are two methods
      - flip - updates the whole display
      - update - possible only partial update of the screen
      - it happens in the program loop - but oustide of the 'for' loop

### drawing the line
line needs surface, color, starting point, ending point and thickness
### drawing the circle
`pygame.draw.circle(display_surface, WHITE, (WINDOW_HEIGHT//2, WINDOW_WIDTH//2), 55, 11)` 55-radius 11 thickness
### drawing the rectangle
here we need a tuple with top-left x, top left y, height, width)

the strating of xy axis is top left of the display area

### blitting images
