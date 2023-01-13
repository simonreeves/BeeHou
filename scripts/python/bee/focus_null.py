import hou

def main():
    nodes = hou.selectedNodes()
    # Init to record if a camera was selected at all
    any_camera_selected = False

    for node in nodes:
        if node.type().name() != 'cam':
            continue
        
        # A camera was found!
        any_camera_selected = True

        # create null
        focus_null = node.parent().createNode('null', node.name() + '_focus')
        expression = "vlength(vtorigin('.', '{}'))".format(node.relativePathTo(focus_null))
        node.parm('focus').setExpression(expression)
        
        # set focus null visual properties
        focus_null.parm('shadedmode').set(1)
        focus_null.parm('controltype').set(2)
        focus_null.parm('geoscale').set(0.1)
        focus_null.parmTuple('dcolor').set((0, 0.1 ,1))

    if not any_camera_selected:
        message = "There were no cameras found in selection! Please select camera(s)"
        hou.ui.setStatusMessage(message=message, severity=hou.severityType.ImportantMessage)
        return