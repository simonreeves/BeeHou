import hou
import stateutils
import toolutils

def main(kwargs):
    """
    Creates a null to use as a focus gizmo for the selected camera(s)
    """

    # store reference to selected node
    selected_nodes = hou.selectedNodes()

    # Init to record if a camera was selected at all
    any_camera_selected = False

    # get network editor pane
    pane = stateutils.activePane(kwargs)

    if not isinstance(pane, hou.NetworkEditor):
        hou.ui.setStatusMessage('Only works in network editor', severity=hou.severityType.Error)
        return False
    
    for node in selected_nodes:
        if node.type().name() != 'cam':
            continue
        
        # A camera was found!
        any_camera_selected = True

        # create null      
        # toolutils not soptoolutils, because it's not a SOP
        focus_null = toolutils.genericTool(kwargs, 'null')
        focus_null.setName(node.name() + '_focus', True)
        
        # add focus distance expression
        expression = "vlength(vtorigin('.', '{}'))".format(node.relativePathTo(focus_null))
        node.parm('focus').setExpression(expression)
        
        # Lock rotation
        focus_null.parmTuple('r').lock(True)

        # set focus null visual properties
        focus_null.parm('shadedmode').set(1)
        focus_null.parm('controltype').set(2)
        focus_null.parm('geoscale').set(0.1)
        focus_null.parmTuple('dcolor').set((0, 0.1 ,1))

    if not any_camera_selected:
        message = "There were no cameras found in selection! Please select camera(s)"
        hou.ui.setStatusMessage(message=message, severity=hou.severityType.ImportantMessage)
        return