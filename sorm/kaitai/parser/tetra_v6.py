# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO
from enum import Enum


if parse_version(kaitaistruct.__version__) < parse_version('0.9'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

from .bcd import Bcd
class Tetra(KaitaiStruct):
    """CDR Parser for Tetra switch software v7.0
    """

    class SdsReportFlag(Enum):
        message = 0
        report = 1
        status = 255

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

    class SdsServiceType(Enum):
        notack = 0
        ack = 1
        unknown = 255

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

    class SdsType(Enum):
        sds1 = 0
        sds2 = 1
        sds3 = 2
        sds4 = 3
        status = 4
        unknown = 255
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
            _io__raw_block = KaitaiStream(BytesIO(self._raw_block[-1]))
            self.block.append(Tetra.Block(_io__raw_block, self, self._root))
            i += 1


    class Reg(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.type = KaitaiStream.resolve_enum(Tetra.Types, self._io.read_u1())
            self.version = self._io.read_u1()
            self._raw_dxt = self._io.read_bytes(4)
            _io__raw_dxt = KaitaiStream(BytesIO(self._raw_dxt))
            self.dxt = Tetra.ForByteBcd(_io__raw_dxt, self, self._root)
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
            _io__raw_dxt_id = KaitaiStream(BytesIO(self._raw_dxt_id))
            self.dxt_id = Tetra.ForByteBcd(_io__raw_dxt_id, self, self._root)
            self._raw_prev_dxt_id = self._io.read_bytes(4)
            _io__raw_prev_dxt_id = KaitaiStream(BytesIO(self._raw_prev_dxt_id))
            self.prev_dxt_id = Tetra.ForByteBcd(_io__raw_prev_dxt_id, self, self._root)
            self.location = self._io.read_u2le()
            self.prev_location = self._io.read_u2le()
            self.cell = self._io.read_bytes(1)
            self._raw_timestamp = self._io.read_bytes(8)
            _io__raw_timestamp = KaitaiStream(BytesIO(self._raw_timestamp))
            self.timestamp = Tetra.Time(_io__raw_timestamp, self, self._root)
            self.accept = self._io.read_bytes(1)
            self.reject = self._io.read_bytes(1)
            self.diagnostic = self._io.read_bytes(2)


    class Event(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.len_rec = self._io.read_u2le()
            _on = self.len_rec
            if _on == 141:
                self._raw_body = self._io.read_bytes((self.len_rec - 2))
                _io__raw_body = KaitaiStream(BytesIO(self._raw_body))
                self.body = Tetra.Pd(_io__raw_body, self, self._root)
            elif _on == 113:
                self._raw_body = self._io.read_bytes((self.len_rec - 2))
                _io__raw_body = KaitaiStream(BytesIO(self._raw_body))
                self.body = Tetra.InG(_io__raw_body, self, self._root)
            elif _on == 262:
                self._raw_body = self._io.read_bytes((self.len_rec - 2))
                _io__raw_body = KaitaiStream(BytesIO(self._raw_body))
                self.body = Tetra.Sds(_io__raw_body, self, self._root)
            elif _on == 99:
                self._raw_body = self._io.read_bytes((self.len_rec - 2))
                _io__raw_body = KaitaiStream(BytesIO(self._raw_body))
                self.body = Tetra.OutG(_io__raw_body, self, self._root)
            elif _on == 125:
                self._raw_body = self._io.read_bytes((self.len_rec - 2))
                _io__raw_body = KaitaiStream(BytesIO(self._raw_body))
                self.body = Tetra.Fraw(_io__raw_body, self, self._root)
            elif _on == 94:
                self._raw_body = self._io.read_bytes((self.len_rec - 2))
                _io__raw_body = KaitaiStream(BytesIO(self._raw_body))
                self.body = Tetra.Reg(_io__raw_body, self, self._root)
            elif _on == 271:
                self._raw_body = self._io.read_bytes((self.len_rec - 2))
                _io__raw_body = KaitaiStream(BytesIO(self._raw_body))
                self.body = Tetra.Toc(_io__raw_body, self, self._root)
            elif _on == 133:
                self._raw_body = self._io.read_bytes((self.len_rec - 2))
                _io__raw_body = KaitaiStream(BytesIO(self._raw_body))
                self.body = Tetra.Tcc(_io__raw_body, self, self._root)
            else:
                self.body = self._io.read_bytes((self.len_rec - 2))


    class Interface(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.ui = KaitaiStream.resolve_enum(Tetra.UnitIndexT, self._io.read_u1())
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
            self.type = KaitaiStream.resolve_enum(Tetra.Types, self._io.read_u1())
            self.version = self._io.read_u1()
            self.dxt_id = Tetra.ForByteBcd(self._io, self, self._root)
            self.checksum = self._io.read_u2le()
            self.seq_num = self._io.read_u2le()
            self.nm_of_ss = self._io.read_u1()
            self.call_reference = self._io.read_u4le()
            self.served_number = self._io.read_bytes(10)
            self.served_nitsi = self._io.read_bytes(10)
            self.organisation_block = self._io.read_bytes(12)
            self.calling_number = self._io.read_bytes(14)
            self.translated_number = self._io.read_bytes(14)
            self.translated_nitsi = self._io.read_bytes(10)
            self.connected_number = self._io.read_bytes(14)
            self.connected_nitsi = self._io.read_bytes(10)
            self.connection_group = self._io.read_bytes(2)
            self._raw_connected_dxt = self._io.read_bytes(4)
            _io__raw_connected_dxt = KaitaiStream(BytesIO(self._raw_connected_dxt))
            self.connected_dxt = Tetra.ForByteBcd(_io__raw_connected_dxt, self, self._root)
            self.location = self._io.read_u2le()
            self.cell_identity = self._io.read_bytes(1)
            self._raw_target_dxt = self._io.read_bytes(4)
            _io__raw_target_dxt = KaitaiStream(BytesIO(self._raw_target_dxt))
            self.target_dxt = Tetra.ForByteBcd(_io__raw_target_dxt, self, self._root)
            self.targget_location = self._io.read_u2le()
            self.targget_ch_type = self._io.read_u2le()
            self.sds_tl_protocol = self._io.read_u1()
            self.forward_number = self._io.read_bytes(14)
            self.translated_forward_number = self._io.read_bytes(13)
            self.report_flag = KaitaiStream.resolve_enum(Tetra.SdsReportFlag, self._io.read_u1())
            self.message_reference = self._io.read_u1()
            self.service_type = KaitaiStream.resolve_enum(Tetra.SdsServiceType, self._io.read_u1())
            self.sds_type = KaitaiStream.resolve_enum(Tetra.SdsType, self._io.read_u1())
            self.length = self._io.read_u4le()
            self.sending_profile = self._io.read_u1()
            self.num_of_groups = self._io.read_u1()
            self.list_of_groups = self._io.read_bytes(80)
            self._raw_time_stamp = self._io.read_bytes(8)
            _io__raw_time_stamp = KaitaiStream(BytesIO(self._raw_time_stamp))
            self.time_stamp = Tetra.Time(_io__raw_time_stamp, self, self._root)
            self.cells_distr = self._io.read_u2le()
            self.cells_reached = self._io.read_u2le()
            self.dispatchers_reached = self._io.read_u1()
            self.result_sds = self._io.read_u1()
            self.diagnostics = self._io.read_u2le()


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
            self.header = Tetra.Header(self._io, self, self._root)
            self._raw_events = self._io.read_bytes((self.header.length - 65))
            _io__raw_events = KaitaiStream(BytesIO(self._raw_events))
            self.events = Tetra.Events(_io__raw_events, self, self._root)
            self.trailer = Tetra.Trailer(self._io, self, self._root)


    class Pd(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.body = self._io.read_bytes((141 - 2))


    class Trailer(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.body = self._io.read_bytes(24)


    class ForByteBcd(KaitaiStruct):
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


    class OutG(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.type = KaitaiStream.resolve_enum(Tetra.Types, self._io.read_u1())
            self.version = self._io.read_u1()
            self._raw_dxt_id = self._io.read_bytes(4)
            _io__raw_dxt_id = KaitaiStream(BytesIO(self._raw_dxt_id))
            self.dxt_id = Tetra.ForByteBcd(_io__raw_dxt_id, self, self._root)
            self.checksum = self._io.read_u2le()
            self.seq_num = self._io.read_u2le()
            self.call_reference = self._io.read_u4le()
            self.calling_number = self._io.read_bytes(10)
            self.calling_ntsi = self._io.read_bytes(10)
            self.transmitted_number = self._io.read_bytes(14)
            self._raw_served_dxt = self._io.read_bytes(4)
            _io__raw_served_dxt = KaitaiStream(BytesIO(self._raw_served_dxt))
            self.served_dxt = Tetra.ForByteBcd(_io__raw_served_dxt, self, self._root)
            self._raw_out_int = self._io.read_bytes(6)
            _io__raw_out_int = KaitaiStream(BytesIO(self._raw_out_int))
            self.out_int = Tetra.Interface(_io__raw_out_int, self, self._root)
            self.conn_group = self._io.read_bytes(2)
            self.mni = self._io.read_bytes(4)
            self._raw_setup_time = self._io.read_bytes(8)
            _io__raw_setup_time = KaitaiStream(BytesIO(self._raw_setup_time))
            self.setup_time = Tetra.Time(_io__raw_setup_time, self, self._root)
            self._raw_answer_time = self._io.read_bytes(8)
            _io__raw_answer_time = KaitaiStream(BytesIO(self._raw_answer_time))
            self.answer_time = Tetra.Time(_io__raw_answer_time, self, self._root)
            self._raw_release_time = self._io.read_bytes(8)
            _io__raw_release_time = KaitaiStream(BytesIO(self._raw_release_time))
            self.release_time = Tetra.Time(_io__raw_release_time, self, self._root)
            self.duration = self._io.read_u4le()
            self.pulses_pstn = self._io.read_bytes(2)
            self.termination = KaitaiStream.resolve_enum(Tetra.Terminations, self._io.read_u1())
            self.diagnoistic = self._io.read_bytes(2)


    class Header(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.magic = self._io.read_bytes(3)
            if not self.magic == b"\x29\x00\x00":
                raise kaitaistruct.ValidationNotEqualError(b"\x29\x00\x00", self.magic, self._io, u"/types/header/seq/0")
            self.size = self._io.read_bytes(1)
            if not self.size == b"\x08":
                raise kaitaistruct.ValidationNotEqualError(b"\x08", self.size, self._io, u"/types/header/seq/1")
            self.type = self._io.read_bytes(2)
            if not self.type == b"\x01\x00":
                raise kaitaistruct.ValidationNotEqualError(b"\x01\x00", self.type, self._io, u"/types/header/seq/2")
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
            self.type = KaitaiStream.resolve_enum(Tetra.Types, self._io.read_u1())
            self.version = self._io.read_u1()
            self._raw_dxt_id = self._io.read_bytes(4)
            _io__raw_dxt_id = KaitaiStream(BytesIO(self._raw_dxt_id))
            self.dxt_id = Tetra.ForByteBcd(_io__raw_dxt_id, self, self._root)
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
            _io__raw_connected_dxt = KaitaiStream(BytesIO(self._raw_connected_dxt))
            self.connected_dxt = Tetra.ForByteBcd(_io__raw_connected_dxt, self, self._root)
            self._raw_served_dxt = self._io.read_bytes(4)
            _io__raw_served_dxt = KaitaiStream(BytesIO(self._raw_served_dxt))
            self.served_dxt = Tetra.ForByteBcd(_io__raw_served_dxt, self, self._root)
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
            _io__raw_setup_time = KaitaiStream(BytesIO(self._raw_setup_time))
            self.setup_time = Tetra.Time(_io__raw_setup_time, self, self._root)
            self._raw_answer_time = self._io.read_bytes(8)
            _io__raw_answer_time = KaitaiStream(BytesIO(self._raw_answer_time))
            self.answer_time = Tetra.Time(_io__raw_answer_time, self, self._root)
            self._raw_connected_time = self._io.read_bytes(8)
            _io__raw_connected_time = KaitaiStream(BytesIO(self._raw_connected_time))
            self.connected_time = Tetra.Time(_io__raw_connected_time, self, self._root)
            self._raw_release_time = self._io.read_bytes(8)
            _io__raw_release_time = KaitaiStream(BytesIO(self._raw_release_time))
            self.release_time = Tetra.Time(_io__raw_release_time, self, self._root)
            self.duration = self._io.read_u4le()
            self.termination = KaitaiStream.resolve_enum(Tetra.Terminations, self._io.read_u1())
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
            self.type = KaitaiStream.resolve_enum(Tetra.Types, self._io.read_u1())
            self.version = self._io.read_u1()
            self._raw_dxt_id = self._io.read_bytes(4)
            _io__raw_dxt_id = KaitaiStream(BytesIO(self._raw_dxt_id))
            self.dxt_id = Tetra.ForByteBcd(_io__raw_dxt_id, self, self._root)
            self.checksum = self._io.read_u2le()
            self.seq_num = self._io.read_u2le()
            self.call_reference = self._io.read_u4le()
            self.calling_number = self._io.read_bytes(14)
            self.called_number = self._io.read_bytes(10)
            self.translated_number = self._io.read_bytes(14)
            self.translated_ntsi = self._io.read_bytes(10)
            self._raw_served_dxt = self._io.read_bytes(4)
            _io__raw_served_dxt = KaitaiStream(BytesIO(self._raw_served_dxt))
            self.served_dxt = Tetra.ForByteBcd(_io__raw_served_dxt, self, self._root)
            self._raw_in_int = self._io.read_bytes(6)
            _io__raw_in_int = KaitaiStream(BytesIO(self._raw_in_int))
            self.in_int = Tetra.Interface(_io__raw_in_int, self, self._root)
            self.conn_group = self._io.read_u2le()
            self.mni = self._io.read_u4le()
            self.pulse = self._io.read_u2le()
            self._raw_setup_time = self._io.read_bytes(8)
            _io__raw_setup_time = KaitaiStream(BytesIO(self._raw_setup_time))
            self.setup_time = Tetra.Time(_io__raw_setup_time, self, self._root)
            self._raw_answer_time = self._io.read_bytes(8)
            _io__raw_answer_time = KaitaiStream(BytesIO(self._raw_answer_time))
            self.answer_time = Tetra.Time(_io__raw_answer_time, self, self._root)
            self._raw_release_time = self._io.read_bytes(8)
            _io__raw_release_time = KaitaiStream(BytesIO(self._raw_release_time))
            self.release_time = Tetra.Time(_io__raw_release_time, self, self._root)
            self.duration = self._io.read_u4le()
            self.termination = KaitaiStream.resolve_enum(Tetra.Terminations, self._io.read_u1())
            self.diagnoistic = self._io.read_bytes(2)


    class Tcc(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.type = KaitaiStream.resolve_enum(Tetra.Types, self._io.read_u1())
            self.version = self._io.read_bytes(1)
            self._raw_dxt_id = self._io.read_bytes(4)
            _io__raw_dxt_id = KaitaiStream(BytesIO(self._raw_dxt_id))
            self.dxt_id = Tetra.ForByteBcd(_io__raw_dxt_id, self, self._root)
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
            _io__raw_served_dxt = KaitaiStream(BytesIO(self._raw_served_dxt))
            self.served_dxt = Tetra.ForByteBcd(_io__raw_served_dxt, self, self._root)
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
            _io__raw_setup_time = KaitaiStream(BytesIO(self._raw_setup_time))
            self.setup_time = Tetra.Time(_io__raw_setup_time, self, self._root)
            self._raw_answer_time = self._io.read_bytes(8)
            _io__raw_answer_time = KaitaiStream(BytesIO(self._raw_answer_time))
            self.answer_time = Tetra.Time(_io__raw_answer_time, self, self._root)
            self._raw_connected_time = self._io.read_bytes(8)
            _io__raw_connected_time = KaitaiStream(BytesIO(self._raw_connected_time))
            self.connected_time = Tetra.Time(_io__raw_connected_time, self, self._root)
            self._raw_release_time = self._io.read_bytes(8)
            _io__raw_release_time = KaitaiStream(BytesIO(self._raw_release_time))
            self.release_time = Tetra.Time(_io__raw_release_time, self, self._root)
            self.duration = self._io.read_u4le()
            self.termination = KaitaiStream.resolve_enum(Tetra.Terminations, self._io.read_u1())
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
                self.event.append(Tetra.Event(self._io, self, self._root))
                i += 1




