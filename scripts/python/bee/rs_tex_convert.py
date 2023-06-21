import subprocess
import os
import hou


def main(kwargs):
    """
    Called from a parm right click menu, gets the file's dir and runs redshiftTextureProcessor
    """

    parms = kwargs.get('parms', False)

    # get first parm
    parm = parms[0]

    # print('parm.eval(): {}'.format(parm.eval()))

    # get dir
    texfiles_dir = os.path.dirname(parm.eval())
    print('texfiles_dir: {}'.format(texfiles_dir))

    # check if path exists
    if not os.path.exists(texfiles_dir):
        print('Directory \"{}\" does not exist')
        return False


    # get redshift path from environ variables
    rs_tex_processor_path = hou.getenv('REDSHIFT_COREDATAPATH') + '/bin/redshiftTextureProcessor.exe'

    # print('rs_tex_processor_path: {}'.format(rs_tex_processor_path))

    if not os.path.exists(rs_tex_processor_path):
        print('BeeHou: Could not find redshiftTextureProcessor.exe')
        return False

    # build args
    args = [rs_tex_processor_path, texfiles_dir + '/*']
    
    # popen starts new process! call does not
    subprocess.Popen(args)


def make_topnet():
    """
    This is neat but not needed, also it creates topnets that cant delete themselves
    """

    # get redshift path from environ variables
    rs_tex_processor_path = hou.getenv('REDSHIFT_COREDATAPATH') + '/bin/redshiftTextureProcessor.exe'
    
    # create topnet and cook in background
    topnet = hou.node('/tasks').createNode('topnet', 'bee_rs_tex_convert')
    
    # tidy layout
    hou.node('/tasks').layoutChildren()

    # ignore errors to skip non convertable files which is fine
    topnet.children()[0].parm('local_echandleby').set(3)

    fp_node = topnet.createNode('filepattern')
    fp_node.parm('pattern').set(texfiles_dir + '/*')

    gg_node = fp_node.createOutputNode('genericgenerator')
    gg_node.parm('pdg_command').set('{} `pdgattribvals("directory")`/`pdgattribvals("filename")`'.format(rs_tex_processor_path))
    
    # tidy layout
    topnet.layoutChildren()

    # execute in background
    gg_node.executeGraph()

    # trying to delete the node after not suprising crashed

    # waitforall_node = gg_node.createOutputNode('waitforall')
    # pythonscript_node = waitforall_node.createOutputNode('pythonscript')
    # pythonscript_node.parm('script').set("print(self.topNode().destroy())")
    # pythonscript_node.executeGraph()
    # topnet.destroy()