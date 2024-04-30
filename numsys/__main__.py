from numsys import *
import cmd

class CLI(cmd.Cmd):
    prompt = ''
    intro = 'Welcome toI. Type "help" for available commands.'

    def do_add(self, line: str):
        """Add two numbers."""

        args = line.split(' ')
        base = int(args[2])
        comp = Comp.NONE if len(args) < 4 else Comp[args[3].upper()]

        num1 = Number(args[0], base, comp)
        num2 = Number(args[1], base, comp)

        result = num1 + num2
        limit = max(len(result), len(num1), len(num2))
        carry = Number('0' * limit, base, comp)
        
        print('  ' + carry.__str__(limit))
        print('=' * (limit + 2))
        print('  ' + num1.__str__(limit))
        print('+ ' + num2.__str__(limit))
        print('=' * (limit + 2))
        print('  ' + result.__str__(limit))

        
    def do_base(self, line):
        """Set the base we're working in."""
        CLI.base = int(line)

    def do_convert(self, line: str):
        """"""

    def do_quit(self, line):
        """Exit the CLI."""
        return True

if __name__ == '__main__':

    CLI().cmdloop()