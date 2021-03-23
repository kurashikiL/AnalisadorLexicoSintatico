from sly import Lexer, Parser

class CalcLexer(Lexer):
    tokens = { NAME, NUMBER, PRINT,READ,FOR,UNTIL,STEP }
    ignore = ' \t'
    literals = { '=', '+', '-', '*', '/', '(', ')' }

    # Tokens
    NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'
    NAME['print'] = PRINT
    NAME['read'] = READ
    NAME['for'] = FOR
    NAME['until'] = UNTIL
    NAME['step'] = STEP
  
    @_(r'\d+')
    def NUMBER(self, t):
        t.value = int(t.value)
        return t

    @_(r'\n+')
    def newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print("Illegal character '%s'" % t.value[0])
        self.index += 1

class CalcParser(Parser):
    tokens = CalcLexer.tokens

    precedence = (
        ('left', '+', '-'),
        ('left', '*', '/'),
        )

    def __init__(self):
        self.names = { }

    @_('NAME "=" expr')
    def statement(self, p):
        self.names[p.NAME] = p.expr

    @_('PRINT "(" expr ")"')
    def expr(self,p):
        return p.expr
    
    @_('READ "(" NAME ")"')
    def expr(self,p):
        return("")  
    
    #for ( a = 10 until b step 1) 1+1
    @_('FOR "(" NAME "=" expr UNTIL NAME STEP NUMBER ")" expr ')
    def expr(self,p):
        try:
            self.names[p.NAME1]
        except LookupError:
            return("ERRO, Variavel não inicializada '%s'" % p.NAME)
            
        var = 0
        self.names[p.NAME0] = p.expr0
        while(self.names[p.NAME0] <= self.names[p.NAME1]):
            var += p.expr1
            self.names[p.NAME0] += p.NUMBER
        return var
        
    
    @_('expr')
    def statement(self, p):
        print(p.expr)

    @_('expr "+" expr')
    def expr(self, p):
        return p.expr0 + p.expr1

    @_('expr "-" expr')
    def expr(self, p):
        return p.expr0 - p.expr1

    @_('expr "*" expr')
    def expr(self, p):
        return p.expr0 * p.expr1

    @_('expr "/" expr')
    def expr(self, p):
        return p.expr0 / p.expr1

    @_('"(" expr ")"')
    def expr(self, p):
        return p.expr

    @_('NUMBER')
    def expr(self, p):
        return p.NUMBER

    @_('NAME')
    def expr(self, p):
        try:
            return self.names[p.NAME]
        except LookupError:
            return("ERRO, Variavel não inicializada '%s'" % p.NAME)
            
            

if __name__ == '__main__':
    lexer = CalcLexer()
    parser = CalcParser()
    while True:
        try:
            text = input('calc > ')
        except EOFError:
            break
        if text:
            parser.parse(lexer.tokenize(text))
