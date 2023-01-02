import re
from collections import defaultdict as multimap, deque
from functools import reduce
from math import inf
from copy import deepcopy
TERMINAL = 'terminal'
NONTERMINAL = 'nonterminal'
ASSIGNMENT = 'assignment'
EMPTY = 'empty string'
grammar = multimap(set)
PARTS = {
    r'"[^"]*"': TERMINAL,
    r'<[^">]+>': NONTERMINAL,
    '::=': ASSIGNMENT,
    'e': EMPTY,
}
start = None
with open('work.txt', 'r', encoding='ANSI') as file:
    first = True
    for s in file:
        s = s[:-1]
        print(s)
        values = []
        while s:
            m = inf
            end = inf
            k = ''
            for part in PARTS:
                ans = re.search(part, s)
                if ans and ans.start() < m:
                    k = part
                    m = ans.start()
                    end = ans.end()
            try:
                values.append((s[m:end],PARTS[k]))
            except TypeError:
                raise TypeError('Incorrect Input')
            s = s[end:]
        grammar[values[0][0]].add((*values[2:],))
        if first:
            start = values[0][0]
            first = False
print(grammar)
FIRST = {k: set() for k in grammar}
FOLLOW = {k: set() for k in grammar}
def FIRST_(G, F, arg, *args):
    if arg[1] in (TERMINAL, EMPTY):
        return {arg[0]}
    res = set()
    if 'e' in F[arg[0]]:
        res |= (F[arg[0]]-{'e'}) | (FIRST_(G, F, *args) if len(args) else {'e'})
    else:
        res |= F[arg[0]]
    return res
changed = True
while changed:
    changed = False
    old = deepcopy(FIRST)
    for A in grammar:
        for seq in grammar[A]:
            FIRST[A] |= FIRST_(grammar, FIRST, *seq)
    changed = old != FIRST
print('FIRST')
print(*(f'{k}:{FIRST[k]}' for k in FIRST), sep='\n')
FOLLOW[start] |= {"$"}
changed = True
while changed:
    changed = False
    old = deepcopy(FOLLOW)
    for A in grammar:
        for seq in grammar[A]:
            for i in range(len(seq)):
                if seq[i][1] == NONTERMINAL:
                    subres = set()
                    for j in range(i+1, len(seq)):
                        if seq[j][1] == TERMINAL:
                            subres.add(seq[j][0])
                            break
                        subres |= (FIRST[seq[j][0]] - {'e'})
                        if 'e' not in FIRST[seq[j][0]]:
                            break
                    if i == len(seq)-1 or 'e' in FIRST_(grammar, FIRST, *seq[i+1:]):
                        subres |= FOLLOW[A]
                    FOLLOW[seq[i][0]] |= subres
    changed = old != FOLLOW
print('FOLLOW')
print(*(f'{k}:{FOLLOW[k]}' for k in FOLLOW), sep='\n')
M = {}
for A in grammar:
    M[A] = {}
    for seq in grammar[A]:
        tmp = FIRST_(grammar,FIRST,*seq)
        for a in FIRST_(grammar,FIRST,*seq)-{'e'}:
            M[A][a] = [A, '::=', *(map(lambda x: str(x[0]), seq))]
        if 'e' in tmp:
            for b in FOLLOW[A]:
                M[A][b] = [A, '::=', *(map(lambda x: str(x[0]), seq))]
for k in M:
    print(f'{k}:', *(f'{i}:{"".join(M[k][i])}' for i in M[k]),sep='\t')
with open('out.py', 'w') as f:
    f.write('from collections import deque\n')
    f.write(
        'TERMINALS = ' +
        ','.join(
            map(
                lambda x: "'"+x+"'",
                reduce(
                    lambda x, y: x | y,
                    ({k for k in M[nt]} for nt in M)
                )
            )
        )
    )
    f.write('''
stack = deque()
tokens = deque()
line=input()+'$'
while len(line) != 0:
\tfor terminal in TERMINALS:
\t\tif line.startswith(terminal):
\t\t\ttokens.append(terminal)
\t\t\tline = line[len(terminal):]
stack.append('$')
''')
    f.write(f'stack.append("{start}")')
    f.write('''
while len(stack) or len(tokens):
\tx, y = stack.pop(), tokens[0]
\tprint(f'{x=}\\t{"".join(tokens)}')
\tmatch x, y:
\t\tcase x, y if x == y:
\t\t\ttokens.popleft()    
''')
    for A in M:
        for a in M[A]:
            A_ = A.replace(r"'",r"\'")
            f.write(f'\t\tcase \'{A_}\',\'{a}\':\n')
            if M[A][a][-1] != 'e':
                for el in M[A][a][:1:-1]:
                    el_ = el.replace(r"'",r"\'")
                    f.write(f'\t\t\tstack.append(\'{el_}\')\n')
            s ="".join(M[A][a]).replace(r"'", r"\'")
            f.write("\t\t\tprint('"+s+"')\n")
    f.write('''\t\tcase x, y:
\t\t\tprint('Error')
\t\t\tbreak
''')
symbols = set()
for k in M:
    symbols |= M[k].keys()
symbols = [*symbols]
print('####################')
print('',*symbols, sep='\t')
for A in M:
    print(A, *(("".join(M[A][a]) if a in M[A] else '') for a in symbols),sep='\t')