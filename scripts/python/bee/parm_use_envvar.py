import os
import hou


def main(kwargs):
    """
    look for a environment variable that matches something in the path
    """

    parms = kwargs.get('parms', False)

    # get first parm
    parm = parms[0]
    
    # check job first
    job_env = os.environ.get('JOB', False)
    
    if job_env:
        
        if job_env in parm.eval():
            n = parm.eval().replace(job_env, '$JOB')
            parm.set(n)
            return

    for k, v in os.environ.items():
        if v in parm.eval():
            n = parm.eval().replace(v, '${}'.format(k))
            parm.set(n)
            break