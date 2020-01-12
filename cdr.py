class Cdr:
    """
    General call data record presentation
    call_reference - порядковый номер звонка
    """

    def __init__(self, call_reference):
        self.__call_reference = call_reference

    def add_toc(self, toc, group=False, termination='ok'):
        if self.__call_reference != toc.call_reference:
            raise ValueError("uндикаторы звонка не совпадают self.{__call_reference} != {call_reference}".format(self.__call_reference, toc.call_reference))
        if toc.members == 65535:
            # Персональный вызов
            if self.__call_reference == 0:
                # Вызов не состоялся, ошибка соединения.
                print(f'add_toc() - abonent is busy {toc.termination}')
            else:
                # Обработка персонального вызова. Ожидаем получения ТСС или 
                print("add_toc() - Start call parser")
        else:
            # Групповой вызов
            print("add_toc() - Group Call")
        # Init head rec
        self.seq_num = toc.seq_num
    
    def add_tcc(self, tcc):
        if self.__call_reference != tcc.call_reference:
            raise IOError("uндикаторы звонка не совпадают self.{__call_reference} != {call_reference}".format(self.__call_reference, toc.call_reference))

        # Append data to rec
        print("add_tcc() - calling")
