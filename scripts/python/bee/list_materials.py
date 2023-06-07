import hou

def main():
    for n in hou.selectedNodes():
    
        g = n.geometry()
        a = g.findPrimAttrib('shop_materialpath')
        
        materials = a.strings()
        
        for m in materials:
            print(m)