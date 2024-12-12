
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
blitting in pygame means copying the images to the surface
its done by 
- loading the image
`dragon_left_image = pygame.image.load("dragon_left.png")`
- getting the rect size of the image
`dragon_left_rect = dragon_left_image.get_rect()`
- setting the position for the image (on the main display)
`dragon_left_rect.topleft = (0,0)`
- calling the blit method, inside the program loop
`display_surface.blit(dragon_left_image, dragon_left_rect)`
- updating the surface with 
`pygame.display.update()`

### checking available fonts in the system
``` 
fonts = pygame.font.get_fonts()
for font in fonts:
    print(font)
```

loading custom font:  
`custom_font = pygame.font.Font('AttackGraffiti.tff' 32)`
in above example the font is available in the project directory, file extension is mandatory

### intiger division
`WINDOW_WIDTH//2` this kind of division returns always intiger as result

### moving the object on surface - look into examples - section 2 -> 6_discrete_movement