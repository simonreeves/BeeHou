import hou

def main(kwargs):
    node = kwargs.get('node', False)
    add_loop_parms(node)


def add_loop_parms(node):
    """
    relies on manual creation of adding spare param and linking foreach meta node
    adds useful parms to access iteration of foreach loop
    """
    
    n = node

    # get existing list of parameters for the given node
    parm_template = n.parmTemplateGroup()

    # check if loop tools already exists
    if parm_template.find('loop_tools'):
        return
    
    # create parm list
    parms = []
    
    # add a parm to the list
    parms.append(hou.FloatParmTemplate(
        name="iteration",
        label="iteration",
        num_components=1,
        default_expression=("detail(-1, 'iteration', 0)",),
        )
    )

    parms.append(hou.FloatParmTemplate(
        name="iteration_rand",
        label="iteration rand",
        num_components=1,
        default_expression=("rand(ch('iteration')+ch('rand_seed'))",),
        )
    )

    parms.append(hou.FloatParmTemplate(
        name="rand_seed",
        label="rand_seed",
        num_components=1,
        )
    )

    # create folder with with parms
    parmfolder = hou.FolderParmTemplate(
        "loop_tools",
        "Loop Tools",
        folder_type=hou.folderType.Simple,
        parm_templates=parms
    )

    # append the folder
    parm_template.append(parmfolder)

    # apply changes
    n.setParmTemplateGroup(parm_template)