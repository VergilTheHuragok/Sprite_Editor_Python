'''
Created on May 21, 2016

@author: VergilTheHuragok

A sprite editor to create sprites which can only be used and displayed in the
editor. Not the most useful creation but a unique one, at least. I made this back
when I didn't really know what I was doing programming-wise. It definitely shows.
There are lot's of useless features available here each of which would have made
greater sense if I had ever finished this project. Looking back on this code, I
do not intend ever to finish it. Oh, and I'm guessing everything is broken.

CONTROLS:
Click to add a points. Hold to add points.
C to change color
N to create a new poly
F1 to save file as
S to add shapes
= to change the zoom level
v to generate a variation of the sprite with attachments and changes based on attributes
f to fill the polies
i to restrict points to simple polygons
r to change resolution
g to display a grid
z to undo poly
Shift + z to undo point
b to cycle background
d to delete individual polies
Shift + d to delete all polies
a to add attributes to polies
Shift + a to add attributes to all polies
l to lock points of current poly onto polies in background
m to toggle mirror
Shift + m to create mirror from current poly if only two points placed

ATTRIBUTES:
Attributes can be added to individual polies which enable different functions for generating variations.
Attributes are added as "key, first argument, second, third, etc"

change generates a new variation every given milliseconds in the first argument
genshape allows the poly to move points a max of the first argument and at a frequency of the second argument
Invisible does not fill the poly and gives the boundary a dotted line
complex allows varied points to form complex polygons
gencolor varies the poly's color based on max hue difference, saturation difference, and lightness difference as the first, second, and third arguments respectively. Uses the HSL scale
attach allows a path to a sprite folder to be specified as the first argument. Random sprites will be pulled from the folder with attach attributes which match the current sprite and are overlayed with the attach polies lined up
'''
import pygame
import jsonpickle
import os
import json
import getpass
import time
import math
import colorsys
import random


pygame.init()
clock = pygame.time.Clock()

class sprite:
    def __init__(self, stype=None, name=None):
        self.stype = stype
        self.polygons = []
        self.attributes = []
        self.name = name
    def add_polygon(self, polygon, color, attributes=None):
        self.polygons.append([polygon, color, attributes])
    def get_polygons(self):
        return self.polygons
    def add_attribute(self, attribute):
        i = 0
        if len(self.attributes) > 0:
            for att in self.attributes:
                if att[0] == attribute[0]:
                    self.attributes[i] = attribute
                    i = 0
                    break
                i += 1
        if i == 0:
            self.attributes.append(attribute)
        self.attributes.append(attribute)
    def get_attribute(self, attribute):
        for a in self.attributes:
            if (a[0] == attribute):
                return a[1]
    def draw_sprite(self, point, size, rotation):
        pass

def save(overwrite, new_name=None):
    global current_file
    cdir = "C:\\Users\\" + getpass.getuser() + "\\Desktop\\sprites\\" + sprite1.stype + "\\"
    if (new_name != None and not overwrite):
        current_file = new_name
    if (current_file == -1):
        if (new_name == None):
            current_file = next_file(cdir)
    if (check_polies([points, color])):
        sprite1.add_polygon(points, color)
    clean_polies()
    sprite1.add_attribute(("size", base_resolution))
    if (not overwrite and new_name == None):
        num = next_file(cdir)
    else:
        num = current_file
    sprite1.add_attribute(("name", num))
    if (os.path.isfile(cdir + str(num) + ".json")):
        os.remove(cdir + str(num) + ".json")
    time.sleep(.003)
    output = open(cdir + str(num) + ".json", 'w')
    json.dump(jsonpickle.encode(sprite1), output)
    output.close()

def draw_from_file(filled, polygons):
    global back_odd
    global back_first
    global back_i
    global back_toggle
    global change_points
    
    if back_toggle == "grey move" or back_toggle == "black move":
        if (back_toggle == "grey move"):
            color_1 = (125, 125, 125)
            color_2 = (75, 75, 75)
        elif (back_toggle == "black move"):
            color_1 = (0, 0, 0)
            color_2 = (255, 255, 255)
        timer = pygame.time.get_ticks()
        width = 25
        height = 25
        i = 0
        while timer > 100 * width:
            i = i + 1
            if (i > back_i):
                back_i = i
                back_odd = not back_odd
            timer = timer - 100 * width
        for r in range(0, base_resolution[1], height):
            grey = back_odd
            for i in range(0, base_resolution[0] + 4 * width, width):
                l = i - int(timer / 100)
                if (grey):
                    screen.fill(color_1, (l, r, width, height))
                else: 
                    screen.fill(color_2, (l, r, width, height))
                grey = not grey
            if (len(range(0, base_resolution[1], height)) % 2 == 0):
                back_odd = not back_odd
            elif (r < base_resolution[1] - height):
                back_odd = not back_odd
    elif (back_toggle == "white"):
        screen.fill((255, 255, 255))
    elif (back_toggle == "black"):
        screen.fill((0, 0, 0))
    elif (back_toggle == "light grey"):
        screen.fill((125, 125, 125))
    elif (back_toggle == "dark grey"):
        screen.fill((75, 75, 75))
    
    timer = pygame.time.get_ticks()
    for p in polygons:
        poly_string = ""
        np = p  # I'm gonna be rich
        change_att = get_poly_attribute(p, "change")
        change_ind = get_att_index(p, ["change"])
        change_var = False
        if isinstance(change_ind, type(None)):
            change_ind = len(p)
            change_var = True
        if (change_att != None and vary):
            timer = pygame.time.get_ticks()
            # if (timer > math.pow(10, get_poly_attribute(p, "change")) and int(str(timer)[-get_poly_attribute(p, "change"):]) < clock.get_fps() / 4):  # WHAT IN THE ACTUAL HELL IS THIS SUPPOSE TO DO? @PAST ME
            if change_var or is_int(change_att) or len(change_att) < 3 or change_att[2] > timer + change_att[1]:
                if len(p[2][change_ind]) < 3:
                    p[2][change_ind] = list(p[2][change_ind])
                    p[2][change_ind].append("")
                p[2][change_ind][2] = timer
                tsprite = sprite()
                tsprite.add_polygon(p[0], p[1], p[2])
                np = gen_variations(tsprite).polygons[0]
                for poly_point in p[0]:
                    poly_string += str(poly_point[0]) + str(poly_point[1])
                change_points[poly_string] = np
            else:
                for poly_point in p[0]:
                    poly_string += str(poly_point[0]) + str(poly_point[1])
                if poly_string in change_points:
                    np = change_points[poly_string]
        poly_points = np[0]
        color = np[1]
        if (not get_poly_attribute(np, "Invisible")):
            if (not filled):
                line_points = points_from_poly(poly_points)
                for p1 in range(1, len(line_points) - 1):
                    pygame.draw.line(screen, color, line_points[p1 - 1], line_points[p1])
                for p1 in poly_points:
                    if p == polygons[len(polygons) - 1] and p1 == poly_points[len(poly_points) - 1] and not vary and len(points) > 0: 
                        if (timer > 100 and int(str(timer)[-3]) % 2 == 0): 
                            pygame.draw.circle(screen, (245, 251, 37), p1, 3)
                        else:
                            pygame.draw.circle(screen, (191, 196, 30), p1, 3) 
                    else:
                        pygame.draw.circle(screen, color, p1, 2)
            else:
                if (len(poly_points) > 2):
                    pygame.draw.polygon(screen, color, poly_points)
        elif not vary:
            timer = pygame.time.get_ticks()
            line_points = points_from_poly(poly_points)
            if (timer > 1000 and int(str(timer)[-4]) % 2 == 0):
                line_odd = True
            else:
                line_odd = False
            for p1 in range(1, len(line_points) - 1):
                if line_odd:
                    pygame.draw.line(screen, color, line_points[p1 - 1], line_points[p1])
                line_odd = not line_odd
    timer = pygame.time.get_ticks()
    if (grid):
        for r in range(0, base_resolution[0], 25): 
            if (timer > 1000 and int(str(timer)[-3]) % 2 == 0):
                pygame.draw.line(screen, (59, 232, 25), (r, 0), (r, base_resolution[1]))
            else:
                pygame.draw.line(screen, (41, 182, 13), (r, 0), (r, base_resolution[1]))
        for r in range(0, base_resolution[1], 25): 
            if (timer > 1000 and int(str(timer)[-3]) % 2 == 0):
                pygame.draw.line(screen, (59, 232, 25), (0, r), (base_resolution[0], r))
            else:
                pygame.draw.line(screen, (41, 182, 13), (0, r), (base_resolution[0], r))

def get_att_index(poly, att):
    """Returns index of given attribute if found"""
    j = 0
    if isinstance(poly[2], type(None)):
        return None
    for _att in poly[2]:
        if _att[0] == att[0]:
            return j
        j += 1
    return None

def get_input(text, label):
    global prompt
    global typing
    global type_string
    global input_label
    input_label = label
    prompt = text
    typing = True
    type_string = ""
    
def execute_string(string):
    global input_label
    global last_color
    global color
    global display_text
    global poly_num
    global placing
    global poly_radius
    global poly_width
    global poly_height
    global more_input
    global line_angle
    global zoom_level
    global delete
    global scaling
    
    if (input_label == "overwrite"):
        more_input = False
        if (string != "" and not (string == "scale" and scale)):
            pygame.display.set_caption(str(string) + " : " + str(stype))
            sprite1.polygons = fix_boundaries(sprite1.polygons)
            save(False, string)
        elif string == "":
            sprite1.polygons = fix_boundaries(sprite1.polygons)
            save(True)
        elif string == "scale" and scaling:
            sprite1.polygons = scale(sprite1.polygons, base_resolution)
            save(True)
        scaling = False
    elif (input_label == "color"):
        string = string.replace(".", "")
        display_text = ""
        color_string = string.replace(" ", "").split(",")
        if type_string.replace(" ", "") == "":
            color = last_color
        else:
            if (len(color_string) > 0 and is_int(color_string[0]) and int(color_string[0]) <= 255):
                r = int(color_string[0])
            else:
                r = 0
            if (len(color_string) > 1 and is_int(color_string[1]) and int(color_string[1]) <= 255):
                g = int(color_string[1])
            else:
                g = 0
            if (len(color_string) > 2 and is_int(color_string[2]) and int(color_string[2]) <= 255):
                b = int(color_string[2])
            else:
                b = 0
            color = (r, g, b)
        last_color = color
        
    elif input_label == "polygon":
        display_text = ""
        if string != "":
            more_input = True
        if string == "square" or string == "s":
            get_input("Enter the radius: ", "square")
        if string == "circle" or string == "c":
            get_input("Enter the radius: ", "circle")
        elif string == "rectangle" or string == "r":
            get_input("Enter the width, height: ", "rect")
        elif string == "line" or string == "l":
            get_input("Enter the angle in standard pos: ", "line")
    elif input_label == "zoom":
        if (is_int(string)):
            if (int(string) > 1 and int(string) <= min(base_resolution[0], base_resolution[1]) / 10):
                zoom_level = int(string)
                placing = "zoom"
    elif (input_label == "square"):
        if (is_int(string)):
            placing = "square"
            poly_radius = int(string)
        more_input = False
    elif (input_label == "line"):
        if (is_int(string) and int(string) <= 360):
            if (int(string) == 0):
                string = 360
            placing = "line"
            line_angle = int(string)
        more_input = False
    elif (input_label == "circle"):
        if (is_int(string)):
            placing = "circle"
            poly_radius = int(string)
        more_input = False
    elif (input_label == "rect"):
        if ("," in string):
            if (is_int(string.split(",")[0].replace(" ", "")) and is_int(string.split(",")[1].replace(" ", ""))):
                placing = "rect"
                poly_height = int(string.split(",")[1].replace(" ", ""))
                poly_width = int(string.split(",")[0].replace(" ", ""))
        more_input = False
    elif (input_label == "attributes"):
        if (string == ""):
            poly_num += 1
            if poly_num >= len(sprite1.polygons):
                poly_num = -1
            display_text = ""
        else:
            if string.startswith("color") and "," in string and len(string.split(",")) > 3:
                    sprite1.polygons[poly_num][1] = (int(string.split(",")[1].strip()), int(string.split(",")[2].strip()), int(string.split(",")[3].strip()))
                    display_text = ""
            else:
                sprite1.polygons[poly_num][2] = add_attribute(string, sprite1.polygons[poly_num])
                display_text = ""
    elif (input_label == "all attributes"):
        if (string != ""):
            for i in range(0, len(sprite1.polygons)):
                if string.startswith("color") and "," in string and len(
                        string.split(",")) > 3:
                    sprite1.polygons[i][1] = (
                    int(string.split(",")[1].strip()),
                    int(string.split(",")[2].strip()),
                    int(string.split(",")[3].strip()))
                    display_text = ""
                else:
                    sprite1.polygons[i][2] = add_attribute(string, sprite1.polygons[i])
    elif (input_label == "delete"):
        if (string == "y"):
            sprite1.polygons.pop(poly_num)
            if len(sprite1.polygons) < 1 or poly_num == len(sprite1.polygons):
                poly_num = -1
                delete = False
        else:
            poly_num += 1
            if poly_num >= len(sprite1.polygons):
                poly_num = -1
                delete = False
    elif input_label == "resolution":
        string = string.replace(".", "")
        if string != "" and "," in string:
            if len(string.split(",")) > 1 and is_int(string.split(",")[0].strip()) and is_int(string.split(",")[1].strip()):
                more_input = True
                new_resolution = (int(string.split(",")[0].strip()) + margin, int(string.split(",")[1].strip()) + margin)
                change_resolution(new_resolution)
        elif string == "fit":
            npolies = []
            shiftf = (-1 * get_boundaries(sprite1)[0], -1 * get_boundaries(sprite1)[1])
            for poly in sprite1.polygons:
                npolies.append(shift_points(poly, shiftf))
            sprite1.polygons = npolies
            change_resolution((get_boundaries(sprite1)[2], get_boundaries(sprite1)[3]))
            
def change_resolution(new_resolution=None, event=None, asksave=True):  
    global screen
    global last_point
    global points
    global scaling
    global last_size
    global back_odd
    global back_i
    global current_size
    global display
    global base_resolution

    if event != None:
        current_size = event.dict['size']
    else:
        current_size = (new_resolution[0] + margin, new_resolution[1] + margin)
    if (current_size != last_size and main_loop_count > 2):
        back_odd = False
        back_i = -1
        display = pygame.display.set_mode(current_size , pygame.RESIZABLE)
        base_resolution = (current_size[0] - margin, current_size[1] - margin)
        screen = pygame.Surface(base_resolution)
        pygame.display.set_caption(str(current_file) + " : " + str(stype))
        label = myfont.render((str(base_resolution[0]) + " " + str(base_resolution[1])), 1, (255, 255, 0))
        display.blit(label, (0, 0))
        if asksave:
            last_point = (-1, -1)
            points = []
            scaling = True
            get_input("Save as? (\"\" for overwrite or \"scale\" for scale): ", "overwrite")
        
    last_size = current_size
    pygame.display.flip()
    

def add_attribute(string, poly):
    atts = []
    if ("," in string):
        att = (string.split(",")[0].strip(), string[len(string.split(",")[0]) + 1:].strip())
    else:
        att = (string.strip(), "True")
    if (poly[2] != None):
        for a in poly[2]:
            atts.append(a)
    atts.append(att)
    return atts

def get_poly_attribute(poly, attribute):
    if (poly[2] != None):
        for a in poly[2]:
            if a[0] == attribute:
                returns = []
                if "," in str(a[1]):
                    for att in a[1].split(","):
                        att = att.strip()
                        if att == "True":
                            returns.append(True)
                        elif att == "False":
                            returns.append(False)
                        elif is_int(att):
                            returns.append(int(att))
                        else:
                            returns.append(att)
                    return returns
                else:
                    att = str(a[1]).strip()
                    if att == "True":
                        return True
                    elif att == "False":
                        return False
                    elif is_int(att):
                        return int(att)
                    elif attribute == "attach":
                        return [att]
                    return att
    return None

def to_HSL(color):
    color = [(float)(color[0])/255,(float)(color[1])/255,(float)(color[2])/255]
    color = colorsys.rgb_to_hls(color[0],color[1],color[2])
    return color
def to_RGB(ncolor):
    ncolor = colorsys.hls_to_rgb(ncolor[0],ncolor[1],ncolor[2])
    ncolor = [(float)(ncolor[0])*255,(float)(ncolor[1])*255,(float)(ncolor[2])*255]
    return ncolor
def get_LUMA(color):
    return (0.2126*color[0] + 0.7152*color[1] + 0.0722*color[2])

def next_file(cdir):
    lf = 0
    if (os.path.isdir(cdir)):
        for f in os.listdir(cdir):
            if is_int(f.split(".")[0]):
                if (int(f.split(".")[0]) > lf):
                    lf = int(f.split(".")[0])
        num = lf + 1
        return num
    else:
        os.mkdir(cdir)
        return 1

def getCharacter(event):
    keyinput = pygame.key.get_pressed()  
    character = "NULL"
    keyPress = event.key
    if keyPress >= 32 and keyPress <= 126:
        if keyinput[pygame.K_LSHIFT]: 
            keyPress -= 32
        character = chr(keyPress)
    return character


def shift_points(poly, shiftf):
    npoly = []
    for point in poly[0]:
        npoly.append((point[0] + shiftf[0], point[1] + shiftf[1]))
    return (npoly, poly[1], poly[2])


def dist(point1, point2):
    return math.sqrt(
        (point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)


def angle_wrt_x(point1, point2):
    """Modified from here:
    https://stackoverflow.com/a/13544022
    """
    ax, ay = point1
    bx, by = point2
    return math.degrees(math.atan2(by - ay, bx - ax))


def point_pos(point, d, theta):
    """Found here:
    https://stackoverflow.com/a/23280722
    """
    x0 = point[0]
    y0 = point[1]
    theta_rad = math.pi / 2 - math.radians(theta)
    return x0 + d * math.sin(theta_rad), y0 + d * math.cos(theta_rad)


def mirrored(point, points):
    if mirror[0][0] != -1:
        lp = 10000000000000000000000000000000000
        np = point
        i = 0
        for p in get_line(mirror[0], mirror[1]):
            if (dist(point, p) < lp):
                lp = dist(point, p)
                np = p
            i += 1
        new_point = point_pos(point, 2 * int(dist(point, np)),
                              angle_wrt_x(point, np))

        return add_mirror(check_boundaries(new_point), points)
    else:
        return points


def add_mirror(point, points):
    npoints = []
    npoints.append(point)
    for p in points:
        npoints.append(p)
    return npoints


def check_mirror(points):
    fd = 0
    fpoint = points[0]
    for point in points:
        if dist(fpoint, point) > fd:
            fd = dist(fpoint, point)
            fp = point
    line_points = get_line(fpoint, fp)
    for point in points:
        if (not point in line_points):
            return False
    return fp


def fix_boundaries(polys):
    new_polys = []
    for poly in polys:
        new_poly = []
        for point in poly[0]:
            new_point = check_boundaries(point)
            new_poly.append(new_point)
        new_polys.append([new_poly, poly[1], poly[2]])
    return new_polys


def reposition(point):
    lp = 100
    np = point
    if len(current_points) > 2:
        polies = sprite1.polygons[0:len(sprite1.polygons) - 1]
    else:
        polies = sprite1.polygons
    for poly in polies:
        for p in poly[0]:
            if (abs(point[0] - p[0]) + abs(point[1] - p[1]) <= ((min(
                    base_resolution[0],
                    base_resolution[1]) / zoom_level) / 20) and abs(
                    point[0] - p[0]) + abs(point[1] - p[1]) < lp):
                lp = abs(point[0] - p[0]) + abs(point[1] - p[1])
                np = p
    if np == point:
        for poly in polies:
            for p in points_from_poly(poly[0]):
                if (abs(point[0] - p[0]) + abs(point[1] - p[1]) <= ((min(
                        base_resolution[0],
                        base_resolution[1]) / zoom_level) / 20) and abs(
                        point[0] - p[0]) + abs(point[1] - p[1]) < lp):
                    lp = abs(point[0] - p[0]) + abs(point[1] - p[1])
                    np = p
    return (int(np[0]), int(np[1]))


def point_shift():
    point = (pygame.mouse.get_pos()[0] - int(margin / 2),
             pygame.mouse.get_pos()[1] - int(margin / 2))
    if zoom_point[0] != -1:
        point = (
        (point[0] * ((base_resolution[0] / zoom_level) / base_resolution[0])) +
        zoom_rect[0],
        (point[1] * ((base_resolution[1] / zoom_level) / base_resolution[1])) +
        zoom_rect[1])
    return (int(point[0]), int(point[1]))


def check_boundaries(point):
    cpoint1 = []
    cpoint2 = []
    bounding_rect = (0, 0, base_resolution[0], base_resolution[1])
    if zoom_point[0] != -1:
        bounding_rect = (
        zoom_rect[0], zoom_rect[1], zoom_rect[0] + zoom_rect[2],
        zoom_rect[1] + zoom_rect[3])
    if (point[0] < bounding_rect[0]):
        cpoint1.append(bounding_rect[0])
    else:
        cpoint1.append(point[0])
    if (point[1] < bounding_rect[1]):
        cpoint1.append(bounding_rect[1])
    else:
        cpoint1.append(point[1])
    if (cpoint1[0] > bounding_rect[2]):
        cpoint2.append(bounding_rect[2])
    else:
        cpoint2.append(cpoint1[0])
    if (cpoint1[1] > bounding_rect[3]):
        cpoint2.append(bounding_rect[3])
    else:
        cpoint2.append(cpoint1[1])
    return (int(cpoint2[0]), int(cpoint2[1]))


def to_rect(points):
    xvals = []
    yvals = []
    for point in points:
        if not point[0] in xvals:
            xvals.append(point[0])
        if not point[1] in yvals:
            yvals.append(point[1])
    a = min(xvals)
    b = min(yvals)
    c = max(xvals) - a
    d = max(yvals) - b
    return (int(a), int(b), int(c), int(d))


def get_boundaries(bsprite):
    prect = []
    for poly in bsprite.polygons:
        for point in poly[0]:
            prect.append(point)
    return to_rect(prect)


def get_line(start, end):
    """Bresenham's Line Algorithm found here:
    http://www.roguebasin.com/index.php?title=Bresenham%27s_Line_Algorithm
    """
    x1, y1 = start
    x2, y2 = end
    dx = x2 - x1
    dy = y2 - y1
    is_steep = abs(dy) > abs(dx)
    if is_steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2
    swapped = False
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
        swapped = True
    dx = x2 - x1
    dy = y2 - y1
    error = int(dx / 2.0)
    ystep = 1 if y1 < y2 else -1
    y = y1
    points = []
    for x in range(x1, x2 + 1):
        coord = (y, x) if is_steep else (x, y)
        points.append(coord)
        error -= abs(dy)
        if error < 0:
            y += ystep
            error += dx
    if swapped:
        points.reverse()
    return points


def get_pairs(points):
    pair1 = []
    pair2 = []
    pairs = []
    p2 = False
    for point in points:
        pair1.append(point)
        if len(pair1) == 2:
            pairs.append(pair1)
            pair1 = []
        if p2:
            pair2.append(point)
        if len(pair2) == 2:
            pairs.append(pair2)
            pair2 = []
        p2 = True
    return pairs


def check_complex(points, point, index):
    if len(points) > 1:
        lpoint = points[index]
        if len(points) < index + 2:
            npoint = points[0]
        else:
            npoint = points[index + 1]
        pairs = get_pairs(points)
        for pair in pairs:
            if (closed_segment_intersect(pair[0], pair[1], lpoint,
                                         point) != False and pair[
                0] != point and pair[1] != point and pair[0] != lpoint and pair[
                1] != lpoint):
                return True
            if (closed_segment_intersect(pair[0], pair[1], npoint,
                                         point) != False and pair[
                0] != npoint and pair[1] != npoint):
                return True
        return False
    return None


def get_simple(points, point, index, panic=False, margin=7):
    if len(points) > 1:
        lpoint = points[index]
        npoint = point
        d = int(dist(point, lpoint))
        while check_complex(points, npoint, len(points) - 1):
            npoint = point_pos(lpoint, d, angle_wrt_x(lpoint, point))
            npoint = (int(npoint[0]), int(npoint[1]))
            d -= 1
            if d < 1:
                if panic:
                    d = int(dist(point, lpoint))
                    angle = angle_wrt_x(lpoint, point) - 90
                    if angle < 1:
                        angle += 360
                    while check_complex(points, npoint, len(points) - 1):
                        npoint = point_pos(lpoint, d, angle)
                        npoint = (int(npoint[0]), int(npoint[1]))
                        d -= 1
                        if d < 1:
                            d = int(dist(point, lpoint))
                            angle = angle_wrt_x(lpoint, point) + 90
                            if angle > 360:
                                angle -= 360
                            while check_complex(points, npoint,
                                                len(points) - 1):
                                npoint = point_pos(lpoint, d, angle)
                                npoint = (int(npoint[0]), int(npoint[1]))
                                d -= 1
                                if d < 1:
                                    return None
                            if int(dist(npoint,
                                        lpoint)) < margin and not check_complex(
                                    points, point_pos(lpoint, int(
                                            dist(npoint, lpoint)) + margin,
                                                      angle), len(points) - 1):
                                npoint = point_pos(lpoint, int(
                                    dist(npoint, lpoint)) + margin, angle)
                                npoint = (int(npoint[0]), int(npoint[1]))
                            return npoint
                    if int(dist(npoint, lpoint)) < margin and not check_complex(
                            points, point_pos(lpoint, int(
                                    dist(npoint, lpoint)) + margin, angle),
                            len(points) - 1):
                        npoint = point_pos(lpoint,
                                           int(dist(npoint, lpoint)) + margin,
                                           angle)
                        npoint = (int(npoint[0]), int(npoint[1]))
                    return npoint
                return None
        if int(dist(npoint, lpoint)) > margin:
            npoint = point_pos(lpoint, int(dist(npoint, lpoint)) - margin,
                               angle_wrt_x(lpoint, point))
            npoint = (int(npoint[0]), int(npoint[1]))
        else:
            npoint = point_pos(lpoint, 1, angle_wrt_x(lpoint, point))
            npoint = (int(npoint[0]), int(npoint[1]))
        return npoint


def side(a, b, c):
    """ Returns a position of the point c relative to the line going through a and b
        Points a, b are expected to be different
    """
    d = (c[1] - a[1]) * (b[0] - a[0]) - (b[1] - a[1]) * (c[0] - a[0])
    return 1 if d > 0 else (-1 if d < 0 else 0)


def is_point_in_closed_segment(a, b, c):
    """ Returns True if c is inside closed segment, False otherwise.
        a, b, c are expected to be collinear
    """
    if a[0] < b[0]:
        return a[0] <= c[0] and c[0] <= b[0]
    if b[0] < a[0]:
        return b[0] <= c[0] and c[0] <= a[0]

    if a[1] < b[1]:
        return a[1] <= c[1] and c[1] <= b[1]
    if b[1] < a[1]:
        return b[1] <= c[1] and c[1] <= a[1]

    return a[0] == c[0] and a[1] == c[1]


def closed_segment_intersect(a, b, c, d):
    """ Verifies if closed segments a, b, c, d do intersect.
    """
    if a == b:
        return a == c or a == d
    if c == d:
        return c == a or c == b

    s1 = side(a, b, c)
    s2 = side(a, b, d)

    # All points are collinear
    if s1 == 0 and s2 == 0:
        return \
            is_point_in_closed_segment(a, b, c) or is_point_in_closed_segment(a,
                                                                              b,
                                                                              d) or \
            is_point_in_closed_segment(c, d, a) or is_point_in_closed_segment(c,
                                                                              d,
                                                                              b)

    # No touching and on the same side
    if s1 and s1 == s2:
        return False

    s1 = side(c, d, a)
    s2 = side(c, d, b)

    # No touching and on the same side
    if s1 and s1 == s2:
        return False

    return True


def points_from_poly(poly, spacing=3):
    last_point = (-1, 0)
    line_points = []
    for p in range(0, len(poly) + spacing):
        if p < len(poly):
            point = poly[p]
        else:
            point = poly[0]
        if (last_point[0] != -1):
            i = 0
            for po in get_line(last_point, point):
                if (i == spacing):
                    line_points.append(po)
                    i = 0
                i += 1
        last_point = point
    return line_points


def scale(polys, resolution, original_size=None):
    if original_size == None:
        original_size = sprite1.get_attribute("size")
    new_polys = []
    for poly in polys:
        new_poly = []
        for point in poly[0]:
            new_point = (int(point[0] * (resolution[0] / original_size[0])),
                         int(point[1] * (resolution[1] / original_size[1])))
            new_poly.append(new_point)
        new_polys.append([new_poly, poly[1], poly[2]])
    return new_polys

def square(point):
    poly_points = []
    poly_points.append((int(point[0] - poly_radius), int(point[1] - poly_radius)))
    poly_points.append((int(point[0] + poly_radius), int(point[1] - poly_radius)))
    poly_points.append((int(point[0] + poly_radius), int(point[1] + poly_radius)))
    poly_points.append((int(point[0] - poly_radius), int(point[1] + poly_radius)))
    return poly_points

def circle(center):
    list_points = []
    points = int(math.pi * (2 * poly_radius))
    segment = 2 * math.pi / points
    for i in range(0,points):
        angle = segment * i
        newX = center[0] + poly_radius * math.cos(angle)
        newY = center[1] + poly_radius * math.sin(angle)
        point = (int(newX), int(newY))
        list_points.append((int(point[0]), int(point[1])))
    return list_points

def rect(point):
    poly_points = []
    poly_points.append((int(point[0] - poly_width /2), int(point[1] - poly_height /2)))
    poly_points.append((int(point[0] + poly_width /2), int(point[1] - poly_height /2)))
    poly_points.append((int(point[0] + poly_width /2), int(point[1] + poly_height /2)))
    poly_points.append((int(point[0] - poly_width /2), int(point[1] + poly_height /2)))
    return poly_points

def line(point):
    end_point = point_pos(line_start, int(math.sqrt(base_resolution[0]**2 + base_resolution[1]**2)), line_angle)
    end_point = (int(end_point[0]), int(end_point[1]))
    if (line_angle > 180):
        angle = line_angle - 180
    elif (line_angle < 180):
        angle = line_angle + 180
    else:
        angle = 360
    start_point = point_pos(line_start, int(math.sqrt(base_resolution[0]**2 + base_resolution[1]**2)), angle)
    start_point = (int(start_point[0]), int(start_point[1]))
    ld = 100000000000000000000
    np = line_start
    for i in get_line(start_point, end_point):
        if dist(point, i) < ld:
            ld = dist(point, i)
            np = i
    return (int(np[0]), int(np[1]))


def clean_polies():
    i = 0
    for poly in sprite1.polygons:
        if len(poly[0]) < 2:
            sprite1.polygons.pop(i)
        i += 1


def check_polies(poly):
    for p in sprite1.polygons:
        if (poly[0] == p[0] and poly[1] == p[1]):
            return False
    return True


def gen_sprite():
    base_sprite = sprite()
    get_attach_points(gen_variations(sprite1), base_sprite, sprite1.stype)
    return base_sprite


def pick_sprite(path):
    file = os.listdir(
        "C:\\Users\\" + getpass.getuser() + "\\Desktop\\sprites\\" + path)[
        random.randint(0, len(os.listdir(
            "C:\\Users\\" + getpass.getuser() + "\\Desktop\\sprites\\" + path)) - 1)]
    inp = open(
        "C:\\Users\\" + getpass.getuser() + "\\Desktop\\sprites\\" + path + "\\" + file,
        'r')
    bsprite = jsonpickle.decode(json.load(inp))
    inp.close()
    bsprite = gen_variations(bsprite)
    return bsprite


def gen_variations(base_sprite=None):
    if base_sprite == None:
        base_sprite = sprite1
    new_points = {}
    new_colors = {}
    sprite2 = sprite()
    for poly in base_sprite.polygons:
        npoly = poly[0]
        if (len(poly[0]) > 2):
            if get_poly_attribute(poly, "genshape") != None:
                rad = get_poly_attribute(poly, "genshape")[0]
                interval = get_poly_attribute(poly, "genshape")[1]
                npoly = []
                pn = 0
                for point in poly[0]:
                    next_point = False
                    for p in new_points.keys():
                        if point == p:
                            npoint = new_points[p]
                            next_point = True
                            break
                    if not next_point:
                        npoint = point
                        if random.randint(0, interval) == 0:
                            npoint = (
                            point[0] + random.randint(0, rad) if random.choice(
                                (True, False)) else point[0] - random.randint(0,
                                                                              rad),
                            point[1] + random.randint(0, rad) if random.choice(
                                (True, False)) else point[1] - random.randint(0,
                                                                              rad))
                            npoint = check_boundaries(npoint)
                            if get_poly_attribute(poly, "complex") != True:
                                if pn != 0 and check_complex(npoly, npoint,
                                                             pn - 1):
                                    npoint = get_simple(npoly, npoint, pn - 1,
                                                        True)
                                    if npoint == None:
                                        npoint = point
                        new_points[point] = npoint
                    npoly.append(npoint)
                    pn += 1
        if get_poly_attribute(poly, "gencolor") != None:
            hue_var = get_poly_attribute(poly, "gencolor")[0]
            sat_var = get_poly_attribute(poly, "gencolor")[1]
            light_var = get_poly_attribute(poly, "gencolor")[2]
            ncolor = []
            next_color = False
            for c in new_colors.keys():
                if str(poly[1][0]) + str(poly[1][1]) + str(poly[1][2]) == c:
                    ncolor = new_colors[c]
                    next_color = True
                    break
            if not next_color:
                pcolor = to_HSL(poly[1])
                pcolor = (
                (pcolor[0] * 360), (pcolor[1] * 100), (pcolor[2] * 100))
                ncolor = (
                pcolor[0] - random.randint(0, hue_var) if random.choice(
                    (True, False)) else pcolor[0] + random.randint(0, hue_var),
                pcolor[1] - random.randint(0, sat_var) if random.choice(
                    (True, False)) else pcolor[1] + random.randint(0, sat_var),
                pcolor[2] - random.randint(0, light_var) if random.choice(
                    (True, False)) else pcolor[2] + random.randint(0,
                                                                   light_var))
                new_colors[str(poly[1][0]) + str(poly[1][1]) + str(
                    poly[1][2])] = ncolor
            nncolor = []
            if ncolor[0] > 360:
                nncolor.append((ncolor[0] - 360) / 360)
            elif ncolor[0] < 0:
                nncolor.append((ncolor[0] + 360) / 360)
            else:
                nncolor.append((ncolor[0]) / 360)
            if ncolor[1] > 100:
                nncolor.append(1)
            elif ncolor[1] < 0:
                nncolor.append(0)
            else:
                nncolor.append(float(ncolor[1]) / 100)
            if ncolor[2] > 100:
                nncolor.append(1)
            elif ncolor[2] < 0:
                nncolor.append(0)
            else:
                nncolor.append(float(ncolor[2]) / 100)
            ncolor = to_RGB(nncolor)
        else:
            ncolor = poly[1]

        sprite2.add_polygon(npoly, ncolor, poly[2])
    return sprite2


def get_attach_points(bsprite, base_sprite, apath=None, ppoints=None,
                      ppath=None, attributes=[]):
    shift_factor = (0, 0)
    ppoints_size = (1, 1)
    poly_size = (1, 1)
    if ppath != None:
        for poly in bsprite.polygons:
            if get_poly_attribute(poly, "attach") != None:
                if get_poly_attribute(poly, "attach")[0] == ppath:
                    if ppoints != None:
                        ppoints_size = (
                        to_rect(ppoints)[2], to_rect(ppoints)[3])
                        poly_size = (to_rect(poly[0])[2], to_rect(poly[0])[3])
                        npolies = []
                        npolies.append(poly)
                        scaledp = scale(npolies, ppoints_size, poly_size)[0]
                        shift_factor = (
                        to_rect(ppoints)[0] - to_rect(scaledp[0])[0],
                        to_rect(ppoints)[1] - to_rect(scaledp[0])[1])
                    break
    for poly in bsprite.polygons:
        if get_poly_attribute(poly, "attach") != None:
            if get_poly_attribute(poly, "attach")[0] != ppath:
                path = get_poly_attribute(poly, "attach")[0]
                npolies = []
                npolies.append(poly)
                np = scale(npolies, ppoints_size, poly_size)[0]
                np = shift_points(np, shift_factor)
                attributes = []
                i = 0
                for att in get_poly_attribute(np, "attach"):
                    if i > 0:
                        attributes.append((att, get_poly_attribute(np, att)))
                    i += 1
                get_attach_points(pick_sprite(path), base_sprite, path, np[0],
                                  apath, attributes)
        elif get_poly_attribute(poly, "attach") == None:
            npolies = []
            npolies.append(poly)
            np = scale(npolies, ppoints_size, poly_size)[0]
            np = shift_points(np, shift_factor)
            attributes1 = attributes
            if np[2] != None:
                for att in np[2]:
                    attributes1.append(att)
            base_sprite.add_polygon(np[0], np[1], attributes1)

def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
    except TypeError:
        return False


def crop(surface, rect):
    rect = pygame.Rect(rect)
    new = pygame.Surface(rect.size, 0, surface)
    new.blit(surface, (0, 0), rect)
    return new


back_list = ["grey move", "black move", "white", "black", "light grey", "dark grey"]

current_file = -1
last_color = (255, 255, 255)
margin = 100
back_odd = False
back_i = -1
prompt = ""
input_label = ""
back_toggle = "grey move"
back_tnum = 0
grid = False
last_point = (-1, -1)
vary = False
change_points = {}

if (input("New Sprite? ") == "y"):
    stype = input("Type: ")
    if (stype == ""):
        stype = "Miscellaneous"
    sname = input("Name: ")
    if (sname == ""):
        sname = next_file("C:\\Users\\" + getpass.getuser() + "\\Desktop\\sprites\\" + stype + "\\")
    sprite1 = sprite(stype, sname)
    if (not os.path.isdir("C:\\Users\\" + getpass.getuser() + "\\Desktop\\sprites\\" + sprite1.stype + "\\")):
        if "\\" in sprite1.stype:
            dirpath = ""
            for folder in sprite1.stype.split("\\"):
                dirpath += folder + "\\"
                if not os.path.isdir("C:\\Users\\" + getpass.getuser() + "\\Desktop\\sprites\\" + dirpath):
                    os.mkdir("C:\\Users\\" + getpass.getuser() + "\\Desktop\\sprites\\" + dirpath)
        else:
            os.mkdir("C:\\Users\\" + getpass.getuser() + "\\Desktop\\sprites\\" + sprite1.stype + "\\")
    x = input("X: ")
    if (x == ""):
        x = 500
        y = 500
    else:
        y = input("Y: ")
    current_file = sprite1.name
    base_resolution = (int(x), int(y))
    display_resolution = (base_resolution[0] + margin, base_resolution[1] + margin)
    sprite1.add_attribute(["size", base_resolution])
    color = (255, 255, 255)
    points = []
    screen = pygame.Surface(base_resolution)
    display = pygame.display.set_mode(display_resolution, pygame.RESIZABLE)
    pygame.display.set_caption(str(current_file) + " : " + str(stype))
    pygame.display.flip()
else:
    stype = input("Type? ")
    if stype == "":
        stype = "Miscellaneous"
    cdir = "C:\\Users\\" + getpass.getuser() + "\\Desktop\\sprites\\" + stype + "\\"
    if (os.path.isdir(cdir)):
        if (len(os.listdir(cdir)) > 0):
            print(os.listdir(cdir))
            current_file = input("Which Sprite? ")
            if os.path.isfile(cdir + current_file + ".json"):
                inp = open(cdir + current_file + ".json", 'r')
                sprite1 = jsonpickle.decode(json.load(inp))
                inp.close()
                points = []
                color = (255, 255, 255)
                last_color = color
                base_resolution = sprite1.get_attribute("size")
                display_resolution = (base_resolution[0] + margin, base_resolution[1] + margin)
                screen = pygame.Surface(base_resolution)
                display = pygame.display.set_mode(display_resolution, pygame.RESIZABLE)
                pygame.display.set_caption(str(current_file) + " : " + str(stype))
                pygame.display.flip()
                draw_from_file(False, sprite1.polygons)
            else:
                print("Is not a file")
                quit()
        else:
            print("Nothing saved here")
            quit()
    else:
        print("Is not a saved file type")
        quit()

myfont = pygame.font.SysFont("monospace", 15)
label = myfont.render((str(base_resolution[0]) + " " + str(base_resolution[1])), 1, (255, 255, 0))
display.blit(label, (0, 0))
last_pos = (-1, -1)

pygame.display.update()

last_size = base_resolution
filled = False
leftclick = False
last_press = -1000
last_click = -1000
first = True
main_loop_count = 0
typing = False
type_string = ""
poly_num = -1
display_text = ""
lock_points = False
mirror = ((-1, -1), (-1, -1))
reflect = False
placing = ""
poly_radius = 0
poly_height = 0
poly_width = 0
more_input = False
line_start = (-1, -1)
line_angle = 0
zoom_level = 1
zoom_point = (-1, -1)
current_points = ()
delete = False
scaling = False
restricted = False
zoom_rect = (0, 0, base_resolution[0], base_resolution[1])
sprite_paths = []

while True:
    tools_text = ""
    main_loop_count += 1
    pygame.event.pump()
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        save(True)
        pygame.display.quit()
        quit()
        
    elif event.type == pygame.VIDEORESIZE:
        change_resolution(None, event)
    
    if (not typing):
        if (event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] == 1):
            leftclick = True
        if (event.type == pygame.MOUSEBUTTONUP and pygame.mouse.get_pressed()[0] != 1):
            leftclick = False
            if (line_start[0] != -1):
                line_start = (-1, -1)
                last_point = (-1, -1)
                points = []
                save(True)
        if(pygame.key.get_pressed()[pygame.K_c] != 0 and not vary):
            if (pygame.time.get_ticks() > last_press + 150):
                last_press = pygame.time.get_ticks()
                last_point = (-1, -1)
                points = []
                display_text = "Previous Color: " + str(last_color[0]) + ", " + str(last_color[1]) + ", " + str(last_color[2])
                get_input("Enter Colors in R,G,B format: ", "color")
                save(True)
        if(pygame.key.get_pressed()[pygame.K_n] != 0 and not vary):
            if (pygame.time.get_ticks() > last_press + 150):
                last_press = pygame.time.get_ticks()
                last_point = (-1, -1)
                points = []
                save(True)
        if(pygame.key.get_pressed()[pygame.K_F1] != 0 and not vary):
            if (pygame.time.get_ticks() > last_press + 150):
                last_press = pygame.time.get_ticks()
                last_point = (-1, -1)
                points = []
                save(True)
                get_input("Save file as: ", "overwrite")
        if(pygame.key.get_pressed()[pygame.K_s] != 0 and not vary):
            if (pygame.time.get_ticks() > last_press + 150):
                last_press = pygame.time.get_ticks()
                if placing == "":
                    display_text = "Square, Rectangle, Line, Circle"
                    get_input("Enter a shape: ", "polygon")
                else:
                    placing = ""
                    line_start = (-1, -1)
        if(pygame.key.get_pressed()[pygame.K_EQUALS] != 0):
            if (pygame.time.get_ticks() > last_press + 150):
                last_press = pygame.time.get_ticks()
                if zoom_level == 1:
                    get_input("Enter the zoom level: ", "zoom")
                else:
                    placing = ""
                    zoom_level = 1
                    zoom_point = (-1, -1)
        if(pygame.key.get_pressed()[pygame.K_v] != 0):
            if (pygame.time.get_ticks() > last_press + 150):
                last_press = pygame.time.get_ticks()
                vary = not vary
                if vary:
                    sprite_r = gen_sprite()
                    npolies = []
                    shiftf = (-1 * get_boundaries(sprite_r)[0], -1 * get_boundaries(sprite_r)[1])
                    sprite_r_size = get_boundaries(sprite_r)
                    for poly in sprite_r.polygons:
                        npolies.append(shift_points(poly, shiftf))
                    sprite_r.polygons = npolies
                    if sprite_r_size[2] > 1600:
                        sprite_r.polygons = scale(sprite_r.polygons, (1600, sprite_r_size[3]), sprite_r_size)
                    if sprite_r_size[3] > 900:
                        sprite_r.polygons = scale(sprite_r.polygons, (sprite_r_size[2], 900), sprite_r_size)
                    change_resolution((get_boundaries(sprite_r)[2], get_boundaries(sprite_r)[3]), None, False)
                else:
                    change_resolution(sprite1.get_attribute("size"), None, False)
        if(pygame.key.get_pressed()[pygame.K_f] != 0):
            if (pygame.time.get_ticks() > last_press + 150):
                last_press = pygame.time.get_ticks()
                filled = not filled
        if(pygame.key.get_pressed()[pygame.K_i] != 0 and not vary):
            if (pygame.time.get_ticks() > last_press + 150):
                last_press = pygame.time.get_ticks()
                restricted = not restricted
        if(pygame.key.get_pressed()[pygame.K_r] != 0 and not vary):
            if (pygame.time.get_ticks() > last_press + 150):
                last_press = pygame.time.get_ticks()
                get_input("New resolution: ", "resolution")
        if(pygame.key.get_pressed()[pygame.K_g] != 0):
            if (pygame.time.get_ticks() > last_press + 150):
                last_press = pygame.time.get_ticks()
                grid = not grid
        if(pygame.key.get_pressed()[pygame.K_z] != 0 and not vary):
            if (pygame.time.get_ticks() > last_press + 250):
                last_press = pygame.time.get_ticks()
                if (not pygame.key.get_pressed()[pygame.K_LSHIFT]):
                    if (len(sprite1.polygons) > 0):
                        sprite1.polygons.pop()
                    last_point = (-1, -1)
                    points = []
                    save(True)
                else:
                    if (len(sprite1.polygons) > 0 and len(sprite1.polygons[len(sprite1.polygons) - 1][0]) > 2):
                        sprite1.polygons[len(sprite1.polygons) - 1][0].pop()
                        if (reflect):
                            sprite1.polygons[len(sprite1.polygons) - 1][0].pop(0)
                    elif len(sprite1.polygons) > 0:
                        sprite1.polygons.pop()
                        last_point = (-1, -1)
                        points = []
                    save(True)
        if(pygame.key.get_pressed()[pygame.K_b] != 0):
            if (pygame.time.get_ticks() > last_press + 150):
                last_press = pygame.time.get_ticks()
                back_tnum += 1
                if back_tnum > 5:
                    back_tnum = 0
                back_toggle = back_list[back_tnum]
        if(pygame.key.get_pressed()[pygame.K_d] != 0 and not vary):
            if (pygame.time.get_ticks() > last_press + 150):
                last_press = pygame.time.get_ticks()
                if (not pygame.key.get_pressed()[pygame.K_LSHIFT]):
                    if (len(sprite1.polygons) > 0):
                        poly_num = 0
                        delete = True
                    last_point = (-1, -1)
                    points = []
                    save(True)
                else:
                    sprite1.polygons.clear()
                    last_point = (-1, -1)
                    points = []
                    get_input("Save file as (leave blank for overwrite): ", "overwrite")
        if(pygame.key.get_pressed()[pygame.K_a] != 0 and not vary):
            if (pygame.time.get_ticks() > last_press + 150):
                last_press = pygame.time.get_ticks()
                if (not pygame.key.get_pressed()[pygame.K_LSHIFT]):
                    if (len(sprite1.polygons) > 0):
                        poly_num = 0
                    last_point = (-1, -1)
                    points = []
                    save(True)
                else:
                    get_input("Add to all (att, value): ", "all attributes")
                    last_point = (-1, -1)
                    points = []
                    save(True)
        if(pygame.key.get_pressed()[pygame.K_l] != 0 and not vary):
            if (pygame.time.get_ticks() > last_press + 150):
                last_press = pygame.time.get_ticks()
                lock_points = not lock_points
        if(pygame.key.get_pressed()[pygame.K_m] != 0 and not vary):
            if (pygame.time.get_ticks() > last_press + 150):
                last_press = pygame.time.get_ticks()
                if (not pygame.key.get_pressed()[pygame.K_LSHIFT]):
                    reflect = not reflect
                    if reflect and mirror[0][0] == -1:
                        reflect = False
                else:
                    if (len(sprite1.polygons) > 0) and check_mirror(sprite1.polygons[len(sprite1.polygons) - 1][0]) != False:
                        mirror = ((sprite1.polygons[len(sprite1.polygons) - 1][0][0], check_mirror(sprite1.polygons[len(sprite1.polygons) - 1][0])))
                        mirror = (point_pos(mirror[0], int(math.sqrt(base_resolution[0] ** 2 + base_resolution[1] ** 2)), angle_wrt_x(mirror[0], mirror[1])), point_pos(mirror[1], int(math.sqrt(base_resolution[0] ** 2 + base_resolution[1] ** 2)), angle_wrt_x(mirror[1], mirror[0])))
                        mirror = ((int(mirror[0][0]), int(mirror[0][1])), (int(mirror[1][0]), int(mirror[1][1])))
                        sprite1.polygons.pop()
                        reflect = True
                        last_point = (-1, -1)
                        points = []
                        save(True)
        if (leftclick and pygame.time.get_ticks() > last_click + 70):
            last_click = pygame.time.get_ticks()
            point = point_shift()
            
            point = check_boundaries(point)
            
            if (lock_points):
                point = reposition(point)
            if (line_start[0] != -1):
                point = line(point)
            
            if (point != last_pos and (placing == "" or line_start[0] != -1) and not vary):
                if (check_complex(points, point, len(points) - 1) != True or not restricted):
                    points.append(point)
                else:
                    if get_simple(points, point, len(points) - 1, 5) != None:
                        points.append(get_simple(points, point, len(points) - 1, 5))
                    else:
                        point = False
                if point != False:
                    if (reflect):
                        points = mirrored(point, points)
                        if len(sprite1.polygons) > 0 and len(points) > 2:
                            sprite1.polygons.pop()
                    current_points = points
                    save(True)
                    last_pos = point
            elif placing != "":
                last_click = pygame.time.get_ticks() + 40
                if (line_start[0] == -1) and not vary:
                    points = []
                    last_point = (-1, -1)
                if placing == "square" and not vary:
                    for p in square(point):
                        points.append(p)
                if placing == "circle" and not vary:
                    for p in circle(point):
                        points.append(p)
                elif placing == "rect" and not vary:
                    for p in rect(point):
                        points.append(p)
                elif placing == "line" and not vary:
                    if (line_start[0] == -1):
                        line_start = point
                elif placing == "zoom":
                    zoom_point = point
                    placing = ""
                save(True)
                if(line_start[0] == -1) and not vary:
                    last_point = (-1, -1)
                    points = []
    else:
        if event.type == pygame.KEYDOWN:
            if (getCharacter(event) != "NULL"):
                type_string += getCharacter(event)
        if(pygame.key.get_pressed()[pygame.K_BACKSPACE] != 0 and pygame.time.get_ticks() > last_press + 150):
            last_press = pygame.time.get_ticks()
            if (len(type_string) > 0):
                type_string = type_string[:len(type_string) - 1]
            elif (input_label == "attributes"):
                atts = []
                if (sprite1.polygons[poly_num][2] != None):
                    for a in sprite1.polygons[poly_num][2]:
                        if (a != sprite1.polygons[poly_num][2][len(sprite1.polygons[poly_num][2]) - 1]):
                            atts.append(a)
                sprite1.polygons[poly_num][2] = atts
        if(pygame.key.get_pressed()[pygame.K_RETURN] != 0 and pygame.time.get_ticks() > last_press + 150):
            last_press = pygame.time.get_ticks()
            execute_string(type_string)
            if not more_input:
                typing = False
                type_string = ""
                prompt = ""
                input_label = ""
    
    display.fill(color, ((margin / 2) - 2, (margin / 2) - 2, base_resolution[0] + 4, base_resolution[1] + 4))
    if (poly_num != -1):  # attributes
        polies = []
        polies.append(sprite1.polygons[poly_num])
        draw_from_file(True, polies)
        if (not delete):
            if sprite1.polygons[poly_num][2] != None and sprite1.polygons[poly_num][2] != []:
                display_text = "Attributes: "
                f = True
                for a in sprite1.polygons[poly_num][2]:
                    if (not f):
                        display_text += ", "
                    f = False
                    display_text += str(a[0]) + ": " + str(a[1])
            else:
                display_text = ""
            if (not typing):
                atts = []
                get_input("Attribute Name, Value: ", "attributes")
        else:
            if (not typing):
                get_input("Delete? ", "delete")
    elif not vary:
        draw_from_file(filled, sprite1.polygons)
    else:
        draw_from_file(filled, sprite_r.polygons)
        
    if (reflect):
        timer = pygame.time.get_ticks()
        if (timer > 1000 and int(str(timer)[-3]) % 2 == 0):
            pygame.draw.line(screen, (255, 0, 0), mirror[0], mirror[1], 1)
        else:
            pygame.draw.line(screen, (130, 38, 38), mirror[0], mirror[1], 1)
    
    rad = 1
    if (filled):
        rad = 0
    if (placing == "square"):
        pygame.draw.polygon(screen, color, square(point_shift()), rad)
    if (placing == "circle"):
        pygame.draw.polygon(screen, color, circle(point_shift()), rad)
    if (placing == "rect"):
        pygame.draw.polygon(screen, color, rect(point_shift()), rad)
    if placing == "line" and line_start[0] != -1:
        timer = pygame.time.get_ticks()
        if (line_angle > 180):
            angle = line_angle - 180
        elif (line_angle < 180):
            angle = line_angle + 180
        else:
            angle = 180
        end_point = point_pos(line_start, 15, angle)
        end_point = (int(end_point[0]), int(end_point[1]))
        if (timer > 1000 and int(str(timer)[-3]) % 2 == 0):
            pygame.draw.line(screen, (220, 15, 210), line_start, end_point, 1)
            pygame.draw.circle(screen, (220, 15, 210), line_start, 2)
        else:
            pygame.draw.line(screen, (177, 15, 170), line_start, end_point, 1)
            pygame.draw.circle(screen, (177, 15, 170), line_start, 2)
            
    timer = pygame.time.get_ticks()
    if zoom_level != 1:
        if (zoom_point[0] == -1):
            if (timer > 1000 and int(str(timer)[-3]) % 2 == 0):
                col = (14, 48, 238)
            else:
                col = (8, 31, 156)
            pygame.draw.rect(screen, col, (point_shift()[0] - (base_resolution[0] / zoom_level) / 2, point_shift()[1] - (base_resolution[1] / zoom_level) / 2, (base_resolution[0] / zoom_level), (base_resolution[1] / zoom_level)), 1)
        if (zoom_point[0] != -1):
            zoom_rect = (zoom_point[0] - (base_resolution[0] / zoom_level) / 2, zoom_point[1] - (base_resolution[1] / zoom_level) / 2, (base_resolution[0] / zoom_level), (base_resolution[1] / zoom_level))
            zoom_rect2 = []
            if zoom_rect[0] < 0:
                zoom_rect2.append(0)
            elif zoom_rect[0] > base_resolution[0] - (base_resolution[0] / zoom_level):
                zoom_rect2.append(base_resolution[0] - (base_resolution[0] / zoom_level))
            else:
                zoom_rect2.append(int(zoom_rect[0]))
            if zoom_rect[1] < 0:
                zoom_rect2.append(0)
            elif zoom_rect[1] > base_resolution[1] - (base_resolution[1] / zoom_level):
                zoom_rect2.append(base_resolution[1] - (base_resolution[1] / zoom_level))
            else:
                zoom_rect2.append(int(zoom_rect[1]))
            zoom_rect2.append(int(base_resolution[0] / zoom_level))
            zoom_rect2.append(int(base_resolution[1] / zoom_level))
            zoom_rect = zoom_rect2
            cropped_screen = crop(screen, zoom_rect)
            pygame.transform.scale(cropped_screen, (base_resolution[0], base_resolution[1]), screen)
    
    display.blit(screen, (int(margin / 2), int(margin / 2)))
    label = myfont.render((prompt + type_string), 1, (125, 255, 117))
    bprompt_color = (0, 0, 0)
    if (input_label == "color"):
        color_string = type_string.replace(" ", "").split(",")
        if type_string.replace(" ", "") == "":
            lcolor = last_color
        else:
            if (len(color_string) > 0 and is_int(color_string[0]) and int(color_string[0]) <= 255):
                r = int(color_string[0])
            else:
                r = 0
            if (len(color_string) > 1 and is_int(color_string[1]) and int(color_string[1]) <= 255):
                g = int(color_string[1])
            else:
                g = 0
            if (len(color_string) > 2 and is_int(color_string[2]) and int(color_string[2]) <= 255):
                b = int(color_string[2])
            else:
                b = 0
            lcolor = (r, g, b)
        label = myfont.render((prompt + type_string), 1, lcolor)
        if get_LUMA(lcolor) <= 50:
            bprompt_color = (125, 125, 125)
        display.fill(lcolor, (int(((base_resolution[0] + margin) / 2) - 10), base_resolution[1], 30, 20))

    
    if (vary):
        tools_text += " Variation " 
    if (placing != "" and placing != "zoom"):
        tools_text += " " + placing.title() + " "
    if (lock_points):
        tools_text += " Locked "
    if (restricted):
        tools_text += " Simple "
    if (filled):
        tools_text += " Filled "
    if (zoom_point[0] != -1):
        tools_text += " Zoom "
    if (reflect):
        tools_text += " Mirrored "
    
    
    display.fill((0, 0, 0), (0, base_resolution[1] + (margin / 2 + 2), base_resolution[0] + margin, margin / 2))
    display.fill(bprompt_color, (int(((base_resolution[0] + margin) / 2) - ((len(prompt + type_string) * 9) / 2)), base_resolution[0] + margin / 2 + 3, (len(prompt + type_string) * 9), 12))
    display.blit(label, (int(((base_resolution[0] + margin) / 2) - ((len(prompt + type_string) * 9) / 2)), base_resolution[1] + (margin / 2)))
    label = myfont.render((display_text), 1, (167, 212, 144))
    display.blit(label, (int(((base_resolution[0] + margin) / 2) - ((len(display_text) * 9) / 2)), base_resolution[1] + (margin / 2) + 18))
    label = myfont.render((tools_text), 1, (167, 212, 144))
    display.blit(label, (0, base_resolution[1] + (margin / 2) + 36))
    display.fill((0, 0, 0), (((base_resolution[0] + margin) - len(str(int(clock.get_fps()))) * 9) - 36, 0, (len(str(clock.get_fps())) * 9) + 72, 13))
    label = myfont.render((str(int(clock.get_fps()))), 1, (255, 255, 0))
    display.blit(label, ((base_resolution[0] + margin) - len(str(int(clock.get_fps()))) * 9, 0))
    pygame.display.update()
    clock.tick(70)
