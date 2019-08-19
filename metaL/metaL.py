# https://github.com/ponyatov/itstep/wiki/metaL

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

hello = Frame('hello') ; hello // hello ; hello << hello
print(hello)
