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



