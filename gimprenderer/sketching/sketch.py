'''
Created on Jun 5, 2015

@author: mucx
'''

from __future__ import division
import math
import random

import randomize
from geometry import LineSimple, LineString, Polygon

seed = 1

def add_points_to_line(line, n = 1, method = "equal"):
    """
    Note: The direction of the new line is always from min X to max X
    """
    
    line_new = []
    
    points_new = randomize.random_points_on_line(line, n, method)        
    
    line_new += [line[0]]
    line_new += points_new
    line_new += [line[1]]
    
    return line_new

def displace_line(line, r):
    """
    Displaces the two end points of a line. If the specified radius is
    larger than the line length, the points are displaced by half of the
    original line length.
    """
    
    line = LineSimple(line)
    
    a = line.coords[0]
    b = line.coords[1]
    
    length = line.length()
    
    if (length <= r):
        r =  length/2               
            
    random.seed(length + seed)
    point1 = randomize.displace_point(a, r, method = "circle")
    point2 = randomize.displace_point(b, r, method = "circle")
    
    line_new = [point1, point2]
    
    return line_new

def handy_hachures(hachures):
    
    hachures_handy = []
    hachures_displaced = []
    
    for hachure in hachures:
        
        hachure_displaced = displace_line(hachure, 3.0)
        hachures_displaced.append(hachure_displaced)
        
        hachure_handy = randomize.line_handy(hachure_displaced, 3.0)
        
        hachures_handy.append(hachure_handy)
        
        randomize.seed_loop += 1
        
    randomize.reset_seed_loop()
        
    return hachures_handy

def jitter_line(line, d = 10.0, method = "displace"):
    """
    Creates a jittered version of a Line (LineSimple or LineString) using 
    an absolute distortion value (in image units). Depending on the 
    distortion d, random points are added to the line segments (lines 
    connecting two points). After that, the line points are distorted 
    either using circular point displacement ("displace"), random Bezier 
    control points ("bezier") or both techniques ("displace_bezier").
    
    IMPORTANT: Do not forget to reset the randomize.seed_loop in the calling
    environment!
    
    :param line: List of coordinate pairs determining the line
    :param d: Jitter distortion of the line in absolute image units
    :param method: Method used for jittering ("displace", "bezier" or
    "displace_bezier")
    
    TO DO: Adding a relative_displacement d_rel?
    """
    
    line = LineString(line)
    
    line_points = []    
    line_points.append(line.coords[0]) # Adding the first point to result   
    
    # Iteration over all line segments  
    for i in range(0, len(line.coords) - 1):
        
        a = line.coords[i]
        b = line.coords[i + 1]
        
        line_seg = LineSimple([a,b])
        
        # Adding ceil(length/[10d|d^2])-1 points to the line segment
        seg_breaks = int(math.floor(line_seg.length() / (d * d))) - 1
                 
        if seg_breaks > 0:
            
            points = add_points_to_line(
                line_seg.coords, seg_breaks, "equal_beta"
            )
            
            # Check the direction of the segment and flip if necessary
            if points[0] == a:
                line_points += points[1:-1]
            else:
                line_points += reversed(points[1:-1])
                
        line_points.append(line.coords[i + 1]) # Adding segment end point
        
        randomize.seed_loop += 1
    
    line_jittered = randomize.jitter_linestring(line_points, d, method)
    
    return line_jittered

def jitter_polygon(polygon, d = 10.0, method = "displace"):
    
    polygon = Polygon(polygon)
    
    segments = polygon.disjoin(120)
    
    segments_jittered = []
    
    randomize.seed = 1
     
    for segment in segments:
        
        segment_jittered = jitter_line(segment, 10, "bezier")
        segments_jittered.append(segment_jittered)
        
        randomize.seed_loop += 1
        
    randomize.reset_seed_loop()
    
    return segments_jittered

################################################################################
# Interface functions

def path_to_linestring(path):
    
    coords = path.split(" ");   
    coords.remove('M')
    coords.remove('L')

    linestring = []
    
    for i in range(0, len(coords), 2):
        linestring.append(
            (float(coords[i]), float(coords[i + 1]))
        )
    
    return linestring
    
def path_to_polygon(path):
    
    polygons_str = path.split("Z");
    polygons_str.pop() # Removing last item from list (empty due to split)
    
    polygons = []
    
    for polygon_str in polygons_str:
        
        polygon_str = polygon_str.strip()
        
        polygon = path_to_linestring(polygon_str)
        polygons.append(polygon)
        
    return polygons