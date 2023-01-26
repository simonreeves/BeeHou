import hou


def main():
    """
    Create a network box with a big label around the selected nodes, asks users for the label, picks a random colour
    """

    # find parent node of current node.
    selected_nodes = hou.selectedNodes()

    if len(selected_nodes) == 0:
        message = "There are no selected nodes, please select some nodes first"
        hou.ui.setStatusMessage(message=message, severity=hou.severityType.ImportantMessage)
        return
    
    # Ask user for label, first looks tidier in network viewer
    label = hou.ui.readInput('Label')

    # get parent of first selected node
    parent = selected_nodes[0].parent()

    # create network box
    child_network_box = parent.createNetworkBox()

    # find good position of boxes, which is center of selected nodes.
    list_x_of_selected_nodes = [node.position().x() for node in selected_nodes]
    center_x = sum(list_x_of_selected_nodes) / len(selected_nodes)
    list_y_of_selected_nodes = [node.position().y() for node in selected_nodes]
    center_y = sum(list_y_of_selected_nodes) / len(selected_nodes)
    child_network_box.setPosition(hou.Vector2(center_x, center_y))

    # add selected nodes to box. and resize box.
    for selected_node in selected_nodes:
        child_network_box.addItem(selected_node)
        child_network_box.fitAroundContents()

    # set color of network boxes
    # create a hou.Colour
    network_box_color = hou.Color()
    
    # create random hue using x position (whynot)
    hue = hou.hmath.rand(center_x) * 360

    # set its HSV
    network_box_color.setHSL((hue, 0.5, 0.4),)
    child_network_box.setColor(network_box_color)

    # create sticky_note
    sticky_note = parent.createStickyNote()
    
    sticky_note_position_x = child_network_box.position().x()
    sticky_note_position_y = child_network_box.size().y() + child_network_box.position().y()
    sticky_note_position = hou.Vector2(sticky_note_position_x, sticky_note_position_y)
    sticky_note.setPosition(sticky_note_position)
    
    sticky_note.setText(label[1])
    sticky_note_height = 2
    sticky_note.setTextSize(sticky_note_height * .5)

    # min width to fit sticky note text
    sticky_note_width = max(child_network_box.size().x(), 4)
    sticky_note.setSize(hou.Vector2(sticky_note_width, sticky_note_height))

    # add after setting position
    child_network_box.addItem(sticky_note)
    sticky_note.setDrawBackground(False)

    return


