# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
from kaitaistruct import __version__ as ks_version, KaitaiStruct, KaitaiStream, BytesIO
from enum import Enum


if parse_version(ks_version) < parse_version('0.7'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.7 or later is required, but you have %s" % (ks_version))

from .bcd import Bcd
class Tetra(KaitaiStruct):
    """CDR Parser for Tetra switch software v5.5
    """

    class Terminations(Enum):
        ok = 1
        busy = 2
        partial_record = 3
        bad_number = 4
        reject_by_user = 5
        reject_by_operator = 6
        reject_by_gw = 7
        eight = 8
        faill = 9

    class Types(Enum):
        toc = 1
        tcc = 2
        in_g = 3
        out_g = 4
        sms = 5
        data = 6
        farward = 7
        redirect = 8
        reg = 9

    class UnitIndexT(Enum):
        fnim0 = 0
        fnim1 = 1
        fnim2 = 2
        fnim3 = 3
        fnim4 = 4
        fnim5 = 5
        fnim6 = 6
        fnim7 = 7
        isdn = 8
        fnimet = 9
        sip = 10
        err = 255

    class SdsTypes(Enum):
        sds_1 = 0
        sds_2 = 1
        sds_3 = 2
        sds_4 = 3
        status = 4
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self._raw_block = []
        self.block = []
        i = 0
        while not self._io.is_eof():
            self._raw_block.append(self._io.read_bytes(65408))
            io = KaitaiStream(BytesIO(self._raw_block[-1]))
            self.block.append(self._root.Block(io, self, self._root))
            i += 1


    class Reg(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.type = self._root.Types(self._io.read_u1())
            self.version = self._io.read_u1()
            self._raw_dxt = self._io.read_bytes(4)
            io = KaitaiStream(BytesIO(self._raw_dxt))
            self.dxt = self._root.FourByteBcd(io, self, self._root)
            self.checksum = self._io.read_u2le()
            self.seq_num = self._io.read_u2le()
            self.served_nitsi = self._io.read_bytes(10)
            self.assigned_itsi = self._io.read_bytes(10)
            self.originator_itsi = self._io.read_bytes(10)
            self.organisation_block = self._io.read_bytes(12)
            self.tei = self._io.read_bytes(8)
            self.registration_type = self._io.read_bytes(1)
            self.authentication = self._io.read_bytes(1)
            self.encription = self._io.read_bytes(1)
            self.class_ms = self._io.read_bytes(4)
            self._raw_dxt_id = self._io.read_bytes(4)
            io = KaitaiStream(BytesIO(self._raw_dxt_id))
            self.dxt_id = self._root.FourByteBcd(io, self, self._root)
            self._raw_prev_dxt_id = self._io.read_bytes(4)
            io = KaitaiStream(BytesIO(self._raw_prev_dxt_id))
            self.prev_dxt_id = self._root.FourByteBcd(io, self, self._root)
            self.location = self._io.read_u2le()
            self.prev_location = self._io.read_u2le()
            self.cell = self._io.read_bytes(1)
            self._raw_timestamp = self._io.read_bytes(8)
            io = KaitaiStream(BytesIO(self._raw_timestamp))
            self.timestamp = self._root.Time(io, self, self._root)
            self.accept = self._io.read_bytes(1)
            self.reject = self._io.read_bytes(1)


    class FourByteBcd(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.fourth = Bcd(2, 4, False, self._io)
            self.third = Bcd(2, 4, False, self._io)
            self.second = Bcd(2, 4, False, self._io)
            self.first = Bcd(2, 4, False, self._io)

        @property
        def as_int(self):
            if hasattr(self, '_m_as_int'):
                return self._m_as_int if hasattr(self, '_m_as_int') else None

            self._m_as_int = ((((self.first.as_int * 10000) + (self.second.as_int * 10000)) + (self.third.as_int * 100)) + self.fourth.as_int)
            return self._m_as_int if hasattr(self, '_m_as_int') else None


    class Event(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.len_rec = self._io.read_u2le()
            _on = self.len_rec
            if _on == 251:
                self._raw_body = self._io.read_bytes((self.len_rec - 2))
                io = KaitaiStream(BytesIO(self._raw_body))
                self.body = self._root.Sds(io, self, self._root)
            elif _on == 95:
                self._raw_body = self._io.read_bytes((self.len_rec - 2))
                io = KaitaiStream(BytesIO(self._raw_body))
                self.body = self._root.OutG(io, self, self._root)
            elif _on == 125:
                self._raw_body = self._io.read_bytes((self.len_rec - 2))
                io = KaitaiStream(BytesIO(self._raw_body))
                self.body = self._root.Fraw(io, self, self._root)
            elif _on == 109:
                self._raw_body = self._io.read_bytes((self.len_rec - 2))
                io = KaitaiStream(BytesIO(self._raw_body))
                self.body = self._root.InG(io, self, self._root)
            elif _on == 271:
                self._raw_body = self._io.read_bytes((self.len_rec - 2))
                io = KaitaiStream(BytesIO(self._raw_body))
                self.body = self._root.Toc(io, self, self._root)
            elif _on == 133:
                self._raw_body = self._io.read_bytes((self.len_rec - 2))
                io = KaitaiStream(BytesIO(self._raw_body))
                self.body = self._root.Tcc(io, self, self._root)
            elif _on == 139:
                self._raw_body = self._io.read_bytes((self.len_rec - 2))
                io = KaitaiStream(BytesIO(self._raw_body))
                self.body = self._root.Pd(io, self, self._root)
            elif _on == 92:
                self._raw_body = self._io.read_bytes((self.len_rec - 2))
                io = KaitaiStream(BytesIO(self._raw_body))
                self.body = self._root.Reg(io, self, self._root)
            else:
                self.body = self._io.read_bytes((self.len_rec - 2))


    class Interface(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.ui = self._root.UnitIndexT(self._io.read_u1())
            self.pui_type = self._io.read_u2be()
            self.pui_index = self._io.read_u2be()
            self.ext_line_index = self._io.read_u1()


    class Sds(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.type = self._root.Types(self._io.read_u1())
            self.version = self._io.read_u1()
            self.dxt = self._root.FourByteBcd(self._io, self, self._root)
            self.checksum = self._io.read_u2le()
            self.seq_num = self._io.read_u2le()
            self.ss_numb = self._io.read_u1()
            self.call_reference = self._io.read_u4le()
            self.served_number = self._io.read_bytes(10)
            self.served_nitsi = self._io.read_bytes(10)
            self.organisation_block = self._io.read_bytes(12)
            self.calling_number = self._io.read_bytes(14)
            self.translated_number = self._io.read_bytes(14)
            self.translated_nitsi = self._io.read_bytes(10)
            self.connected_number = self._io.read_bytes(14)
            self.connected_nitsi = self._io.read_bytes(10)
            self.connection_group = self._io.read_u2le()
            self._raw_dxt_id = self._io.read_bytes(4)
            io = KaitaiStream(BytesIO(self._raw_dxt_id))
            self.dxt_id = self._root.FourByteBcd(io, self, self._root)
            self.location = self._io.read_u2le()
            self.cell_identity = self._io.read_bytes(1)
            self.forward_number = self._io.read_bytes(14)
            self.translated_forward_number = self._io.read_bytes(14)
            self.transfer = self._io.read_u1()
            self.message_reference = self._io.read_u1()
            self.sds_service_type = self._io.read_u1()
            self.sds_type = self._root.SdsTypes(self._io.read_u1())
            self.sds_len = self._io.read_u4le()
            self.list_of_groups = self._io.read_bytes(80)
            self.number_of_group = self._io.read_u1()
            self.timestamp = self._root.Time(self._io, self, self._root)
            self.cells_distributed = self._io.read_u2le()
            self.cells_reached = self._io.read_u2le()
            self.dispatchers_reached = self._io.read_u1()
            self.sds_result = self._io.read_u1()


    class Fraw(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.body = self._io.read_bytes((125 - 2))


    class Block(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.header = self._root.Header(self._io, self, self._root)
            self._raw_events = self._io.read_bytes((self.header.length - 65))
            io = KaitaiStream(BytesIO(self._raw_events))
            self.events = self._root.Events(io, self, self._root)
            self.trailer = self._root.Trailer(self._io, self, self._root)


    class Pd(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.body = self._io.read_bytes((139 - 2))


    class Trailer(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.body = self._io.read_bytes(24)


    class OutG(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.type = self._root.Types(self._io.read_u1())
            self.version = self._io.read_u1()
            self._raw_dxt_id = self._io.read_bytes(4)
            io = KaitaiStream(BytesIO(self._raw_dxt_id))
            self.dxt_id = self._root.FourByteBcd(io, self, self._root)
            self.checksum = self._io.read_u2le()
            self.seq_num = self._io.read_u2le()
            self.call_reference = self._io.read_u4le()
            self.calling_number = self._io.read_bytes(10)
            self.calling_ntsi = self._io.read_bytes(10)
            self.transmitted_number = self._io.read_bytes(14)
            self._raw_served_dxt = self._io.read_bytes(4)
            io = KaitaiStream(BytesIO(self._raw_served_dxt))
            self.served_dxt = self._root.FourByteBcd(io, self, self._root)
            self._raw_out_int = self._io.read_bytes(6)
            io = KaitaiStream(BytesIO(self._raw_out_int))
            self.out_int = self._root.Interface(io, self, self._root)
            self.conn_group = self._io.read_bytes(2)
            self._raw_setup_time = self._io.read_bytes(8)
            io = KaitaiStream(BytesIO(self._raw_setup_time))
            self.setup_time = self._root.Time(io, self, self._root)
            self._raw_answer_time = self._io.read_bytes(8)
            io = KaitaiStream(BytesIO(self._raw_answer_time))
            self.answer_time = self._root.Time(io, self, self._root)
            self._raw_release_time = self._io.read_bytes(8)
            io = KaitaiStream(BytesIO(self._raw_release_time))
            self.release_time = self._root.Time(io, self, self._root)
            self.duration = self._io.read_u4le()
            self.pulses_pstn = self._io.read_bytes(2)
            self.termination = self._root.Terminations(self._io.read_u1())
            self.diagnoistic = self._io.read_bytes(2)


    class Header(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.magic = self._io.ensure_fixed_contents(b"\x29\x00\x00")
            self.size = self._io.ensure_fixed_contents(b"\x08")
            self.type = self._io.ensure_fixed_contents(b"\x01\x00")
            self.length = self._io.read_u2le()
            self.exchange_id = self._io.read_bytes(10)
            self.first_record = self._io.read_u4le()
            self.batch_num = self._io.read_u4le()
            self.block_num = self._io.read_u2le()
            self.start_time = self._io.read_bytes(7)
            self.version = self._io.read_bytes(6)


    class Toc(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.type = self._root.Types(self._io.read_u1())
            self.version = self._io.read_u1()
            self._raw_dxt_id = self._io.read_bytes(4)
            io = KaitaiStream(BytesIO(self._raw_dxt_id))
            self.dxt_id = self._root.FourByteBcd(io, self, self._root)
            self.checksum = self._io.read_u2le()
            self.seq_num = self._io.read_u2le()
            self.unused = self._io.read_bytes(6)
            self.call_reference = self._io.read_u4le()
            self.served_number = self._io.read_bytes(10)
            self.served_nitsi = self._io.read_bytes(10)
            self.organization_block = self._io.read_bytes(12)
            self.called_number = self._io.read_bytes(14)
            self.translated_number = self._io.read_bytes(14)
            self.translated_nitsi = self._io.read_bytes(10)
            self.connected_number = self._io.read_bytes(14)
            self.connected_nitsi = self._io.read_bytes(10)
            self.connection_group = self._io.read_bytes(2)
            self._raw_connected_dxt = self._io.read_bytes(4)
            io = KaitaiStream(BytesIO(self._raw_connected_dxt))
            self.connected_dxt = self._root.FourByteBcd(io, self, self._root)
            self._raw_served_dxt = self._io.read_bytes(4)
            io = KaitaiStream(BytesIO(self._raw_served_dxt))
            self.served_dxt = self._root.FourByteBcd(io, self, self._root)
            self.location = self._io.read_u2le()
            self.cell_identity = self._io.read_bytes(1)
            self.basic_service_used = self._io.read_bytes(4)
            self.basic_servise_request = self._io.read_bytes(4)
            self.priority = self._io.read_bytes(1)
            self.urgency_class = self._io.read_bytes(1)
            self.queuing_priority = self._io.read_bytes(1)
            self.duplex = self._io.read_bytes(1)
            self.hook = self._io.read_bytes(1)
            self.encryption = self._io.read_bytes(1)
            self.members = self._io.read_u2le()
            self.allocations = self._io.read_bytes(2)
            self.channel_usage_time = self._io.read_bytes(4)
            self.number_of_groups = self._io.read_bytes(1)
            self.list_of_groups = self._io.read_bytes(80)
            self._raw_setup_time = self._io.read_bytes(8)
            io = KaitaiStream(BytesIO(self._raw_setup_time))
            self.setup_time = self._root.Time(io, self, self._root)
            self._raw_answer_time = self._io.read_bytes(8)
            io = KaitaiStream(BytesIO(self._raw_answer_time))
            self.answer_time = self._root.Time(io, self, self._root)
            self._raw_connected_time = self._io.read_bytes(8)
            io = KaitaiStream(BytesIO(self._raw_connected_time))
            self.connected_time = self._root.Time(io, self, self._root)
            self._raw_release_time = self._io.read_bytes(8)
            io = KaitaiStream(BytesIO(self._raw_release_time))
            self.release_time = self._root.Time(io, self, self._root)
            self.duration = self._io.read_u4le()
            self.termination = self._root.Terminations(self._io.read_u1())
            self.diagnostic = self._io.read_bytes(2)


    class Time(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.msec = Bcd(2, 4, False, self._io)
            self.sec = Bcd(2, 4, False, self._io)
            self.min = Bcd(2, 4, False, self._io)
            self.hour = Bcd(2, 4, False, self._io)
            self.day = Bcd(2, 4, False, self._io)
            self.month = Bcd(2, 4, False, self._io)
            self.year = Bcd(2, 4, False, self._io)
            self.age = Bcd(2, 4, False, self._io)

        @property
        def full_year(self):
            if hasattr(self, '_m_full_year'):
                return self._m_full_year if hasattr(self, '_m_full_year') else None

            self._m_full_year = ((self.age.as_int * 100) + self.year.as_int)
            return self._m_full_year if hasattr(self, '_m_full_year') else None


    class InG(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.type = self._root.Types(self._io.read_u1())
            self.version = self._io.read_u1()
            self._raw_dxt_id = self._io.read_bytes(4)
            io = KaitaiStream(BytesIO(self._raw_dxt_id))
            self.dxt_id = self._root.FourByteBcd(io, self, self._root)
            self.checksum = self._io.read_u2le()
            self.seq_num = self._io.read_u2le()
            self.call_reference = self._io.read_u4le()
            self.calling_number = self._io.read_bytes(14)
            self.called_number = self._io.read_bytes(10)
            self.translated_number = self._io.read_bytes(14)
            self.translated_ntsi = self._io.read_bytes(10)
            self._raw_served_dxt = self._io.read_bytes(4)
            io = KaitaiStream(BytesIO(self._raw_served_dxt))
            self.served_dxt = self._root.FourByteBcd(io, self, self._root)
            self._raw_in_int = self._io.read_bytes(6)
            io = KaitaiStream(BytesIO(self._raw_in_int))
            self.in_int = self._root.Interface(io, self, self._root)
            self.conn_group = self._io.read_u2le()
            self.pulse = self._io.read_u2le()
            self._raw_setup_time = self._io.read_bytes(8)
            io = KaitaiStream(BytesIO(self._raw_setup_time))
            self.setup_time = self._root.Time(io, self, self._root)
            self._raw_answer_time = self._io.read_bytes(8)
            io = KaitaiStream(BytesIO(self._raw_answer_time))
            self.answer_time = self._root.Time(io, self, self._root)
            self._raw_release_time = self._io.read_bytes(8)
            io = KaitaiStream(BytesIO(self._raw_release_time))
            self.release_time = self._root.Time(io, self, self._root)
            self.duration = self._io.read_u4le()
            self.termination = self._root.Terminations(self._io.read_u1())
            self.diagnoistic = self._io.read_bytes(2)


    class Tcc(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.type = self._root.Types(self._io.read_u1())
            self.version = self._io.read_bytes(1)
            self._raw_dxt_id = self._io.read_bytes(4)
            io = KaitaiStream(BytesIO(self._raw_dxt_id))
            self.dxt_id = self._root.FourByteBcd(io, self, self._root)
            self.checksum = self._io.read_bytes(2)
            self.seq_num = self._io.read_u2le()
            self.skeep = self._io.read_bytes(5)
            self.call_reference = self._io.read_u4le()
            self.served_number = self._io.read_bytes(10)
            self.served_nitsi = self._io.read_bytes(10)
            self.organisation_block = self._io.read_bytes(12)
            self.calling_number = self._io.read_bytes(14)
            self.calling_nitsi = self._io.read_bytes(10)
            self._raw_served_dxt = self._io.read_bytes(4)
            io = KaitaiStream(BytesIO(self._raw_served_dxt))
            self.served_dxt = self._root.FourByteBcd(io, self, self._root)
            self.location = self._io.read_u2le()
            self.call_identity = self._io.read_bytes(1)
            self.service = self._io.read_bytes(4)
            self.priority = self._io.read_bytes(1)
            self.urgency = self._io.read_bytes(1)
            self.queuie = self._io.read_bytes(1)
            self.duplex = self._io.read_bytes(1)
            self.hook = self._io.read_bytes(1)
            self.encription = self._io.read_bytes(1)
            self._raw_setup_time = self._io.read_bytes(8)
            io = KaitaiStream(BytesIO(self._raw_setup_time))
            self.setup_time = self._root.Time(io, self, self._root)
            self._raw_answer_time = self._io.read_bytes(8)
            io = KaitaiStream(BytesIO(self._raw_answer_time))
            self.answer_time = self._root.Time(io, self, self._root)
            self._raw_connected_time = self._io.read_bytes(8)
            io = KaitaiStream(BytesIO(self._raw_connected_time))
            self.connected_time = self._root.Time(io, self, self._root)
            self._raw_release_time = self._io.read_bytes(8)
            io = KaitaiStream(BytesIO(self._raw_release_time))
            self.release_time = self._root.Time(io, self, self._root)
            self.duration = self._io.read_u4le()
            self.termination = self._root.Terminations(self._io.read_u1())
            self.diagnoistic = self._io.read_bytes(2)


    class Events(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.event = []
            i = 0
            while not self._io.is_eof():
                self.event.append(self._root.Event(self._io, self, self._root))
                i += 1