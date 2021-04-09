import subprocess
import os
import hou


def main(kwargs):
    """
    called from a parm right click menu, gets file path to convert to rs tex
    """

    parms = kwargs.get('parms', False)

    # get first parm
    parm = parms[0]

    print('parm.eval(): {}'.format(parm.eval()))

    # get dir
    texfiles_dir = os.path.dirname(parm.eval())
    print('texfiles_dir: {}'.format(texfiles_dir))
    
    # check if path exists
    if not os.path.exists(texfiles_dir):
        print('could not find folder')
        return False

    # get redshift path from environ variables
    rs_tex_processor_path = hou.getenv('REDSHIFT_COREDATAPATH') + '/bin/redshiftTextureProcessor.exe'

    print('rs_tex_processor_path: {}'.format(rs_tex_processor_path))

    if not os.path.exists(rs_tex_processor_path):
        print('could not find rstex exe')
        return False

    args = [rs_tex_processor_path, texfiles_dir + '/*']
    
    # start subprocess
    subprocess.call(args)




