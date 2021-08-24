import hou


def main():
    """
    Called from a parm right click menu, gets the file's dir and runs redshiftTextureProcessor
    """

    # save selected
    selected_nodes = hou.selectedNodes()
    
    # create geo at same hierarchy
    merged_geo_node = hou.selectedNodes()[0].parent().createNode('geo', 'merged_geo')
    
    merge_sop = merged_geo_node.createNode('merge')

    for orig_node in selected_nodes:
        objmerge = merged_geo_node.createNode('object_merge', orig_node.name())
        rel_path = objmerge.relativePathTo(orig_node)
        objmerge.parm('objpath1').set(rel_path)
        objmerge.parm('xformtype').set(1)
        
        # lazy get last input index
        merge_sop.setInput(999, objmerge)
        
    merged_geo_node.layoutChildren()