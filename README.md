# Tic-Tac-Toe Game :sunglasses::fire:

## Table of Contents
1. [Game description](#game-description)
3. [About the Code](#about-the-code) 
	- [Useful pygame functions](#useful-pygame-functions)
	- [Hovering effect on buttons](#hovering-effect-on-buttons)
	- [Minimax algorithm](#minimax-algorithms)
4. [References](#references)


### <Center>Game Description</center><br><br>
This game is also called noughts and crosses. It is a two player turn based game and consists of a 3x3 empty square in which the players can place their marks.<br><br>During their turn each player tries to place three of their marks in a horizontal, vertical, or diagonal row to win.<br><br> This game is so simple that it is often used as a pedagogical tool for teaching the concepts of good sportsmanship and the branch of artificial intelligence that deals with the searching of game trees.

### <center>About the Code</center><br><br>

#### Useful pygame functions

**How to display a text on the screen** - For this we first need to make a font object which contains all the information about the font of our text.<br><br>
```my_font = pygame.font.SysFont(font_type,font_size,bold=False,italic=False)```<br><br>
font_type : It is the font you like your text to be in and that is available to your pygame module.<br>
font_size : It is the size of the text.<br>
bold : If this parameter is set to True then your font will be in bold.It is by default set to False.<br>
italic : If this parameter is set to True then yout font will be in Italic.It is also by default set to False.<br><br>
After you have made the font for your text then you need to get the text by rendering whatever you like to display through the font you made.<br><br>

```my_text = my_font.render(text_to_display,True,color)```<br><br>
text_to_display : It is the text we want to display .It can be anything.
color : It is the color we want our text to be in.It can be tuple containing the RGB(Red,Green,Blue) values of the color (example: (255,0,255) - this is purple), or we select a predefined color using pygame module (example : pygame.color('DarkBlue'))<br><br>

After we have our text we have to blit or paste it to our canvas.For this we use the ```blit()``` function<br><br>
```window.blit(my_text,(x_coordinate,y_coordinate))```<br><br>
window : It is the pygame canvas in which we are working. Every thing which is displayed is displayed here only.<br>It is initialised in the very beginning of the program.<br>```window = pygame.display.set_mode((screenWidth,screenHeight))```<br>my_text is assumed to be inside a rectangle whose dimensions are such that the text is tightly bounded by it.Then the x_coordinate and the y_coordinate are the x and y coordinates of the top-left corner of this rectangle.<br><br>
The work is not over yet.Even after pasting the text to the pygame window we still need the update the display of the window . To do this we use the command - <br>```pygame.display.update()```<br>This will update the display window and any changes we made can now be seen on the screen.<br><br><br><br>
**How to draw a line or a rectangle** - Drawing a line or a rectangle is very easy.<br>A line in pygame is defined by - <br>color : the color of the line<br>line_width : This means how thick the line is.<br>starting_position : This is a tuple containing the x and y coordinate of the starting point of the line.<br>ending_position : This is a tuple containing the x and y coordinates of the ending point of the line.<br>After we have decided all these parameters all we need to do is call the ```draw.rect()``` function<br>
```pygame.draw.line(window,color,starting_point,ending_point,line_width=1)```<br><br>
here again the color is a 3 length tuple (r,g,b) or predefined pygame.Color('Red')<br>
Also the starting_point and ending_point are also tuples (x,y)<br>
**It should be noted that the origin of the canvas is at top left and not bottom left. Also x coordinate increases from left to right and the y coordinate increases from top to bottom**<br><br>
Similar to the line , a rectangle is defined by its color , coordinates of the top-left corner and the dimension of the rectangle . The sides of the rectangle are parallel to the x and y axis.<br><br>
```pygame.draw.rect(window,color(x_coordinate_top_left_point,y_coordinate_top_left_point,rectangle_width,rectangle_height))```<br><br>



