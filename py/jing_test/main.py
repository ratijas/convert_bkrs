"""jing test main program"""

from os import path
import subprocess
import sys

__all__ = ['JingTestError', 'run', 'main']


class JingTestError(subprocess.CalledProcessError):
    """this exception raised when jing test failed, e.g. returned non-zero.
       the exit status will be stored in the *returncode* attribute.
       the *output* attribute also will store the output.
    """

    def __init__(self, returncode, cmd, output):
        super(JingTestError, self).__init__(returncode, cmd, output)

    def __str__(self):
        return '`jing` test failed with exit status %d:\n%s\n%s' %\
            (self.returncode, '-' * 80, self.output)


def run(filename):
    """run(filename) --> None

    check file named *filename* whether it conforms to
    ``AppleDictionarySchema.rng``.

    returns None of success,
    raises ``JingTestError`` on error.
    """
    here = path.abspath(path.dirname(__file__))
    filename = path.abspath(filename)

    jing_jar_path = path.join(here, 'jing', 'bin', 'jing.jar')
    rng_path = path.join(here, 'DictionarySchema', 'AppleDictionarySchema.rng')
    # -Xmxn Specifies the maximum size, in bytes, of the memory allocation
    #       pool.
    # -- from `man java(1)`
    args = ['java', '-Xmx2G', '-jar', jing_jar_path, rng_path, filename]
    cmd = ' '.join(args)

    print 'running `jing` test:'
    print cmd
    print '...'

    pipe = subprocess.Popen(args,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)
    returncode = pipe.wait()
    output = pipe.communicate()[0]

    if returncode != 0:
        if returncode < 0:
            print >>sys.stderr, '`jing` was terminated by signal', -returncode
        elif returncode > 0:
            print >>sys.stderr, '`jing` returned', returncode
        raise JingTestError(returncode, cmd, output)
    else:
        print '`jing` test successfully passed!'


def main():
    """a command-line program that runs jing test on given dictionary xml
       file with apple dictionary schema.
    """
    if len(sys.argv) < 2:
        prog_name = path.basename(sys.argv[0])
        print >>sys.stderr, "usage:\n  %s filename" % prog_name
        exit(1)
    try:
        run(sys.argv[1])
    except JingTestError, e:
        print str(e)
        exit(e.returncode)
