#!/usr/bin/env python
#encoding:utf-8

import commands

HELP = '''
 When your application crash with a segment fault, tell me where is your application,
 I will report which function caused this segment fault.

 Here is a demo for use:
\033[32m
    //segmentfault.c
    #include <stdlib.h>

    void logic_function(void) {
      char *ptr = 0x00;
      *ptr = 'A';
    }

    int main(int argc, const char *argv[]) {
      logic_function();
      return EXIT_SUCCESS;
    }

    [liangchengming@pandora segmentChecker]$ gcc segmentfault.c -o crash
    [liangchengming@pandora segmentChecker]$ ./crash
    segmentation fault
    [liangchengming@pandora segmentChecker]$ python %s ./crash
    Programme     : crash[29184]
    Operation     : user mode / write(0000000000000000) / NoPageFound
    Found Match   : [400458:    c6 00 41                movb   $0x41,(%%rax)]
    See Founction : <logic_function>
    [liangchengming@pandora segmentChecker]$
\033[0m

Usage:
    $python %s.py [name-of-your-binary-application]
'''%(__file__, __file__)



################################################################################
## perform dmesg and objdump
################################################################################
def dmesg_and_objdump(application):
    app_name = application.split('/')[-1][:15]
    error, output = commands.getstatusoutput("dmesg | tac")
    errmsg = None
    for line in output.split('\n'):
        if line.startswith(app_name):
            errmsg = line.strip()
            break
    error, dottxt_asm   = commands.getstatusoutput('objdump -d -S %s' % application)
    return errmsg, dottxt_asm.split('\n')


################################################################################
## change error for human read
################################################################################
def operation_at_cause_fault(error_code):
    errBytes = str(bin(int(error_code)))[2:]
    reason = {}
    reason['permit'] = errBytes[-1] == '1'
    reason['write']  = errBytes[-2] == '1'
    reason['user']   = errBytes[-3] == '1'
    return reason


################################################################################
## perform c++ name demangling
################################################################################
def demangling(mangled_name):
    _, demangled_name = commands.getstatusoutput('c++filt -i %s' % mangled_name)
    return demangled_name

################################################################################
## Add color for shell output
################################################################################
def polish(chars, color='auto'):
    if color == 'always':
        return '\033[32m%s\033[0m' % (chars)
    if color == 'auto':
        _os = __import__('os', fromlist=['isatty'])
        _sys = __import__('sys', fromlist=['stdout'])
        if _os.isatty(_sys.stdout.fileno()):
            return '\033[32m%s\033[0m' % (chars)
    #if color == 'none':
    return chars



################################################################################
## Add indent for human read
################################################################################
def readable(demangled_name, indent=0, tab = '    '):
    indented_name = []
    line = []
    level = 0
    for c in demangled_name:
        if c == ')':
            indented_name.append("%s%s" % (tab*level, ''.join(line)))
            level -= 1
            line = []
        if line or c != ' ':
            line.append(c)
        if c == ',' and level == 1:
            indented_name.append("%s%s" % (tab*level, ''.join(line)))
            line = []
            continue
        if c == '(':
            indented_name.append("%s%s" % (tab*level, ''.join(line)))
            line = []
            level += 1
            continue
        if c == '<':
            level += 1
            continue
        if c == '>':
            level -= 1
            continue
    indented_name.append("%s%s" % (tab*level, ''.join(line)))
    return '\n'.join(['%s%s'%(indent*' ', line) for line in indented_name])


################################################################################
## Search for BUG which caused segment fault, return the bug-container(function)
################################################################################
def locateError(errmsg, dotTxt):
    re = __import__('re', fromlist=['search'])
    match = re.search(r'(.+)\[(\d+)\]: segfault at ([\da-fA-F]+) rip '\
                      r'([\da-fA-F]+) rsp ([\da-fA-F]+) error (\d)', errmsg)

    if match:
        programme, pid, invalidAddr, source_code, _stack, error = match.groups()
        explain = operation_at_cause_fault(error)
        print "Programme          : %s[%s]\n"\
              "Operation          : %s"\
              % (
                programme,
                pid,
                polish('%s mode / %s(%s) / %s' % (
                    'user'  if explain['user']  else 'kernel',
                    'write' if explain['write'] else 'read',
                    invalidAddr,
                    'NoPermission'  if explain['permit']  else 'NoPageFound'
                    )),
              )
        page, offset = source_code[-6:-3], source_code[-3:]
        shortAdd = page+offset
        bugs = []
        for k in xrange(len(dotTxt)):
            if shortAdd in dotTxt[k]:
                print "Found Match        : [%s]" % dotTxt[k].strip().split('\t')[2]
                for dec in xrange(k, 0, -1):
                    if not dotTxt[dec].startswith(' '):
                        mangled_name = re.search(r'<(.*)>', dotTxt[dec][:-1]).group(0)
                        print "Mangled Founction  : %s" % mangled_name
                        print "Demangled Function : %s" % polish(
                                        readable(demangling(mangled_name[1:-1]))
                              )
                        return
    del re



################################################################################
## main
################################################################################
if __name__ == "__main__":

    sys = __import__('sys', fromlist=['argv'])
    if len(sys.argv) < 2:
        print HELP
        exit(-1)
    application = sys.argv[1]
    del sys

    errmsg, dotTxt  = dmesg_and_objdump(application)
    locateError(errmsg, dotTxt)


