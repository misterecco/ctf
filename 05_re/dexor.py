# -*- coding: utf-8 -*-

from test import foo
import marshal

code = bytearray(open('task_jmp.pyc', 'rb').read())

main = code[0x679:0x753]


for (i, c) in enumerate(main):
    c = main[i] ^ 88
    main[i] = c

code[0x679:0x753] = main

new_file = open('task_clean.pyc', 'wb')

new_file.write(code) 