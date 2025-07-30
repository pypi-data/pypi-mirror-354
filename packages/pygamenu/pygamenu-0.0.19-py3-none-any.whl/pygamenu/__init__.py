from .mainn import View, initialize
STYLES = {
    "position":{"types":['text'], "default":"relative", "accepted":["relative","absolute","block"]},
    "height":{"types":['number', 'percentage'], "default":0,"max":"parentheight"},
    "width":{"types":['number', 'percentage'], "default":0,"max":"parentwidth"},
    "top":{"types":['number', 'percentage'], "default":0,"max":"parentheight"},
    "left":{"types":['number', 'percentage'], "default":0,"max":"parentwidth"},
    "rotation":{"types":['number'], "default":0},
    "background":{"types":['rgbvalue'], "default":None},
    "opacity":{"types":['number', 'percentage'], "default":255, "max":255},
    "corner-radius":{"types":['number'], "default":0},
    "border-width":{"types":['number'], "default":0},
    "border-color":{"types":['rgbvalue'], "default":None},
    "font":{"types":['text'],"default":"verdana", "accepted":[]},
    "font-color":{"types":['rgbvalue'],'default':(255,255,255)},
    "font-size":{"types":['number'],"default":10},
    "cx": {"types":['number','percentage'], "default":0, "max":"parentwidth"},
    "cy": {"types":['number','percentage'], "default":0, "max":"parentheight"},
}
# I will selectively import stuff that the user needs and make sure to not give the user system functions
