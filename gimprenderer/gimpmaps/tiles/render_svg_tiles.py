# -*- coding: utf-8 -*-

from gimpmaps.tiles import tilerenderersvg

zoom_min = 12
zoom_max = 12

zoom_levels = range(zoom_min,zoom_max+1) # last number is excluded

bbox_ul = [1275000, 6131500]
bbox_lr = [1289700, 6118200]

bbox = [bbox_ul, bbox_lr]

tile_size = 256

map_style = 1

# out_dir = os.getcwd() + "/results/"
out_dir = "../results/"

tile_renderer = tilerenderersvg.TileRendererSvg(
    bbox, 
    zoom_levels,
    tile_size,
    out_dir,
    map_style
)
tile_renderer.render_tiles()