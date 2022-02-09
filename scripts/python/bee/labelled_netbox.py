import hou


def main():
    # find parent node of current node.
    selected_nodes = hou.selectedNodes()  # type: tuple[hou.Node]
    current_nodes = [x for x in selected_nodes if x.isCurrent]  # type: List[hou.Node]
    if len(current_nodes) == 0:
        print("there are no selected node. please select some nodes")
        return
    parent = current_nodes[0].parent()  # type: hou.Node

    # create network boxes
    # parent_network_box = parent.createNetworkBox()  # type: hou.NetworkBox
    child_network_box = parent.createNetworkBox()  # type: hou.NetworkBox

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
    network_box_color = hou.Color(0.5,0.1,0.1)
    child_network_box.setColor(network_box_color)

    # create sticky_note
    sticky_note = parent.createStickyNote()
    
    sticky_note_position_x = child_network_box.position().x()
    sticky_note_position_y = child_network_box.size().y() + child_network_box.position().y()
    sticky_note_position = hou.Vector2(sticky_note_position_x, sticky_note_position_y)
    sticky_note.setPosition(sticky_note_position)
    
    if hou.isUIAvailable:
        label = hou.ui.readInput('Label')
    else:
        label = 'default'

    sticky_note.setText(label[1])
    sticky_note_height = 2
    sticky_note.setTextSize(sticky_note_height * .5)
    # min width to fit sticky note text
    sticky_note_width = max(child_network_box.size().x(), 4)

    sticky_note.setSize(hou.Vector2(sticky_note_width, sticky_note_height))

    # add after setting position
    child_network_box.addItem(sticky_note)
    
    sticky_note_text_color = hou.Color(214.0 / 255.0, 214.0 / 255.0, 214.0 / 255.0)
    sticky_note.setDrawBackground(False)
    sticky_note.setTextColor(sticky_note_text_color)

    return


