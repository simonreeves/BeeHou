# get the active pane when this is run via tab menu
# https://www.sidefx.com/docs/houdini/hom/tool_script.html#howto

import hou
import soptoolutils
import stateutils


def sibling_sop(kwargs):
    """
    creates an object merge SOP as a sibling as the source
    """
    # get pane (where tab menu called from)
    pane = stateutils.activePane(kwargs)

    if isinstance(pane, hou.NetworkEditor):
        # save selected node
        selected_nodes = hou.selectedNodes()

        for orig_node in selected_nodes:
            
            input_index = selected_nodes.index(orig_node)

            if input_index == 0:
                # use drop tool for first source
                objmerge = soptoolutils.genericTool(kwargs, 'object_merge')
                first_network_pos = objmerge.position()
            else:
                objmerge = orig_node.parent().createNode('object_merge', orig_node.name())
                
                # set position based on first placed node and index of loop
                additional_pos = hou.Vector2((input_index*2, 0.0))
                objmerge.setPosition(first_network_pos + additional_pos)
            
            objmerge.setName(orig_node.name().replace('OUT', 'IN'))
            # get relative path
            rel_path = objmerge.relativePathTo(orig_node)
            objmerge.parm('objpath1').set(rel_path)
            objmerge.parm('xformtype').set(1)

    else:
        hou.ui.setStatusMessage('Only works in network editor', severity=hou.severityType.Error)


def sibling_obj(kwargs):
    """
    creates a new object with an object merge SOP inside, so a sibling object
    """
    # save selected
    selected_nodes = hou.selectedNodes()
    
    # create object at same sibling hierarchy
    merged_geo_node = hou.selectedNodes()[0].parent().parent().createNode('geo', 'merged_geo')

    
    # create merge sop if more than 1 source nodes
    if len(selected_nodes) > 1:
        merge_sop = merged_geo_node.createNode('merge')
    else:
        merge_sop = None

    for orig_node in selected_nodes:
        objmerge = merged_geo_node.createNode('object_merge', orig_node.name())
        rel_path = objmerge.relativePathTo(orig_node)
        objmerge.parm('objpath1').set(rel_path)
        objmerge.parm('xformtype').set(1)
        
        if merge_sop:
            # lazy get last input index
            merge_sop.setInput(999, objmerge)
    
    # only auto layout if a new object was made
    merged_geo_node.layoutChildren()
