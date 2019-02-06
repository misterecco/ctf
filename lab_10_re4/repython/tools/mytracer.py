globs = dict(globals())
import sys
import types
import dis
def trace2(frame, event, arg):
    valid_opcodes = dis.opmap.values()
    tracefile = sys.stdout
    #print '>', frame.f_lasti, event
    if event == 'line':
        # Get the code object
        co_object = frame.f_code

        # Retrieve the name of the associated code object
        co_name = co_object.co_name

        if True: #options.name is None or co_name == options.name:
            # Get the code bytes
            co_bytes = co_object.co_code

            # f_lasti is the offset of the last bytecode instruction executed
            # w.r.t the current code object
            # For the very first instruction this is set to -1
            ins_offs = frame.f_lasti
            #print ins_offs
            if ins_offs >= 0:
                opcode = ord(co_bytes[ins_offs])

                # Check if it is a valid opcode
                if opcode in valid_opcodes:
                    if opcode >= dis.HAVE_ARGUMENT:
                        # Fetch the operand
                        operand = arg = ord(co_bytes[ins_offs+1]) | (ord(co_bytes[ins_offs+2]) << 8)

                        # Resolve instriction arguments if specified
                        if True:#options.resolve:
                            try:
                                if opcode in dis.hasconst:
                                    operand = co_object.co_consts[arg]
                                elif opcode in dis.hasname:
                                    operand = co_object.co_names[arg]
                                elif opcode in dis.haslocal:
                                    operand = co_object.co_varnames[arg]
                                elif opcode in dis.hascompare:
                                    operand = dis.cmp_op[arg]
                                elif opcode in dis.hasjabs:
                                    operand = arg
                                elif opcode in dis.hasjrel:
                                    operand = arg + ins_offs + 3
                                else:
                                    operand = arg
                            except:
                                operand = None

                        tracefile.write('{}> {} {} ({})\n'.format(co_name, ins_offs, dis.opname[opcode], operand))

                    # No operands
                    else:
                        tracefile.write('{}> {} {}\n'.format(co_name, ins_offs, dis.opname[opcode]))

                # Invalid opcode
                else:
                    tracefile.write('{}> {} {} **********INVALID**********\n'.format(co_name, ins_offs, opcode))

    return trace2

def fix_lines(code_obj):
    new_consts = []
    for c in code_obj.co_consts:
        if type(c) == types.CodeType:
            new_consts.append(fix_lines(c))
        else:
            new_consts.append(c)

    return types.CodeType(
        code_obj.co_argcount, code_obj.co_nlocals,
        code_obj.co_stacksize, code_obj.co_flags,
        code_obj.co_code,
        tuple(new_consts), code_obj.co_names, code_obj.co_varnames,
        code_obj.co_filename, code_obj.co_name, 0,
'\x01\x01' * (len(code_obj.co_code) - 1))


def run_traced(code_obj):
    code_obj = fix_lines(code_obj)
    f = types.FunctionType(code_obj, globs)    
    sys.settrace(trace2)
    f()

if __name__ == '__main__':
    import reader
    code_obj = reader.read(sys.argv[1])
    run_traced(code_obj)
    
