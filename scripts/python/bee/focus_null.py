import hou

def main():
    nodes = hou.selectedNodes()

    for node in nodes:
        if node.type().name() != 'cam':
            continue

        # create null
        focus_null = node.parent().createNode('null', node.name() + '_focus')
        expression = "vlength(vtorigin('.', '{}'))".format(node.relativePathTo(focus_null))
        node.parm('focus').setExpression(expression)
        
        # set focus null visual properties
        focus_null.parm('shadedmode').set(1)
        focus_null.parm('controltype').set(2)
        focus_null.parm('geoscale').set(0.1)
        focus_null.parmTuple('dcolor').set((0,0.1,1))