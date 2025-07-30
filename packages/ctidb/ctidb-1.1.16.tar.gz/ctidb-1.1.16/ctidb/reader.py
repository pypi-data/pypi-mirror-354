"""
ctidb.reader

This module contains the pure Python database reader and related classes.

"""
import os
import time
import hashlib
import json

try:
    import mmap
except ImportError:
    # pylint: disable=invalid-name
    mmap = None  # type: ignore

import ipaddress
import struct
from typing import AnyStr, Any, Optional, Tuple, Union, List, Dict, cast

from .custom import Record, InvalidDatabaseError
from .decoder import Decoder

MODE_AUTO = 0
MODE_MMAP = 2
MODE_MEMORY = 8


# =======================================================================================
# CCtiReader
# =======================================================================================
class CCtiReader:
    """
    Instances of this class provide a reader for the cti DB format. IP
    addresses can be looked up using the ``get`` method.
    """

    _DATA_SECTION_SEPARATOR_SIZE = 16
    _METADATA_START_MARKER = b"\x44\x48\x43AISpera.com"
    _LANGDATA_START_MARKER = b"\x44\x48\x43ALIASNpGera.com"

    _buffer: mmap.mmap
    _ipv4_start: Optional[int] = None

    def __init__(
        self, database: str,
        mode: int = MODE_AUTO
    ) -> None:
        """Reader for the cti DB file format

        Arguments:
        database -- A path to a valid cti DB file such as a GeoIP2 database file.
        mode -- mode to open the database with. Valid mode are:
            * MODE_MEMORY - load database into memory.
            * MODE_AUTO - tries MODE_MMAP and then MODE_FILE. Default.
        """

        if not os.path.exists(database):
            raise InvalidDatabaseError(
                f"Error finding database file ({database}).")
        
        if (mode == MODE_AUTO and mmap) or mode == MODE_MMAP:
            with open(database, "rb") as db_file:  # type: ignore
                self._buffer = mmap.mmap(db_file.fileno(), 0, access=mmap.ACCESS_READ)
                self._buffer_size = self._buffer.size()
        elif mode in (MODE_AUTO, MODE_MEMORY):
            with open(database, "rb") as db_file:  # type: ignore
                self._buffer = db_file.read()
                self._buffer_size = len(self._buffer)
        else:
            raise ValueError(
                f"Unsupported open mode ({mode}). Only MODE_AUTO, "
                "MODE_MEMORY are supported by the pure Python Reader")

        filename = database
        metadata_start = self._buffer.rfind(
            self._METADATA_START_MARKER, 0, len(self._buffer)
        )
        if metadata_start == -1:
            self.close()
            raise InvalidDatabaseError(
                f"Error opening database file ({filename}). "
                "Is this a valid cti DB file?")

        metadata_start += len(self._METADATA_START_MARKER)
        metadata_decoder = Decoder(self._buffer, metadata_start)
        (metadata, _) = metadata_decoder.decode(metadata_start)
        if not isinstance(metadata, dict):
            raise InvalidDatabaseError(
                f"Error reading metadata in database file ({filename})."
            )

        build_epoch = metadata.get('build_epoch') if isinstance(metadata.get('build_epoch'), int) else 0
        build_epoch_limit = metadata.get('build_epoch_limit') if isinstance(metadata.get('build_epoch_limit'), int) else 0
        # if 0 != build_epoch_limit:
        #     if 0 == build_epoch + build_epoch_limit or time.time() > build_epoch + build_epoch_limit:
        #         raise InvalidDatabaseError(
        #             f"Error reading metadata in database file ({filename})."
        #         )

            # tmp_buffer_md5 = hashlib.md5(self._buffer[:metadata_start]).hexdigest()
            # if metadata.get('license')[:32] != tmp_buffer_md5.encode('utf8'):
            #     raise InvalidDatabaseError(
            #         f"Error reading metadata in database file ({filename})."
            #     )

        self._metadata = Metadata(**metadata)  # pylint: disable=bad-option-value

        langdata_start = self._buffer.rfind(
            self._LANGDATA_START_MARKER,
            0,
            self._buffer_size
        )
        self._metadata_lange = None
        self._metadata_cache = dict()
        self._metadata_cache_tmp = dict()
        if -1 != langdata_start:
            self._metadata_lange_tmp = json.loads(self._buffer[langdata_start + len(self._LANGDATA_START_MARKER):])
            self._metadata_lange = dict(zip(self._metadata_lange_tmp.values(),self._metadata_lange_tmp.keys()))
            self._metadata_lange_tmp.clear()

        self._decoder = Decoder(
            self._buffer,
            self._metadata.search_tree_size + self._DATA_SECTION_SEPARATOR_SIZE,
        )

        tmp_description = self._metadata.description.get('description', '')
        if 'SecOps License' in tmp_description:
            self._license = 5
        elif 'Full CTI License' in tmp_description:
            self._license = 4
        elif 'Fraud Detection License' in tmp_description:
            self._license = 3
        elif 'TI_C2 License' in tmp_description:
            self._license = 2
        else:
            self._license = 1
        self.closed = False

    def metadata(self) -> "Metadata":
        """Return the metadata associated with the cti DB file"""
        return self._metadata

    def get_license_info(self):
        alias = ""
        build_epoch = 0
        build_epoch_limit = 0
        t_result = dict()
        try:
            alias = self._metadata.alias

            create_date = ""
            # build_epoch = int(self._metadata.build_epoch)
            # if 0 != build_epoch:
            #     gt = time.gmtime(build_epoch)
            #     create_date = time.strftime("%Y.%m.%d", gt)

            expire_date = ""
            # build_epoch_limit = int(self._metadata.build_epoch_limit)
            # if 0 != build_epoch_limit:
            #     gt = time.gmtime(build_epoch + build_epoch_limit)
            #     expire_date = time.strftime("%Y.%m.%d", gt)

            tmp_license_name = ''
            tmp_description = self._metadata.description.get('description', '')
            if 0 != len(tmp_description):
                tmp_description = json.loads(tmp_description)
                tmp_product = tmp_description.get('product', 'CriminalIP CTIDB v1.0')
                tmp_license_name = 'Full CTI License' if 'Plan D' == tmp_description.get('license_name', '') else tmp_description.get('license_name', '')
                tmp_latest_ctidb = tmp_description.get('latest_ctidb', '20000101')
                tmp_expire_dtime = tmp_description.get('expire_dtime', '2000-01-01')

                create_date = "{}.{}.{}".format(tmp_latest_ctidb[:4], tmp_latest_ctidb[4:6], tmp_latest_ctidb[6:])
                expire_date = "{}.{}.{}".format(tmp_expire_dtime[:4], tmp_expire_dtime[5:7], tmp_expire_dtime[8:10])

            t_result['product'] = tmp_product
            t_result['customer'] = str(alias)
            t_result['license'] = tmp_license_name
            t_result['create_date'] = create_date
            t_result['expire_date'] = expire_date

        except AttributeError:
            raise InvalidDatabaseError(f"Error reading metadata in database file.")
        except Exception as ex:
            raise InvalidDatabaseError(f"Error reading metadata in database file.")
        return t_result

    def get(self, ip_address: str) -> Optional[Record]:
        """Return the record for the ip_address in the cti DB

        Arguments:
        ip_address -- an IP address in the standard string notation
        """
        if not isinstance(ip_address, str):
            raise TypeError("argument 1 must be a string")

        try:
            address = ipaddress.ip_address(ip_address)
            packed_address = bytearray(address.packed)
        except AttributeError as ex:
            raise TypeError("argument 1 must be a string or ipaddress object") from ex
        if address.version == 6 and self._metadata.ip_version == 4:
            raise ValueError(
                f"Error looking up {ip_address}. You attempted to look up "
                "an IPv6 address in an IPv4-only database.")

        (pointer, prefix_len) = self._find_address_in_tree(packed_address)
        if not pointer:
            return None

        return self._resolve_data_pointer(pointer)

    def _find_address_in_tree(self, packed: bytearray) -> Tuple[int, int]:
        bit_count = len(packed) * 8
        node = self._start_node(bit_count)
        node_count = self._metadata.node_count

        i = 0
        while i < bit_count and node < node_count:
            bit = 1 & (packed[i >> 3] >> 7 - (i % 8))
            node = self._read_node(node, bit)
            i = i + 1

        if node == node_count:
            # Record is empty
            return 0, i
        if node > node_count:
            return node, i

        raise InvalidDatabaseError("Invalid node in search tree")

    def _start_node(self, length: int) -> int:
        if self._metadata.ip_version != 6 or length == 128:
            return 0

        # We are looking up an IPv4 address in an IPv6 tree. Skip over the
        # first 96 nodes.
        if self._ipv4_start:
            return self._ipv4_start

        node = 0
        for _ in range(96):
            if node >= self._metadata.node_count:
                break
            node = self._read_node(node, 0)
        self._ipv4_start = node
        return node

    def _read_node(self, node_number: int, index: int) -> int:
        base_offset = node_number * self._metadata.node_byte_size

        record_size = self._metadata.record_size
        if record_size == 24:
            offset = base_offset + index * 3
            node_bytes = b"\x00" + self._buffer[offset : offset + 3]
        elif record_size == 28:
            offset = base_offset + 3 * index
            node_bytes = bytearray(self._buffer[offset : offset + 4])
            if index:
                node_bytes[0] = 0x0F & node_bytes[0]
            else:
                middle = (0xF0 & node_bytes.pop()) >> 4
                node_bytes.insert(0, middle)
        elif record_size == 32:
            offset = base_offset + index * 4
            node_bytes = self._buffer[offset : offset + 4]
        else:
            raise InvalidDatabaseError(f"Unknown record size: {record_size}")
        return struct.unpack(b"!I", node_bytes)[0]

    def _resolve_data_pointer(self, pointer: int) -> Record:
        resolved = pointer - self._metadata.node_count + self._metadata.search_tree_size

        if resolved >= self._buffer_size:
            raise InvalidDatabaseError("The cti DB file's search tree is corrupt")

        (data, _) = self._decoder.decode(resolved)

        t_result = dict()
        if None is not self._metadata_lange:
            fild = {1: 'country',
                    2: 'country_code',
                    3: 'as_name',
                    4: 'score',
                    5: 'hostname',
                    6: 'representative_domain',
                    7: 'ssl_certificate',
                    8: 'products',
                    9: 'cve',
                    10: 'open_ports',
                    11: 'tags',
                    12: 'abuse_record',
                    13: 'botnet',  # honeypot
                    14: 'connected_domains',
                    15: 'etcs',
                    16: 'C2'}
            for item in data.keys():
                idx = data[item]

                # True / False
                if item in [12, 13, 14, 9, 16, 4]:
                    t_result[fild[item] if item in fild else item] = True if 0 != idx else False
                    continue

                # value
                # if item in [4]:
                #     t_result[fild[item] if item in fild else item] = idx
                #     continue

                # skip
                if item in [5, 6]:
                    continue
                    
                if 0 == idx:
                    continue

                try:
                    if idx in self._metadata_cache:
                        value = self._metadata_cache[idx]
                    else:
                        if idx not in self._metadata_cache_tmp:
                            self._metadata_cache_tmp[idx] = 0
                        self._metadata_cache_tmp[idx] = self._metadata_cache_tmp[idx] + 1

                        value = [self._metadata_lange.get(idx)]
                        if 3 <= self._metadata_cache_tmp[idx]:
                            self._metadata_cache[idx] = value
                            del self._metadata_cache_tmp[idx]

                        if 100 <= len(self._metadata_cache_tmp):
                            self._metadata_cache_tmp.clear()

                    t_result[fild[item] if item in fild else item] = \
                        json.loads(value[0]) if 0 != len(value[0]) and value[0][0] in ['[', '{'] else value[0]
                except Exception as ex:
                    print(str(ex))
                    
            # etc
            if None is not t_result.get('abuse_record'):
                if 0 != len(t_result.get('ssl_certificate', list())):
                    t_result['connected_domains'] = True
                if True is t_result.get('botnet', False):
                    t_result['abuse_record'] = True
            if None is not t_result.get('etcs'):
                if True is t_result.get('abuse_record', False) and True is t_result.get('etcs').get('is_mobile', False):
                    t_result['mobile_botnet'] = True
                else:
                    t_result['mobile_botnet'] = False
            if 1 == len(data):
                if 1 <= self._license:
                    t_result['as_name'] = str()
                    t_result['ssl_certificate'] = list()
                if 2 <= self._license:
                    t_result['score'] = False
                    t_result['abuse_record'] = False
                    t_result['botnet'] = False
                    t_result['connected_domains'] = False
                    t_result['C2'] = False
                if 3 <= self._license:
                    t_result['mobile_botnet'] = False
                    t_result['etcs'] = dict()
                    t_result['etcs']['is_tor'] = False
                    t_result['etcs']['is_cdn'] = False
                    t_result['etcs']['is_vpn'] = False
                    t_result['etcs']['is_proxy'] = False
                    t_result['etcs']['is_hosting'] = False
                    t_result['etcs']['is_cloud'] = False
                    t_result['etcs']['is_mobile'] = False
                if 4 <= self._license:
                    t_result['products'] = list()
                    t_result['cve'] = False
                    t_result['open_ports'] = list()
                    t_result['tags'] = list()
                if 5 == self._license:
                    if 'ssl_certificate' in t_result:  del t_result['ssl_certificate']
                    if 'products' in t_result:  del t_result['products']
                    if 'open_ports' in t_result:  del t_result['open_ports']
                    if 'tags' in t_result:  t_result['tags'] = False
            else:
                if 5 == self._license:
                    if 0 == len(t_result['tags']):
                        t_result['tags'] = False
                    else:
                        t_result['tags'] = True
        else:
            t_result = data
        return t_result

    def close(self) -> None:
        """Closes the cti DB file and returns the resources to the system"""
        try:
            self._buffer.close()  # type: ignore
        except AttributeError:
            pass
        self.closed = True

    def __exit__(self, *args) -> None:
        self.close()

    def __enter__(self) -> "Reader":
        if self.closed:
            raise ValueError("Attempt to reopen a closed cti DB")
        return self


# =======================================================================================
# Metadata
# =======================================================================================
class Metadata:
    """Metadata for the cti DB reader

    .. attribute:: binary_format_major_version
      The major version number of the binary format used when creating the
      database.
      :type: int

    .. attribute:: binary_format_minor_version
      The minor version number of the binary format used when creating the
      database.
      :type: int

    .. attribute:: build_epoch
      The Unix epoch for the build time of the database.
      :type: int

    .. attribute:: database_type
      A string identifying the database type
      :type: str

    .. attribute:: description
      A map from locales to text descriptions of the database.
      :type: dict(str, str)

    .. attribute:: languages
      A list of locale codes supported by the databse.
      :type: list(str)

    .. attribute:: node_count
      The number of nodes in the database.
      :type: int

    .. attribute:: record_size
      The bit size of a record in the search tree.
      :type: int
    """

    def __init__(self, **kwargs) -> None:
        """Creates new Metadata object. kwargs are key/value pairs from spec"""
        # Although I could just update __dict__, that is less obvious and it
        # doesn't work well with static analysis tools and some IDEs
        self.node_count = kwargs["node_count"]
        self.record_size = kwargs["record_size"]
        self.ip_version = kwargs["ip_version"] if 'ip_version' in kwargs else 4
        self.database_type = kwargs["database_type"]
        self.languages = kwargs["languages"]
        self.binary_format_major_version = kwargs["binary_format_major_version"]
        self.binary_format_minor_version = kwargs["binary_format_minor_version"]
        self.build_epoch = kwargs["build_epoch"]
        self.build_epoch_limit = kwargs["build_epoch_limit"] if 'build_epoch_limit' in kwargs else None
        self.description = kwargs["description"]
        self.alias = kwargs["alias"] if 'alias' in kwargs else None
        self.license = kwargs["license"] if 'license' in kwargs else None

    @property
    def node_byte_size(self) -> int:
        """The size of a node in bytes

        :type: int
        """
        return self.record_size // 4

    @property
    def search_tree_size(self) -> int:
        """The size of the search tree

        :type: int
        """
        return self.node_count * self.node_byte_size

    def __repr__(self):
        args = ", ".join(f"{k}={v!r}" for k, v in self.__dict__.items())
        return f"{self.__module__}.{self.__class__.__name__}({args})"