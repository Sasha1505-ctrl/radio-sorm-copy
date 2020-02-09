import re
from dataclasses import dataclass
from sorm.kaitai.parser import Tetra
from datetime import datetime
from enum import Enum, unique
from typing import Optional

from sorm.utility import bcd_to_str, bcd_to_time


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

    def get_number(self):
        return re.sub(r'[f]+', '', self.number)

    def get_type(self) -> str:
        if re.search(r'(10|e)(20250075)(78)?\d{3,4}', self.number) and self.stype is UserType.inner:
            return 'RADIO'
        elif re.search(r'(67)[2]?\d{5}', self.number) and self.stype is UserType.outer:
            return 'VSS'
        else:
            return 'UNKNOWN'

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
class Reg:
    """
    Tetra Reg class wrapper
    """
    def __init__(self, reg: Tetra.Reg):
        self._id = reg.seq_num,
        self._nitsi = bcd_to_str(reg.served_nitsi),
        self._location = reg.location,
        self._prev_location = reg.prev_location,
        self._reg_at = bcd_to_time(reg.timestamp),


    def get_number(self) -> str:
        return re.sub(r'[f]+','', str(self._nitsi))


    def __str__(self):
        return f'{self._reg_at}:{self.get_number()}'.format(self=self)

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
    call_duration: int
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
