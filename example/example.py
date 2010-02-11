'''A sample application for cmd2.'''

from cmd2 import Cmd, make_option, options, Cmd2TestCase, run
import unittest, optparse, sys

class CmdLineApp(Cmd):
    multilineCommands = ['orate']
    Cmd.shortcuts.update({'&': 'speak'})
    maxrepeats = 3
    Cmd.settable.append('maxrepeats   Max number of `--repeat`s allowed')

    @options([make_option('-p', '--piglatin', action="store_true", help="atinLay"),
              make_option('-s', '--shout', action="store_true", help="N00B EMULATION MODE"),
              make_option('-r', '--repeat', type="int", help="output [n] times")
             ])
    def do_speak(self, arg, opts=None):
        """Repeats what you tell me to."""
        arg = ''.join(arg)
        if opts.piglatin:
            arg = '%s%say' % (arg[1:].rstrip(), arg[0])
        if opts.shout:
            arg = arg.upper()
        repetitions = opts.repeat or 1
        for i in range(min(repetitions, self.maxrepeats)):
            self.stdout.write(arg)
            self.stdout.write('\n')
            # self.stdout.write is better than "print", because Cmd can be
            # initialized with a non-standard output destination        

    do_say = do_speak     # now "say" is a synonym for "speak"
    do_orate = do_speak   # another synonym, but this one takes multi-line input

c = CmdLineApp()
#run(c)

class TestMyAppCase(Cmd2TestCase):
    CmdApp = CmdLineApp
parser = optparse.OptionParser()
parser.add_option('-t', '--test', dest='test', action="store_true", 
                  help='Test against transcript(s) in FILE (wildcards OK)')
(callopts, callargs) = parser.parse_args()
if callopts.test:
    CmdLineApp.testfiles = callargs
    sys.argv = [sys.argv[0]] # the --test argument upsets unittest.main()
    unittest.main()
else:
    CmdLineApp().cmdloop()
