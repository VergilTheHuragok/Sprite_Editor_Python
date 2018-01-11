A sprite editor to create sprites which can only be used and displayed in the
editor. Not the most useful creation but a unique one, at least. I made this back
when I didn't really know what I was doing programming-wise. It definitely shows.
There are lot's of useless features available here each of which would have made
greater sense if I had ever finished this project. Looking back on this code, I
do not intend ever to finish it. Oh, and I'm guessing everything is broken.  
  
**CONTROLS**:  
**Click** to add a point. **Hold** to add points.  
**C** to change color  
**N** to create a new poly  
**F1** to save file as  
**S** to add shapes  
**=** to change the zoom level  
**v** to generate a variation of the sprite with attachments and changes based on attributes  
**f** to fill the polies  
**i** to restrict points to simple polygons  
**r** to change resolution  
**g** to display a grid  
**z** to undo poly  
**Shift + z** to undo point  
**b** to cycle background  
**d** to delete individual polies  
**Shift + d** to delete all polies  
**a** to add attributes to polies  
**Shift + a** to add attributes to all polies  
**l** to lock points of current poly onto polies in background  
**m** to toggle mirror  
**Shift + m** to create mirror from current poly if only two points placed  
  
**ATTRIBUTES**:  
Attributes can be added to individual polies which enable different functions for generating variations.  
Attributes are added as "key, first argument, second, third, etc"  
  
**change** generates a new variation every given milliseconds in the first argument  
**genshape** allows the poly to move points a max of the first argument and at a frequency of the second argument  
**Invisible** does not fill the poly and gives the boundary a dotted line  
**complex** allows varied points to form complex polygons  
**gencolor** varies the poly's color based on max hue difference, saturation difference, and lightness difference as the first, second, and third arguments respectively. Uses the HSL scale  
**allows** a path to a sprite folder to be specified as the first argument. Random sprites will be pulled from the folder with attach attributes which match the current sprite and are overlayed with the attach polies lined up  
