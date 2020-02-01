import re
from dataclasses import dataclass
from kaitai.parser.tetra_v7 import Tetra
from datetime import datetime
from enum import Enum, unique

@unique
class UserType(Enum):
    inner = 1
    outer = 2

@unique
class CallType(Enum):
    toc = 1
    toctcc = 2
    tocoutg = 3
    ing = 4
    ingtcc = 5

@dataclass
class Subscriber:
    """
    Абонент сети (радио/всс)
    stype: тип абонента (внешний/внутренний) относительно коммутатора Тетра
    mumbber: телефонный номер абонента
    start_location: номер БС в начале разговора (для внутренних абонентов)
    end_location: номер БС в конце разговора (для внутренних абонентов)
    """

    stype: UserType
    number: str
    start_location: int
    end_location: int

    def getNumber(self):
        return re.sub(r'[f]+', '', self.number)

    def getType(self) -> str:
        if re.search(r'(10|e)(20250075)(78)?\d{3,4}', self.number) and self.stype is UserType.inner:
            return 'RADIO'
        elif re.search(r'(67)[2]?\d{5}', self.number) and self.stype is UserType.outer:
            return 'VSS'
        else:
            return 'UNKNOWN'

    def __str__(self):
        return f'{self.getNumber()}'.format(self)

class Interfacez:
    """
    Tetra.Interface class wrapper
    """
    def __init__(self, int: Tetra.Interface):
        self._ui = int.ui
        self._pui_type = int.pui_type
        self._pui_index = int.pui_index
    def __str__(self):
        return f'Int: {self._ui}:{self._pui_type}{self._pui_index}'.format(self)


@dataclass
class Dvo:
    """
    Дополнительные виды обслуживания
    switch: признак наличия дополнительного вида обслуживания (переадресация, ???) всего этого у нас нет
    call_forwarding: номер куда был переадресован вызов
    edge_dxt_id: идентификатор граничного коммутатора
    rouming_dxt_id: идентификатор роумингового партнера
    """    

    switch: bool
    call_forvarding: str = '--'
    edge_dxt_id: str = '--'
    rouming_dxt_id = '--'

@dataclass
class Gcdr:
    """
    General call data record presentation
    dxt_id: Идентификатор коммутатора
    provider_id: Код филиала
    date: дата звонка
    call_duration: длятельность разговора
    abon_a: вызывающий абонент
    abon_b: вызываемый абонент
    if_in входящий интерфейс для IN_G -> TCC
    if_out: исходящий интерфейс для TOC -> Out_G
    call_termination: Причина завершения вызова
    dvo: дополнительные виды обслуживания
    call_type: тип соединения    
    """
    
    dxt_id: str
    provider_id: int
    date: datetime
    call_duration: int
    abon_a: Subscriber
    abon_b: Subscriber
    if_in: Interfacez
    if_out: Interfacez
    call_termination: Tetra.Terminations
    dvo: Dvo
    call_type: CallType

    @property
    def get_dxt_id(self):
        return "".join([hex(i)[2:] for i in self.dxt_id])

    def __iter__(self):
        return iter([str(self.date), self.call_duration, self.call_type, self.dvo.switch, self.abon_a.getType(),
                     self.dxt_id, self.abon_b.getType(), str(self.if_in), str(self.if_out), self.dvo.edge_dxt_id,
                     self.dvo.rouming_dxt_id, str(self.call_termination), self.abon_a.getNumber(),
                     self.abon_a.start_location, self.abon_a.end_location, self.abon_b.getNumber(),
                     self.abon_b.start_location, self.abon_b.end_location])

    #def __init__(self, call_reference):
    #    self.__call_reference = call_reference

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
