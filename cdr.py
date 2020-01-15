from dataclasses import dataclass
from kaitai.parser.tetra import Tetra
from datetime import datetime

@dataclass
class Subscriber:
    """
    Абонент сети (радио/всс)
    stype: тип абонента (внешний/внутренний) относительно коммутатора Тетра
    mumbber: телефонный номер абонента
    start_location: номер БС в начале разговора (для внутренних абонентов)
    end_location: номер БС в конце разговора (для внутренних абонентов)
    """

    stype: int
    number: str
    start_location: int
    end_location: int


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
    
    dxt_id: int
    provider_id: int
    date: datetime
    call_duration: int
    abon_a: Subscriber
    abon_b: Subscriber
    if_in: str
    if_out: str
    call_termination: Tetra.Terminations
    dvo: Dvo
    call_type: int = 1





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
