from collections import deque
TERMINALS = "letters""numbers""loop""OR""AND""WHERE""INTERSECT""UNION""("")""[""]"",""$"
stack = deque()
tokens = deque()
line=input()+'$'
while len(line) != 0:
   for terminal in TERMINALS:
      if line.startswith(terminal):
         tokens.append(terminal)
         line = line[len(terminal):]
stack.append('$')
stack.append("<оператор_РА>")
while len(stack) or len(tokens):
   x, y = stack.pop(), tokens[0]
   print(f'{x=}\t{"".join(tokens)}')
   match x, y:
      case x, y if x == y:
         tokens.popleft()    
      case '<оператор_РА>','"("':
         stack.append('<якась_таблиця>')
         print('<оператор_РА>::=<якась_таблиця>')
      case '<оператор_РА>','"letters"':
         stack.append('<якась_таблиця>')
         print('<оператор_РА>::=<якась_таблиця>')
      case '<якась_таблиця>','"("':
         stack.append('<якась_таблиця\'>')
         stack.append('<Запит>')
         print('<якась_таблиця>::=<Запит><якась_таблиця\'>')
      case '<якась_таблиця>','"letters"':
         stack.append('<якась_таблиця\'>')
         stack.append('<Запит>')
         print('<якась_таблиця>::=<Запит><якась_таблиця\'>')
      case '<якась_таблиця\'>','"INTERSECT"':
         stack.append('<якась_таблиця\'>')
         stack.append('<Запит>')
         stack.append('"INTERSECT"')
         print('<якась_таблиця\'>::="INTERSECT"<Запит><якась_таблиця\'>')
      case '<якась_таблиця\'>','")"':
         print('<якась_таблиця\'>::=AND')
      case '<якась_таблиця\'>','$':
         print('<якась_таблиця\'>::=AND')
      case '<Запит>','"("':
         stack.append('")"')
         stack.append('<якась_таблиця>')
         stack.append('"("')
         print('<Запит>::="("<якась_таблиця>")"')
      case '<Запит>','"letters"':
         stack.append('<оператор_об’єднання>')
         stack.append('"letters"')
         print('<Запит>::="letters"<оператор_об’єднання>')
      case '<оператор_об’єднання>','$':
         print('<оператор_об’єднання>::=AND')
      case '<оператор_об’єднання>','"INTERSECT"':
         print('<оператор_об’єднання>::=AND')
      case '<оператор_об’єднання>','")"':
         print('<оператор_об’єднання>::=AND')
      case '<оператор_об’єднання>','"WHERE"':
         stack.append('<список_умов>')
         stack.append('"WHERE"')
         print('<оператор_об’єднання>::="WHERE"<список_умов>')
      case '<список_умов>','"loop"':
         stack.append('<список_умов\'>')
         stack.append('<умова>')
         print('<список_умов>::=<умова><список_умов\'>')
      case '<список_умов>','"OR"':
         stack.append('<список_умов\'>')
         stack.append('<умова>')
         print('<список_умов>::=<умова><список_умов\'>')
      case '<список_умов>','"UNION"':
         stack.append('<список_умов\'>')
         stack.append('<умова>')
         print('<список_умов>::=<умова><список_умов\'>')
      case '<список_умов>','"numbers"':
         stack.append('<список_умов\'>')
         stack.append('<умова>')
         print('<список_умов>::=<умова><список_умов\'>')
      case '<список_умов\'>','$':
         print('<список_умов\'>::=AND')
      case '<список_умов\'>','"INTERSECT"':
         print('<список_умов\'>::=AND')
      case '<список_умов\'>','")"':
         print('<список_умов\'>::=AND')
      case '<список_умов\'>','"["':
         stack.append('<список_умов\'>')
         stack.append('<умова>')
         stack.append('"["')
         print('<список_умов\'>::="["<умова><список_умов\'>')
      case '<умова>','"loop"':
         stack.append('<умова\'>')
         print('<умова>::=<умова\'>')
      case '<умова>','"UNION"':
         stack.append('<умова\'>')
         print('<умова>::=<умова\'>')
      case '<умова>','"numbers"':
         stack.append('<умова\'>')
         print('<умова>::=<умова\'>')
      case '<умова>','"OR"':
         stack.append('<умова\'>')
         stack.append('"OR"')
         print('<умова>::="OR"<умова\'>')
      case '<умова\'>','"loop"':
         stack.append('<значення\'>')
         stack.append('<значення>')
         print('<умова\'>::=<значення><значення\'>')
      case '<умова\'>','"UNION"':
         stack.append('<значення\'>')
         stack.append('<значення>')
         print('<умова\'>::=<значення><значення\'>')
      case '<умова\'>','"numbers"':
         stack.append('<значення\'>')
         stack.append('<значення>')
         print('<умова\'>::=<значення><значення\'>')
      case '<значення\'>','"]"':
         stack.append('<значення>')
         stack.append('"]"')
         print('<значення\'>::="]"<значення>')
      case '<значення>','"UNION"':
         stack.append('"UNION"')
         print('<значення>::="UNION"')
      case '<значення>','"loop"':
         stack.append('"loop"')
         print('<значення>::="loop"')
      case '<значення>','"numbers"':
         stack.append('"numbers"')
         print('<значення>::="numbers"')
      case '<оператор_WHERE>','"WHERE"':
         stack.append('<оператор_WHERE\'>')
         print('<оператор_WHERE>::=<оператор_WHERE\'>')
      case '<оператор_INTERSECT>','"INTERSECT"':
         stack.append('<оператор_INTERSECT\'>')
         print('<оператор_INTERSECT>::=<оператор_INTERSECT\'>')
      case '<оператор_UNION>','"UNION"':
         stack.append('<оператор_UNION\'>')
         print('<оператор_UNION>::=<оператор_UNION\'>')
      case '<проєкція>','","':
         stack.append('<проєкція\'>')
         print('<проєкція>::=<проєкція\'>')
      case '<назва>','","':
         stack.append('<назва\'>')
         print('<назва>::=<назва\'>')
      case '<літера>','","':
         stack.append('<літера\'>')
         print('<літера>::=<літера\'>')
      case '<цифра>','","':
         stack.append('<цифра\'>')
         print('<цифра>::=<цифра\'>')
      case '<перелік_полів>','","':
         stack.append('<перелік_полів\'>')
         print('<перелік_полів>::=<перелік_полів\'>')
      case '<оператор_рівності>','","':
         stack.append('<оператор_рівності\'>')
         print('<оператор_рівності>::=<оператор_рівності\'>')
      case '<число>','","':
         stack.append('<число\'>')
         print('<число>::=<число\'>')
      case '<результат_оператору>','","':
         stack.append('<результат_оператору\'>')
         print('<результат_оператору>::=<результат_оператору\'>')
      case x, y:
         print('Error')
         break