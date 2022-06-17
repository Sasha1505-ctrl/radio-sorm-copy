from typing import List, Tuple, DefaultDict
from collections import deque, defaultdict
from cdr import Gcdr, Subscriber, Dvo, Interfacez, UserType, CallType, Reg
from enum import Enum
from pathlib import Path
import logging
from utility import bcd_to_str, bcd_to_time, to_sec

UNDEFINED_LOCATION: int = 0

_filename = Path()
_logger: logging.Logger
_provider_id: int
_call_stack = deque()
_reg_buffer: DefaultDict[str, List[Reg]] = defaultdict(list)
_cdr_buffer: List[Gcdr] = []

class MockUi(Enum):
    Inner = 0

class MockInt:
    def __init__(self):
        self.ui = MockUi.Inner
        self.pui_type = 0
        self.pui_index = 0

void_int = Interfacez(MockInt())

def cdr_parser(
    filename, version: int, provider_id: int, logger
) -> Tuple[List[Gcdr], DefaultDict[str, List[Reg]]]:

    global _filename
    global _logger
    global _provider_id
    _provider_id = provider_id
    _logger = logger
    _filename = filename
    target = Tetra.from_file(filename)

    logger.debug(f"Пытаюсь разобрать {filename} при помощи {version} версии парсера")
    if version == 5:
        from kaitai.parser.tetra_v5 import Tetra
    if version == 6:
        from kaitai.parser.tetra_v6 import Tetra
    elif version == 7:
        from kaitai.parser.tetra_v7 import Tetra
    else:
        logger.error(f"Не удалось загрузить модуль парсера")
        raise Exception("Не удалось загрузить модуль парсера")

    for blk in target.block:
        logger.debug(f"Starting new block {blk.header.block_num} in CDR file")
        for event in blk.events.event:
            if event.body.type == Tetra.Types.toc:
                processing_toc(event)
            if event.body.type == Tetra.Types.tcc:
                processing_tcc(event)
            if event.body.type == Tetra.Types.out_g:
                processing_out_g(event)
            if event.body.type == Tetra.Types.in_g:
                processing_in_g(event)
            if event.body.type == Tetra.Types.reg:
                processing_reg(event)
            if event.body.type == Tetra.Types.sms:
                processing_sms(event)

        logger.info(
            f"End reading block. Calls quantity: {len(_cdr_buffer)}."
            f"Regs quantity: {len(_reg_buffer)}"
        )
    return _cdr_buffer, _reg_buffer

def processing_toc(event):
    """Обработка записи инициализации вызова TOC"""
    if _call_stack:
        rec = _call_stack.pop()
        _logger.error(
                        f"Неожиданное вхождение TOC записи в {_filename}."
                        f"Call stack member is {rec.type} -> "
                        f"cr: {rec.call_reference}"
                    )
    _logger.debug(
                    f"TOC: {event.body.seq_num} cr: {event.body.call_reference}"
                )
    if event.body.members == 65535:
                    # Обработка персонального вызова
        if event.body.call_reference == 0:
                        # Звонок не состоялся. Строим GCDR и сохраняем в CSV
            toc: Tetra.Toc = event.body
            userA = Subscriber(
                            UserType.inner,
                            bcd_to_str(toc.served_number),
                            toc.location,
                            toc.location,
                            _logger,
                        )
            userB = Subscriber(
                            UserType.inner,
                            bcd_to_str(toc.called_number),
                            UNDEFINED_LOCATION,
                            UNDEFINED_LOCATION,
                            _logger,
                        )
            dvo = Dvo(False)
            gdp = Gcdr(
                            toc.dxt_id.as_int,
                            _provider_id,
                            bcd_to_time(toc.setup_time),
                            to_sec(toc.duration),
                            userA,
                            userB,
                            void_int,
                            void_int,
                            toc.termination,
                            dvo,
                            CallType.toc,
                        )
            _cdr_buffer.append(gdp)
        else:
                        # Звонок состоялся. Инициализируем GCDR и ждем TCC или OutG
            _call_stack.append(event.body)
    else:
                    # Обработка группового вызова. Строим GCDR и сохраняем его в CSV
        toc = event.body
        userA = Subscriber(
                        UserType.inner,
                        bcd_to_str(toc.served_number),
                        toc.location,
                        toc.location,
                        _logger,
                    )
        userB = Subscriber(
                        UserType.inner,
                        bcd_to_str(toc.called_number),
                        UNDEFINED_LOCATION,
                        UNDEFINED_LOCATION,
                        _logger,
                    )
        dvo = Dvo(False)
        gdp = Gcdr(
                        toc.dxt_id.as_int,
                        _provider_id,
                        bcd_to_time(toc.setup_time),
                        to_sec(toc.duration),
                        userA,
                        userB,
                        void_int,
                        void_int,
                        toc.termination,
                        dvo,
                        CallType.toc,
                    )
        _cdr_buffer.append(gdp)

def processing_tcc(event):
    """Обработка запси терминации вызова TCC"""
    if not _call_stack:
        _logger.error(
        f"Не обработаны записи TOC или InG для звонка"
        f"{event.body.type} -> cr: {event.body.call_reference}"
        )
        return
    _logger.debug(
                f"TCC: {event.body.seq_num} cr: {event.body.call_reference}"
                )
    partial_cdr = _call_stack.pop()
    if partial_cdr.call_reference == event.body.call_reference:
        """Все совпало. Будем собирать Gcdr"""
        tcc = event.body
        dvo = Dvo(False)
        if type(partial_cdr) is Tetra.Toc:
            userA = Subscriber(
                UserType.inner,
                bcd_to_str(partial_cdr.served_number),
                partial_cdr.location,
                UNDEFINED_LOCATION,
                _logger,
            )
            userB = Subscriber(
                UserType.inner,
                bcd_to_str(tcc.served_number),
                tcc.location,
                UNDEFINED_LOCATION,
                _logger,
            )
            gdp = Gcdr(
                partial_cdr.dxt_id.as_int,
                _provider_id,
                bcd_to_time(partial_cdr.setup_time),
                to_sec(partial_cdr.duration),
                    userA,
                    userB,
                    void_int,
                    void_int,
                    partial_cdr.termination,
                    dvo,
                    CallType.toctcc,
                )
            _cdr_buffer.append(gdp)
        elif type(partial_cdr) is Tetra.InG:
            userA = Subscriber(
                UserType.outer,
                bcd_to_str(partial_cdr.calling_number),
                UNDEFINED_LOCATION,
                UNDEFINED_LOCATION,
                _logger,
                )
            userB = Subscriber(
                UserType.inner,
                bcd_to_str(tcc.served_nitsi),
                tcc.location,
                UNDEFINED_LOCATION,
                _logger,
            )
            gdp = Gcdr(
                tcc.dxt_id.as_int,
                _provider_id,
                bcd_to_time(tcc.setup_time),
                to_sec(tcc.duration),
                userA,
                userB,
                Interfacez(partial_cdr.in_int),
                void_int,
                tcc.termination,
                dvo,
                CallType.ingtcc,
            )
            _cdr_buffer.append(gdp)
        else:
            raise ValueError(f"Неожиданный тип объекта {type(partial_cdr)}")
    else:
        raise ValueError(
            f"Не соответствие call_reference обрабатываемых записей"
            f"{partial_cdr.call_reference} != {event.body.call_reference}"
        )

def processing_out_g(event):
    """Обработка записи звонка исходящего на фиксированную сеть TOC -> OutG"""
    if len(_call_stack) == 0:
        raise ValueError(f"Не обработана запись TOC для звонка {event.body.call_reference}")
    _logger.debug(f"OutG: {event.body.seq_num} cr: {event.body.call_reference}")
    toc: Tetra.Toc = _call_stack.pop()
    out_g: Tetra.OutG = event.body
    userA = Subscriber(
                    UserType.inner,
                    bcd_to_str(toc.served_number),
                    toc.location,
                    UNDEFINED_LOCATION,
                    _logger,
                )
    userB = Subscriber(
                    UserType.outer,
                    bcd_to_str(out_g.transmitted_number),
                    UNDEFINED_LOCATION,
                    UNDEFINED_LOCATION,
                    _logger,
                )
    dvo = Dvo(False)
    gdp = Gcdr(
                    toc.dxt_id.as_int,
                    _provider_id,
                    bcd_to_time(toc.setup_time),
                    to_sec(toc.duration),
                    userA,
                    userB,
                    void_int,
                    Interfacez(out_g.out_int),
                    toc.termination,
                    dvo,
                    CallType.tocoutg,
                )
    _cdr_buffer.append(gdp)

def processing_in_g(event):
    """Обработка записи звонка пришедшего из внешней сети"""
    _logger.debug(
        f"InG: {event.body.seq_num} cr: {event.body.call_reference}"
        )
    if event.body.call_reference == 0:
    # Звонок не состоялся. Строим GCDR и сохраняем его в CSV
        in_g: Tetra.InG = event.body
        userA = Subscriber(
            UserType.outer,
            bcd_to_str(in_g.calling_number),
            UNDEFINED_LOCATION,
            UNDEFINED_LOCATION,
            _logger,
            )
        userB = Subscriber(
            UserType.inner,
            bcd_to_str(in_g.called_number),
            UNDEFINED_LOCATION,
            UNDEFINED_LOCATION,
            _logger,
            )
        dvo = Dvo(False)
        gdp = Gcdr(
            in_g.dxt_id.as_int,
            _provider_id,
            bcd_to_time(in_g.setup_time),
            to_sec(in_g.duration),
            userA,
            userB,
            Interfacez(in_g.in_int),
            void_int,
            in_g.termination,
            dvo,
            CallType.ing,
            )
        _cdr_buffer.append(gdp)
    else:
        # Продолжаем обрабатывать звонок
        _call_stack.append(event.body)

def processing_reg(event):
    """Обработка записи о регистрации абонента"""
    _logger.debug(
                    f"REG: {event.body.seq_num} "
                    f"SERVED_NITSI: {bcd_to_str(event.body.served_nitsi)} "
                    f"LOCATION: {event.body.location}:{event.body.prev_location}"
                )
    reg = Reg(event.body)
    _reg_buffer[reg.get_number()].append(reg)

def processing_sms(event):
    """Обработка записи о текстовом сообщении"""
    _logger.debug("I'am find SMS")
    sds: Tetra.Sds = event.body
    userA = Subscriber(
                    UserType.inner,
                    bcd_to_str(sds.served_number),
                    sds.location,
                    sds.location,
                    _logger,
                )
    userB = Subscriber(
                    UserType.inner,
                    bcd_to_str(sds.connected_number),
                    UNDEFINED_LOCATION,
                    UNDEFINED_LOCATION,
                    _logger,
                )
    dvo = Dvo(False)
    gdp = Gcdr(
                    sds.dxt_id.as_int,
                    _provider_id,
                    bcd_to_time(sds.time_stamp),
                    to_sec(0),
                    userA,
                    userB,
                    void_int,
                    void_int,
                    sds.sds_type,
                    dvo,
                    CallType.sms,
                )
    _cdr_buffer.append(gdp)
