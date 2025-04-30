import copy
import opsc
import oobb
import oobb_base
import yaml
import os
import scad_help

def main(**kwargs):
    make_scad(**kwargs)

def make_scad(**kwargs):
    parts = []

    typ = kwargs.get("typ", "")

    if typ == "":
        #setup    
        #typ = "all"
        typ = "fast"
        #typ = "manual"

    #oomp_mode = "project"
    oomp_mode = "oobb"

    test = False
    #test = True

    if typ == "all":
        filter = ""; save_type = "all"; navigation = True; overwrite = True; modes = ["3dpr"]; oomp_run = False; test = False
        #default
        #filter = ""; save_type = "all"; navigation = True; overwrite = True; modes = ["3dpr"]; oomp_run = True; test = False
    elif typ == "fast":        
        filter = ""; save_type = "none"; navigation = True; overwrite = True; modes = ["3dpr"]; oomp_run = False
        #default
        #filter = ""; save_type = "none"; navigation = False; overwrite = True; modes = ["3dpr"]; oomp_run = False
    elif typ == "manual":
    #filter
        filter = ""
        #filter = "test"

    #save_type
        save_type = "none"
        #save_type = "all"
        
    #navigation        
        #navigation = False
        navigation = True    

    #overwrite
        overwrite = True
                
    #modes
        #modes = ["3dpr", "laser", "true"]
        modes = ["3dpr"]
        #modes = ["laser"]    

    #oomp_run
        oomp_run = True
        #oomp_run = False    

    #adding to kwargs
    kwargs["filter"] = filter
    kwargs["save_type"] = save_type
    kwargs["navigation"] = navigation
    kwargs["overwrite"] = overwrite
    kwargs["modes"] = modes
    kwargs["oomp_mode"] = oomp_mode
    kwargs["oomp_run"] = oomp_run
    
       
    # project_variables
    if True:
        pass
    
    # declare parts
    if True:

        directory_name = os.path.dirname(__file__) 
        directory_name = directory_name.replace("/", "\\")
        project_name = directory_name.split("\\")[-1]
        #max 60 characters
        length_max = 40
        if len(project_name) > length_max:
            project_name = project_name[:length_max]
            #if ends with a _ remove it 
            if project_name[-1] == "_":
                project_name = project_name[:-1]
                
        #defaults
        kwargs["size"] = "oobb"
        kwargs["width"] = 1
        kwargs["height"] = 1
        kwargs["thickness"] = 3
        #oomp_bits
        if oomp_mode == "project":
            kwargs["oomp_classification"] = "project"
            kwargs["oomp_type"] = "github"
            kwargs["oomp_size"] = "oomlout"
            kwargs["oomp_color"] = project_name
            kwargs["oomp_description_main"] = ""
            kwargs["oomp_description_extra"] = ""
            kwargs["oomp_manufacturer"] = ""
            kwargs["oomp_part_number"] = ""
        elif oomp_mode == "oobb":
            kwargs["oomp_classification"] = "oobb"
            kwargs["oomp_type"] = "part"
            kwargs["oomp_size"] = ""
            kwargs["oomp_color"] = ""
            kwargs["oomp_description_main"] = ""
            kwargs["oomp_description_extra"] = ""
            kwargs["oomp_manufacturer"] = ""
            kwargs["oomp_part_number"] = ""

        part_default = {} 
       
        part_default["project_name"] = project_name
        part_default["full_shift"] = [0, 0, 0]
        part_default["full_rotations"] = [0, 0, 0]
        

        widths = [3,5,7,13]

        letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789".lower()   
        #letters = "AIYU".lower()
        #convert letters to an array
        letters = list(letters)
        #letters = []
        letters.append("xs")     
        letters.append("xl")     
        letters.append("xxl")
        letters.append("xxxl")
        

        styles = ["top", "bottom"]  

        thicknesses = [1, 3, 6]
        #thicknesses = [1]
        for wid in widths:
            for letter in letters:
                for style in styles:
                    for thick in thicknesses:
                        part = copy.deepcopy(part_default)
                        p3 = copy.deepcopy(kwargs)
                        p3["width"] = wid
                        #p3["height"] = 3
                        p3["thickness"] = thick
                        
                        p3["letter"] = letter
                        p3["style"] = style
                        p3["extra"] = f"{style}_style_{letter}_letter"
                        part["kwargs"] = p3
                        nam = "alphabet"
                        part["name"] = nam
                        if oomp_mode == "oobb":
                            p3["oomp_size"] = nam
                        if not test:
                            pass
                            parts.append(part)


    kwargs["parts"] = parts

    scad_help.make_parts(**kwargs)

    #generate navigation
    if navigation:
        sort = []
        #sort.append("extra")
        sort.append("name")
        sort.append("width")
        sort.append("letter")
        sort.append("style")
        sort.append("thickness")
        
        scad_help.generate_navigation(sort = sort)


def get_base(thing, **kwargs):

    prepare_print = kwargs.get("prepare_print", False)
    thickness = kwargs.get("thickness", 3)
    width = kwargs.get("width", 7)    
    th = thing["components"]
    extra = kwargs.get("extra", "")
    letter = kwargs.get("letter", "")
    style = kwargs.get("style", "")

    width_working = width - 2
    text_length = len(letter)
    text_size = width_working * 95/5 / text_length

    # plate
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "p"
    p3["shape"] = "oobb_plate"
    p3["depth"] = thickness
    oobb_base.append_full(thing, **p3)
    
    # holes
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "n"
    p3["shape"] = "oobb_holes"
    p3["height"] = 1
    p3["holes"] = ["all"]
    p3["both_holes"] = True
    p3["m"] = "#"
    oobb_base.append_full(thing, **p3)
    # find the start point needs to be half the width_mm plus half oobb_basegv("osp")
    

    if style == "top":
        shift_y = 0
        if width == 3:
            shift_y = -5
        if width == 5:
            shift_y = -5
    elif style == "bottom":
        shift_y = 0
        if width == 3:
            shift_y = width * 8 / (text_length *.80)
        if width == 5:
            shift_y = width * 11 / (text_length * .9)
        if width == 7:
            shift_y = width * 13 / text_length
        if width == 13:
            shift_y = width * 14 / text_length
    

    p2 = copy.deepcopy(kwargs)
    p2["type"] = "p"
    p2["shape"] = "text"
    p2["text"] = letter.upper()
    p2["size"] = text_size
    p2["pos"] = [0,shift_y,0]
    p2["height"] = thickness
    p2["valign"] = "top"
    p2["halign"] = "center"
    p2["font"] = "DejaVu Sans Mono:style=Bold"
    thinga = oobb_base.oe(**p2)
    th.append(thinga)

    

    if prepare_print:
        #put into a rotation object
        components_second = copy.deepcopy(thing["components"])
        return_value_2 = {}
        return_value_2["type"]  = "rotation"
        return_value_2["typetype"]  = "p"
        pos1 = copy.deepcopy(pos)
        pos1[0] += 50
        return_value_2["pos"] = pos1
        return_value_2["rot"] = [180,0,0]
        return_value_2["objects"] = components_second
        
        thing["components"].append(return_value_2)

    
        #add slice # top
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "n"
        p3["shape"] = f"oobb_slice"
        pos1 = copy.deepcopy(pos)
        pos1[0] += -500/2
        pos1[1] += 0
        pos1[2] += -500/2        
        p3["pos"] = pos1
        #p3["m"] = "#"
        oobb_base.append_full(thing,**p3)


def get_bunting_alphabet(**kwargs):
   
    thickness = kwargs.get("thickness", 3)
    width = kwargs.get("width", 7)
    thing = oobb_base.get_default_thing(**kwargs)    
    th = thing["components"]
    extra = kwargs.get("extra", "")

    width_working = width - 2
    text_size = width_working * 95/5

    # plate
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "p"
    p3["shape"] = "oobb_plate"
    p3["depth"] = thickness
    oobb_base.append_full(thing, **p3)
    
    # holes
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "n"
    p3["shape"] = "oobb_holes"
    p3["height"] = 1
    p3["holes"] = ["all"]
    p3["both_holes"] = True
    p3["m"] = "#"
    oobb_base.append_full(thing, **p3)
    # find the start point needs to be half the width_mm plus half oobb_basegv("osp")
    


    shift_y = 0
    if width == 3:
        shift_y = -5
    if width == 5:
        shift_y = -5

    p2 = copy.deepcopy(kwargs)
    p2["type"] = "p"
    p2["shape"] = "text"
    p2["text"] = extra.upper()
    p2["size"] = text_size
    p2["pos"] = [0,shift_y,0]
    p2["height"] = thickness
    p2["valign"] = "top"
    p2["halign"] = "center"
    p2["font"] = "DejaVu Sans Mono:style=Bold"
    thinga = oobb_base.oe(**p2)
    th.append(thinga)


    return thing 

if __name__ == '__main__':
    kwargs = {}
    main(**kwargs)