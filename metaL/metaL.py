# https://github.com/ponyatov/itstep/wiki/metaL

import os,sys

##################################### расширенная модель фреймов Марвина Мински

################################################### базовый класс Frame (фрейм)

class Frame:

    ############################################################### конструктор
    def __init__(self,V):
        # тэг типа/класса
        self.type = self.__class__.__name__.lower()
        # скалярное значение
        self.val  = V
        # ассоциативный массив слотов, указывающий на другие слоты по имени
        self.slot = {}
        # упорядоченное хранилище = вектор = стек = очередь
        self.nest = []
        # счетчик ссылок для системы автоматического управления памятью (см. сборщик мусора)
        self.ref  = 0
        
    # служебные методы для сборки мусора,
    def _use(self): self.ref += 1
    # для Python полагаемся на встроенные механизмы автоматической памяти
    def _free(self): self.ref -= 1
    # при реализации на C++ придется писать собственные спец.аллокаторы
    
    ############################################################ текстовый дамп

    # callback для print, вызывается автоматически в т.ч. в выражениях '%s' % frame
    def __repr__(self):
        return self.dump()
    
    # полный дамп в виде дерева
    def dump(self,depth=0,prefix=''):
        # начало секции текста: заголовок сдвинутый табуляциями на глубину вложенности поддерева
        tree = self._pad(depth) + self.head(prefix)
        # проверка на рекурсивность структуры
        if not depth: Frame._dumped = []
        # если текущий фрейм уже сдампили раньше, внутренности не показываем _/
        if self in Frame._dumped: return tree + ' _/'
        else: Frame._dumped.append(self)
        # дамп слотов: каждый слот выводим в форме <имя> = <содержимое связанного слота...>
        for i in self.slot:
            tree += self.slot[i].dump(depth+1,prefix=i+' = ')
        # дамп вложенных слотов (рекурсивно)
        for j in self.nest:
            tree += j.dump(depth+1)
        # возвращаем строку полученного дампа
        return tree
    
    # короткий дамп фрейма: только заголовок, уникальный id, и счетчик ссылок
    def head(self,prefix=''):
        return '%s<%s:%s> @%x #%i' % \
            (prefix,self.type,self._val(),id(self),self.ref)

    # private: отбивка переводом строки и табуляциями (для дампа деревом)
    def _pad(self,depth):
        return '\n' + '\t' * depth
    # private: представление значения в виде строки для дампа (возможны варианты)
    def _val(self):
        return str(self.val)
    
    ########################################################## Python-операторы

    # A['key']
    def __getitem__(self,key):
        return self.slot[key]
    # A['key'] = B
    def __setitem__(self,key,that):
        self.slot[key] = that ; that._use() ; return self
    # A << B ~> A[B.val] = B
    def __lshift__(self,that):
        self[that.val] = that ; return self
    # A // B
    def __floordiv__(self,that):
        return self.push(that)
    
    ######################################################### стековые операции

    # ( -- A )
    def push(self,that):
        self.nest.append(that) ; that._use() ; return self
    # ( A -- )
    def pop(self):
        return self.nest.pop(-1)
    # ( A -- A )
    def top(self):
        return self.nest[-1]
    
    ######################################################### выполнение фрейма
    
    # по умолчанию фрейм вычисляется сам в себя
    def eval(self,ctx): ctx // self
    
    ####################################### вывод дерева фреймов в формате GOjs

    def plot(self,depth=0,parent=None,link=None):
        nodes = ''
        par = ''
        if parent: par = ', "parent":%i ' % id(parent)
        if link: par += ', "link":"%s" ' % link
        def key(what):
            return '\n{ "key":%i, "head":"%s:%s" %s },' % \
                (id(what),what.type,what._val(),par) 
        nodes += key(self)
        if not depth: Frame._ploted = []
        if self in Frame._ploted: return nodes
        else: Frame._ploted.append(self)
        for i in self.slot:
            nodes += self.slot[i].plot(depth+1,parent=self,link=i)
        count = 0
        for j in self.nest:
            count += 1
            nodes += j.plot(depth+1,parent=self,link=count)
        if not depth: return '[%s]' % nodes[:-1]
        else: return nodes

# hello = Frame('hello') ; hello // hello ; hello << hello
# print(hello)

class Primitive(Frame):
    # все примитивы вычисляются сами в себя
    def eval(self,ctx): ctx // self

class Symbol(Primitive): pass

class String(Primitive): pass

class Number(Primitive): pass

class Integer(Number): pass

class Hex(Integer): pass

class Bin(Integer): pass

################################################## активные исполняемые объекты

class Active(Frame): pass

class Context(Active):
    def __init__(self,V):
        Active.__init__(self, V)
        self.compile = []
    def __lshift__(self,F):
        if callable(F): return self << Cmd(F)
        else: return Active.__lshift__(self, F)
    def __setitem__(self,key,F):
        if callable(F): self[key] = Cmd(F) ; return self
        else: return Active.__setitem__(self,key,F)

class Cmd(Active):
    def __init__(self,F):
        Active.__init__(self, F.__name__)
        self.fn = F
    def eval(self,ctx):
        self.fn(ctx)
        
#################################################################### ввод/вывод

class IO(Frame): pass

############################################################### сетевые функции

class Net(IO): pass

class IP(Net): pass

class Port(Net):
    def __init__(self,V):
        Net.__init__(self, int(V))
        
############################################################## документирование

class Doc(Frame): pass

class Font(Doc): pass

class Size(Doc): pass

class Color(Doc): pass

################################################################# web-интерфейс

class Web(Net):
    def __init__(self,V):
        Net.__init__(self, V)
        self['host'] = IP('127.0.0.1')
        self['port'] = Port(8888)
        self['font'] = Font('monospace')
        self['font']['size'] = Size('3mm')
        self['fore'] = Color('lightgreen')
        self['back'] = Color('black')
    def eval(self,ctx):
        import flask,flask_wtf
        import wtforms as wtf
        
        app   = flask.Flask(self.val)
        app.config['SECRET_KEY'] = os.urandom(0x11)
        
        class CLI(flask_wtf.FlaskForm):
            pad = wtf.TextAreaField('PAD',\
                                    default='# put your commands here',\
                                    render_kw={'rows':'5','autofocus':True})
            go  = wtf.SubmitField('GO')
        
        @app.route('/', methods=['GET', 'POST'])
        def index():
            form = CLI()
            if form.validate_on_submit(): ctx // String(form.pad.data) ; INTERPRET(ctx)
            return flask.render_template('index.html',form=form,ctx=ctx,web=self)
        
        @app.route('/<path>.css')
        def css(path):
            return flask.Response(\
                flask.render_template(path + '.css',ctx=ctx,web=self),\
                mimetype='text/css')
        
        @app.route('/<path>.png')
        def png(path):
            return app.send_static_file('%s.png' % path )
        
        @app.route('/plot/', methods=['GET', 'POST'])
        def plot():
            form = CLI()
            if form.validate_on_submit(): ctx // String(form.pad.data) ; INTERPRET(ctx)
            return flask.render_template('plot.html',form=form,ctx=ctx,web=self)
        
        @app.route('/ajax/plot')
        def ajax_plot(): return ctx.plot()
        
        app.run(host=self['host'].val,port=self['port'].val,debug=True)

########################################################### глобальный контекст

glob = Context('global') ; glob['S'] = glob['W'] = glob

########################################################## управление и отладка

def BYE(ctx): sys.exit(0)
glob << BYE

glob['NOP'] = lambda ctx: None

################################################################# web-интерфейс

def WEB(ctx): ctx['WEB'] = Web('metaL') ; ctx['WEB'].eval(ctx)
glob << WEB

######################################################## no-syntax парсер (PLY)

import ply.lex as lex

tokens = ['symbol','integer']

t_ignore = ' \t\r\n'
t_ignore_comment = '[\\\#].*'

def t_integer(t):
    r'[+\-]?[0-9]+'
    return Integer(t.value)

def t_symbol(t):
    r'[^ \t\r\n\\\#]+'
    return Symbol(t.value)

def t_error(t):
    raise SyntaxError(t)

lexer = lex.lex()

########################################################## интерпретатор команд

# ( -- token ) парсер выделяет один токен из входного потока
def WORD(ctx):
    token = lexer.token()
    if token: ctx // token
    return token

# ( symbol:token -- found | token ) поиск в словаре по имени
def FIND(ctx):
    token = ctx.pop()
    try:   ctx // ctx[token.val]  ; return True
    except KeyError: ctx // token ; return False
    
# ( frame -- ) выполнить фрейм
def EVAL(ctx):
    ctx.pop().eval(ctx)
    
# ( str -- ... ) интерпретатор строки как команды metaL
def INTERPRET(ctx):
    lexer.input(ctx.pop().val)
    while True:
        if not WORD(ctx): break
        if isinstance(ctx.top(), Symbol):
            if not FIND(ctx): pass
        if ctx.compile:
              COMPILE(ctx)
        else: EVAL(ctx)

# Read-Eval-Print-Loop
def REPL(ctx):
    while True:
        print(ctx)
        try:             ctx // String(input('\nok> ')) ; INTERPRET(ctx)
        except EOFError: BYE(ctx)
        
################################################################# инициализация
        
WEB(glob)
REPL(glob)
