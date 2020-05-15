import re
from dataclasses import dataclass
from sorm.kaitai.parser.tetra_v7 import Tetra
from datetime import datetime, timedelta
from enum import Enum, unique
from typing import Optional, List, DefaultDict

from sorm.utility import bcd_to_str, bcd_to_time


@unique
class UserType(Enum):
    inner = 1
    outer = 2
    unknown = 9 


@unique
class CallType(Enum):
    toc = 1
    toctcc = 2
    tocoutg = 3
    ing = 4
    ingtcc = 5

class Reg:
    """
    Tetra Reg class wrapper
    """
    def __init__(self, reg: Tetra.Reg):
        self._id = reg.seq_num
        self._nitsi = bcd_to_str(reg.served_nitsi)
        self._location = reg.location
        self._prev_location = reg.prev_location
        self._reg_at = bcd_to_time(reg.timestamp)


    def get_number(self) -> str:
        return re.sub(r'[f]+','', self._nitsi)

    @property
    def reg_at(self) -> datetime:
        return self._reg_at
    
    @property
    def get_location(self) -> str:
        return self._location


    def __str__(self):
        return f'{self._reg_at}:{self.get_number()}'.format(self=self)


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

    def get_number(self):
        return re.sub(r'[f]+', '', self.number)

    #  TODO: масло, маслянное. Думаю нужно переименвать в check_type и проверять при формировании записи.
    def get_type(self) -> UserType:
        if re.search(r'(10|e)(2025000075)(78)?\d{3,4}', self.number) and self.stype is UserType.inner:
            return UserType.inner 
        elif re.search(r'[6]?[2]?(7)\d{5}', self.number) and self.stype is UserType.outer:
            return UserType.outer
        else:
            return UserType.unknown
   
    def get_last_location(self, reg_buffer: DefaultDict[str, List[Reg]], sd: datetime, td: timedelta) ->None:

        """
        Определяем местоположение аблнента
        reg_buffer: Список регистраций абонентов в обрабатываемом файле
        sd: Start DateTime время начала разговора
        td: Длительность разговора
        """
        print(f'Abonent type is {self.stype}')
        if self.stype == UserType.inner:
            print(f'Check rouming for user {self.get_number()}')
            # pprint(reg_buff.get(gcdr.abon_a.get_number())
            if td > timedelta(minutes=1):
                print('-- check reg_buffer')
                lst = reg_buffer.get(self.get_number())
                new_list = [reg for reg in lst if reg.reg_at > sd and reg.reg_at <= sd + td]
                if len(new_list) != 0:
                    print(f'Rouming occured {self.number}')
                    self.location = new_list[-1].get_location
                else:
                    self.end_location = self.start_location
            else:
                self.end_location = self.start_location

 
    def __str__(self):
        return f'{self.get_number()}'.format(self)


class Interfacez:
    """
    Tetra.Interface class wrapper
    """
    def __init__(self, interface: Tetra.Interface):
        self._ui = interface.ui
        self._pui_type = interface.pui_type
        self._pui_index = interface.pui_index
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
    rouming_dxt_id: str = '--'


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
    call_duration: timedelta 
    abon_a: Subscriber
    abon_b: Subscriber
    if_in: Optional[Interfacez]
    if_out: Optional[Interfacez]
    call_termination: Tetra.Terminations
    dvo: Dvo
    call_type: CallType

    @property
    def get_dxt_id(self):
        return "".join([hex(i)[2:] for i in self.dxt_id])

    def __iter__(self):
        return iter([str(self.date), self.call_duration, self.call_type, self.dvo.switch, self.abon_a.get_type(),
                     self.dxt_id, self.abon_b.get_type(), str(self.if_in), str(self.if_out), self.dvo.edge_dxt_id,
                     self.dvo.rouming_dxt_id, str(self.call_termination), self.abon_a.get_number(),
                     self.abon_a.start_location, self.abon_a.end_location, self.abon_b.get_number(),
                     self.abon_b.start_location, self.abon_b.end_location])
