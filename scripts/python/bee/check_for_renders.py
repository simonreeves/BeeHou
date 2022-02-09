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

        # replace frame with wildcard
        glob_path = output_filepath.replace('1001', '*')

        # for redshift need to check for %AOV% too
        glob_path = glob_path.replace('_%AOV%', '*')

        # use glob to search the folder with wildcard
        existing_files = glob.glob(glob_path)

        # add node path to the list ready to print later
        if existing_files:
            existing_renders.append(node.path())

    # if any were found
    if hou.isUIAvailable():
        if existing_renders:
            message = 'Renders already exist for \"{}\" consider versioning up'.format(', '.join(existing_renders))
            hou.ui.setStatusMessage(message=message, severity=hou.severityType.ImportantMessage)
        else:
            message = 'No renders found'
            hou.ui.setStatusMessage(message=message, severity=hou.severityType.Message)

