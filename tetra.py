# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
from kaitaistruct import __version__ as ks_version, KaitaiStruct, KaitaiStream, BytesIO
from enum import Enum


if parse_version(ks_version) < parse_version('0.7'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.7 or later is required, but you have %s" % (ks_version))

from bcd import Bcd
class Tetra(KaitaiStruct):

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
        redirect = 5
        sms = 6
        farward = 7
        data = 8
        reg = 9
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


    class E(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.body = self._io.read_bytes((262 - 2))


    class Reg(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.type = self._root.Types(self._io.read_u1())
            self.version = self._io.read_u1()
            self.dxt = self._io.read_u4le()
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
            self.subscriber_class = self._io.read_bytes(4)
            self.dxt_id = self._io.read_bytes(4)
            self.location = self._io.read_u2le()
            self.prev_location = self._io.read_u2le()
            self.cell = self._io.read_bytes(1)
            self.channel = self._io.read_bytes(1)
            self.laja = self._io.read_bytes(2)
            self._raw_timestamp = self._io.read_bytes(8)
            io = KaitaiStream(BytesIO(self._raw_timestamp))
            self.timestamp = self._root.Time(io, self, self._root)
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
                io = KaitaiStream(BytesIO(self._raw_body))
                self.body = self._root.F(io, self, self._root)
            elif _on == 113:
                self._raw_body = self._io.read_bytes((self.len_rec - 2))
                io = KaitaiStream(BytesIO(self._raw_body))
                self.body = self._root.InG(io, self, self._root)
            elif _on == 97:
                self._raw_body = self._io.read_bytes((self.len_rec - 2))
                io = KaitaiStream(BytesIO(self._raw_body))
                self.body = self._root.Reg(io, self, self._root)
            elif _on == 262:
                self._raw_body = self._io.read_bytes((self.len_rec - 2))
                io = KaitaiStream(BytesIO(self._raw_body))
                self.body = self._root.E(io, self, self._root)
            elif _on == 99:
                self._raw_body = self._io.read_bytes((self.len_rec - 2))
                io = KaitaiStream(BytesIO(self._raw_body))
                self.body = self._root.OutC(io, self, self._root)
            elif _on == 125:
                self._raw_body = self._io.read_bytes((self.len_rec - 2))
                io = KaitaiStream(BytesIO(self._raw_body))
                self.body = self._root.D(io, self, self._root)
            elif _on == 271:
                self._raw_body = self._io.read_bytes((self.len_rec - 2))
                io = KaitaiStream(BytesIO(self._raw_body))
                self.body = self._root.Toc(io, self, self._root)
            elif _on == 133:
                self._raw_body = self._io.read_bytes((self.len_rec - 2))
                io = KaitaiStream(BytesIO(self._raw_body))
                self.body = self._root.Tcc(io, self, self._root)
            else:
                self.body = self._io.read_bytes((self.len_rec - 2))

/Reg

    class F(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.body = self._io.read_bytes((141 - 2))


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


    class OutC(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.type = self._root.Types(self._io.read_u1())
            self.version = self._io.read_u1()
            self.identity = self._io.read_u4le()
            self.checksum = self._io.read_u2le()
            self.seq_number = self._io.read_u2le()
            self.call_reference = self._io.read_u4le()
            self.calling_number = self._io.read_bytes(10)
            self.calling_ntsi = self._io.read_bytes(10)
            self.transmitted_number = self._io.read_bytes(14)
            self.dxt = self._io.read_bytes(4)
            self.out_int = self._io.read_bytes(6)
            self.conn_group = self._io.read_bytes(2)
            self.mni = self._io.read_bytes(4)
            self._raw_event_time1 = self._io.read_bytes(8)
            io = KaitaiStream(BytesIO(self._raw_event_time1))
            self.event_time1 = self._root.Time(io, self, self._root)
            self._raw_event_time2 = self._io.read_bytes(8)
            io = KaitaiStream(BytesIO(self._raw_event_time2))
            self.event_time2 = self._root.Time(io, self, self._root)
            self._raw_event_time3 = self._io.read_bytes(8)
            io = KaitaiStream(BytesIO(self._raw_event_time3))
            self.event_time3 = self._root.Time(io, self, self._root)


    class Trailer(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.body = self._io.read_bytes(24)


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
            self.dxt_id = self._io.read_bytes(4)
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
            self.connected_dxt = self._io.read_bytes(4)
            self.served_dxt = self._io.read_bytes(4)
            self.location_area = self._io.read_bytes(2)
            self.cell_identity = self._io.read_bytes(1)
            self.basic_service_used = self._io.read_bytes(4)
            self.basic_servise_request = self._io.read_bytes(4)
            self.priority = self._io.read_bytes(1)
            self.urgency_class = self._io.read_bytes(1)
            self.queuing_priority = self._io.read_bytes(1)
            self.duplex = self._io.read_bytes(1)
            self.hook = self._io.read_bytes(1)
            self.encryption = self._io.read_bytes(1)
            self.members = self._io.read_bytes(2)
            self.allocations = self._io.read_bytes(2)
            self.channel_usage_time = self._io.read_bytes(4)
            self.number_of_groups = self._io.read_bytes(1)
            self.list_of_groups = self._io.read_bytes(80)
            self._raw_event_time_stamps1 = self._io.read_bytes(8)
            io = KaitaiStream(BytesIO(self._raw_event_time_stamps1))
            self.event_time_stamps1 = self._root.Time(io, self, self._root)
            self._raw_event_time_stamps2 = self._io.read_bytes(8)
            io = KaitaiStream(BytesIO(self._raw_event_time_stamps2))
            self.event_time_stamps2 = self._root.Time(io, self, self._root)
            self._raw_event_time_stamps3 = self._io.read_bytes(8)
            io = KaitaiStream(BytesIO(self._raw_event_time_stamps3))
            self.event_time_stamps3 = self._root.Time(io, self, self._root)
            self._raw_event_time_stamps4 = self._io.read_bytes(8)
            io = KaitaiStream(BytesIO(self._raw_event_time_stamps4))
            self.event_time_stamps4 = self._root.Time(io, self, self._root)
            self.duration = self._io.read_u4le()
            self.termination = self._root.Terminations(self._io.read_u1())
            self.diagnostic = self._io.read_bytes(2)


    class H(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.body = self._io.read_bytes((271 - 2))


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
            self.dxt1 = self._io.read_u4le()
            self.checksum = self._io.read_u2le()
            self.seq_number = self._io.read_u2le()
            self.call_reference = self._io.read_u4le()
            self.calling_number = self._io.read_bytes(14)
            self.called_number = self._io.read_bytes(10)
            self.translated_number = self._io.read_bytes(14)
            self.translated_ntsi = self._io.read_bytes(10)
            self.dxt = self._io.read_u4le()
            self.inc_int = self._io.read_bytes(6)
            self.conn_group = self._io.read_u2le()
            self.mni = self._io.read_u4le()
            self.pulse = self._io.read_u2le()


    class Tcc(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.type = self._root.Types(self._io.read_u1())
            self.version = self._io.read_bytes(1)
            self.dxt = self._io.read_bytes(4)
            self.checksum = self._io.read_bytes(2)
            self.seq_num = self._io.read_bytes(2)
            self.skeep = self._io.read_bytes(5)
            self.call_reference = self._io.read_u4le()
            self.served_number = self._io.read_bytes(10)
            self.served_nitsi = self._io.read_bytes(10)
            self.organisation_block = self._io.read_bytes(12)
            self.calling_number = self._io.read_bytes(14)
            self.calling_nitsi = self._io.read_bytes(10)
            self.dxt_id = self._io.read_bytes(4)
            self.location = self._io.read_bytes(2)
            self.call_identity = self._io.read_bytes(1)
            self.service = self._io.read_bytes(4)
            self.priority = self._io.read_bytes(1)
            self.urgency = self._io.read_bytes(1)
            self.queuie = self._io.read_bytes(1)
            self.duplex = self._io.read_bytes(1)
            self.hook = self._io.read_bytes(1)
            self.encription = self._io.read_bytes(1)
            self._raw_timestamp1 = self._io.read_bytes(8)
            io = KaitaiStream(BytesIO(self._raw_timestamp1))
            self.timestamp1 = self._root.Time(io, self, self._root)
            self._raw_timestamp2 = self._io.read_bytes(8)
            io = KaitaiStream(BytesIO(self._raw_timestamp2))
            self.timestamp2 = self._root.Time(io, self, self._root)
            self._raw_timestamp3 = self._io.read_bytes(8)
            io = KaitaiStream(BytesIO(self._raw_timestamp3))
            self.timestamp3 = self._root.Time(io, self, self._root)
            self._raw_timestamp4 = self._io.read_bytes(8)
            io = KaitaiStream(BytesIO(self._raw_timestamp4))
            self.timestamp4 = self._root.Time(io, self, self._root)
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



    class D(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.body = self._io.read_bytes((125 - 2))



