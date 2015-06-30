'''
Created on May 13, 2015

@author: mucx
'''

import svgwrite
import logging
from gimpfu import *
from abc import ABCMeta, abstractmethod

from gimpmaps.renderermap import MapRenderer
from tilerenderer import TileRenderer
from gimpmodule import GimpImageManager
from gimpmaps import sketchadapter

class RendererGimp(object):
    '''
    A renderer to create a single PNG map. An editable GIMP XCF file can be 
    created along with the PNG result.
    '''
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self):
        '''
        Constructor
        '''
        
        pass
    
    def draw_features_line(
            self, gimp, parent, line_styles, bbox, resolution
        ):
        """
        Drawing the line features as GIMP images and saving to PNG and/or XCF
        """
        
        try:
        
            self.conn_osm = self.connect_to_osm_db()
            
            # Creating layer groups for the feature type groups 
            group_line = gimp.create_layer_group(parent, -1)        
    
            for style_line in line_styles:
                            
                sql_selection = style_line.get_selection_tags()
                line_style = style_line.get_line_style()
                
                # Style settings
                # TO DO: emulate brush dynamics?????
                gimp.set_context(line_style)
                
                            
                logging.info("Querying database")
    
                # Import SVG data into SVG drawing from database
                svg_geoms = self.get_svg_features(
                    bbox,
                    resolution, 
                    style_line
                )
                
                            
                logging.info("Processing lines")
                
                for svg_commands in svg_geoms:
                    
                    line_sketched = sketchadapter.sketch_line_path(svg_commands)

                    # Adding vectors for stroking of lines, outlines/mask
                    gimp.vectors_import(line_sketched.tostring())
            
                # Creating image layer for geometry feature
                layer = gimp.create_layer(resolution, 
                                          sql_selection, group_line, 
                                          0)
                
                # Drawing vectors into GIMP layer
                
                logging.info("Drawing lines")
                
                gimp.vectors_draw(layer)
                
            self.conn_osm.close()
            
        except TypeError:
            print "No styles for this zoom level or type error"
        
    def draw_features_polygon(
            self, gimp, parent, polygon_styles, bbox, resolution, mask
        ):
        """
        Drawing the geometry features as GIMP images and saving to PNG and/or XCF
        """
        
        self.conn_osm = self.connect_to_osm_db()
        
        # Creating layer groups for the feature type groups       
        group_polygon = gimp.create_layer_group(parent, -1)

        for style_polygon in polygon_styles:
            
            try:
                
                sql_selection = style_polygon.get_selection_tags()
                line_style = style_polygon.get_line_style()
                hachure_style = style_polygon.get_hachure_style()
                
                # TO DO: Import from style and set in hachurizer
                spacing = 30
                angle = 30
                
                logging.info("Querying database")
                
                # Import SVG data into SVG drawing from database
                svg_geoms = self.get_svg_features(
                    bbox,
                    resolution, 
                    style_polygon
                )
                
                logging.info("Processing polygons")
                
                if mask:
                    
                    # Adding vectors for stroking of lines, outlines/mask
                    for svg_commands in svg_geoms:
                  
                        svg_path = svgwrite.path.Path(svg_commands)
                        svg_path_str = svg_path.tostring()
                        gimp.vectors_import(svg_path_str)
                        
                    # Adding background image to use the mask on
                    # TO DO: Get img path from style file
                    mask_image = "img/" + style_polygon.get_image_data()[0]
                    gimp.vectors_as_mask(
                        self, 
                        mask_image, group_polygon, resolution, sql_selection
                    )    
                
                else:
                    
                    group = gimp.create_layer_group(group_polygon, -1)
                
                    layer_fill = gimp.create_layer(resolution, 
                            sql_selection + "_fill", group, -1)
                
                    layer_hachure = gimp.create_layer(resolution, 
                            sql_selection + "_hachure", group, -1)
                    
                    layer_outline = gimp.create_layer(resolution, 
                            sql_selection + "_outline", group, -1)
                
                    for svg_commands in svg_geoms:                        
                        
                        logging.info("Processing fill")
                        
                        # Adding fill
                        path = svgwrite.path.Path(svg_commands)
                        gimp.vectors_import(path.tostring())
                        gimp.vectors_select()                                    
                        gimp.fill_selection(layer_fill, style_polygon.fill)
            
                        logging.info("Processing hachure")              
                        
                        # Getting and drawing the hachure lines
                        hachures = sketchadapter.sketch_polygon_hachure(
                                                                svg_commands)
                        if hachures is not None:
                             
                            for hachure in hachures:
                                 
                                if (hachure is not None):   
                                    
                                    logging.info("Drawing hachure")
                                                     
                                    gimp.vectors_import(hachure.tostring())
                                    gimp.set_context(hachure_style)
                                    gimp.vectors_draw(layer_hachure)
                                     
                                else:
                                    continue
                                
                        logging.info("Processing outline")
                               
                        # Getting and drawing the outline lines 
                        outlines = sketchadapter.sketch_polygon_outline(
                                                                svg_commands)                
                        
                        if outlines is not None:
                                     
                            for outline in outlines:
                                 
                                if (outline is not None):                            
                                    
                                    # Adding outline
                                    gimp.vectors_import(outline.tostring())                                    
                                    gimp.set_context(line_style)
                                    gimp.vectors_draw(layer_outline)
                                    
                                else:
                                    continue                        
            
            except TypeError:
                print "No styles for this zoom level or type error"
                logging.info("NOTE: No style for zoom level or type error!")
                
        self.conn_osm.close()
            
    def draw_text(
            self, gimp, parent, text_styles, bbox, resolution, 
            draw_outline, draw_buffer
        ):
        
        try:
        
            self.conn_osm = self.connect_to_osm_db()
            
            # Creating layer groups for the feature type groups       
            group_polygon_text = gimp.create_layer_group(parent, -1)
            
            for style_text in text_styles:             
                            
                # Import labels and coordinates from database
                text_points = self.get_text(
                    bbox,
                    resolution, 
                    style_text
                )         
                        
                gimp.draw_labels(
                    group_polygon_text, text_points, style_text,
                    resolution
                )
            
        except TypeError:
            print "No styles for this zoom level or type error"
                
       
class MapRendererGimp(MapRenderer, RendererGimp):
    '''
    A renderer to create a single PNG map. An editable GIMP XCF file can be 
    created along with the PNG result.
    '''
    
    def __init__(self, config_file):
        '''
        Constructor
        '''
        
        super(MapRendererGimp, self).__init__(config_file)
        
        self.type = "map_gimp"
        
    def draw(self, zoom, bbox, resolution, out_path):
               
        # Creating a GIMP Manager instance and an image
        gimp = GimpImageManager()
        gimp.image_create(resolution)
        
        # Resetting GIMP image context
        gimp.reset_context()
        
        # Creating a parent layer group for all the layer (groups) added later
        parent = gimp.create_layer_group(None, 0)
        
        # Background image
        bg_image = self.get_bg_img(zoom) 
        gimp.insert_image_tiled(resolution, bg_image, parent, -1)        
        
        # Drawing features
        feature_styles = self.get_feature_styles(zoom)
         
        ## Polygon features
        polygon_styles = feature_styles["polygons"]
        self.draw_features_polygon(
            gimp, parent, polygon_styles, bbox, resolution, False
        )
         
        ## Line features
        line_styles = feature_styles["lines"]
        self.draw_features_line(
            gimp, parent, line_styles, bbox, resolution
        )
       
        # Drawing the text
#         text_styles = self.get_text_styles(zoom)
#         polygon_text_styles = text_styles["polygons"]
#         self.draw_text(
#             gimp, parent, polygon_text_styles, bbox, resolution, True, False
#         )  
                      
        # Save images as PNG and XCF
        gimp.image_save(out_path, parent, True, self.create_xcf)
        
        gimp.image_close()
        
    
        
class TileRendererGimp(TileRenderer, RendererGimp):
    """
    This subclass of TileRenderer implements different 'setup' and
    'draw_features' methods for the creation of GIMP tiles as PNG and (if 
    defined in the 'create_xcf' variable) as XCF files as well.
    """
    
    def __init__(self, config_file):

        super(TileRendererGimp, self).__init__(config_file)
        
        self.type = "tiles_gimp"
        
    def draw(self, styles, bbox, resolution, out_path):   
        
        # Creating a GIMP Manager instance and an image
        gimp = GimpImageManager()
        gimp.image_create(resolution)
        
        # Resetting GIMP image context
        gimp.reset_context()
        
        # Creating a parent layer group for all the layer (groups) added later
        parent = gimp.create_layer_group(None, 0)
        
        # Background image
        bg_image = styles["background_img"]
        gimp.create_layer_image(parent, bg_image, -1)
        
        # Drawing polygon features
        self.draw_features_polygon(
            gimp, parent, styles["features"]["polygons"], bbox, resolution, False
        )  
        
        # Drawing line features
        self.draw_features_line(
            gimp, parent, styles["features"]["lines"], bbox, resolution
        )      
                      
        # Save images as PNG and XCF
        gimp.image_save(out_path, parent, True, self.create_xcf)
        
        gimp.image_close()