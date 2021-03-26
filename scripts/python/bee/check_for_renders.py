import glob
import hou


def main():
    """
    checks all the ROPs in the OUT context to see if their output paths already exist
    """

    rops_output_parms = {
        'Redshift': 'RS_outputFileNamePrefix',
        'OpenGL': 'picture',
        'Mantra': 'vm_picture',
    }

    # init list
    existing_renders = []

    # loop through all (rescursively) nodes in OUT
    out_nodes = hou.node('/out').children()

    for node in out_nodes:
        output_parm = rops_output_parms.get(node.type().description())

        # if ROP is not supported, skip it
        if not output_parm:
            continue

        # eval at frame to get predictable result
        output_filepath = node.parm(output_parm).evalAtFrame(1001)

        # use glob to search the folder with wildcard
        existing_files = glob.glob(output_filepath.replace('1001', '*'))

        # add node path to the list ready to print later
        if existing_files:
            existing_renders.append(node.path())

    # if any were found
    if existing_renders:
        if hou.isUIAvailable():
            message = 'Renders already exist for \"{}\" you should version up'.format(', '.join(existing_renders))
            hou.ui.setStatusMessage(message=message, severity=hou.severityType.ImportantMessage)
    else:
        if hou.isUIAvailable():
            message = 'No renders found'
            hou.ui.setStatusMessage(message=message, severity=hou.severityType.Message)

