from __future__ import annotations
from typing import Tuple, TYPE_CHECKING
from .decorators import decorate_all_methods, check_db_open
import ida_bytes
import ida_kernwin
import ida_lines
import ida_ida
import struct
import inspect

if TYPE_CHECKING:
    from .database import Database


@decorate_all_methods(check_db_open)
class Bytes:
    """
    Handles operations related to raw data access from the IDA database.
    """

    def __init__(self, database: "Database"):
        """
        Constructs a bytes handler for the given database.

        Args:
            database: Reference to the active IDA database.
        """
        self.m_database = database

    def get_byte(self, ea: int) -> Tuple[bool, int]:
        """
        Retrieves a byte at the specified address.

        Args:
            ea: The effective address.

        Returns:
            A pair of (success flag, value). If the flag is false, the value is undefined.
        """
        try:
            value = ida_bytes.get_byte(ea)
            return (True, value)
        except:
            return (False, 0)

    def get_word(self, ea: int) -> Tuple[bool, int]:
        """
        Retrieves a word (2 bytes) at the specified address.

        Args:
            ea: The effective address.

        Returns:
            A pair of (success flag, value). If the flag is false, the value is undefined.
        """
        try:
            value = ida_bytes.get_word(ea)
            return (True, value)
        except:
            return (False, 0)

    def get_dword(self, ea: int) -> Tuple[bool, int]:
        """
        Retrieves a double word (4 bytes) at the specified address.

        Args:
            ea: The effective address.

        Returns:
            A pair of (success flag, value). If the flag is false, the value is undefined.
        """
        try:
            value = ida_bytes.get_dword(ea)
            return (True, value)
        except:
            return (False, 0)

    def get_qword(self, ea: int) -> Tuple[bool, int]:
        """
        Retrieves a quad word (8 bytes) at the specified address.

        Args:
            ea: The effective address.

        Returns:
            A pair of (success flag, value). If the flag is false, the value is undefined.
        """
        try:
            value = ida_bytes.get_qword(ea)
            return (True, value)
        except:
            return (False, 0)

    def get_float(self, ea: int) -> Tuple[bool, float]:
        """
        Retrieves a float value at the specified address.

        Args:
            ea: The effective address.

        Returns:
            A pair of (success flag, value). If the flag is false, the value is undefined.
        """
        # Get data element size for float
        try:
            size = ida_bytes.get_data_elsize(ea, ida_bytes.float_flag())
        except:
            return (False, 0.0)

        if size <= 0 or size > 16:
            return (False, 0.0)

        # Read bytes from address
        data = ida_bytes.get_bytes(ea, size)
        if data is None or len(data) != size:
            func_name = inspect.currentframe().f_code.co_name
            ida_kernwin.warning(f"{func_name}: Failed to read float from address 0x{ea:x}\n")
            return (False, 0.0)

        # Convert bytes to float
        try:
            # Get processor endianness
            is_little_endian = not ida_ida.inf_is_be()
            endian = '<' if is_little_endian else '>'

            if size == 4:
                # IEEE 754 single precision
                value = struct.unpack(f'{endian}f', data)[0]
            elif size == 8:
                # IEEE 754 double precision (treat as float)
                double_value = struct.unpack(f'{endian}d', data)[0]
                value = float(double_value)
            else:
                # Handle other float sizes
                func_name = inspect.currentframe().f_code.co_name
                ida_kernwin.warning(f"{func_name}: Failed to interpret float from address 0x{ea:x}\n")
                return (False, 0.0)

        except (struct.error, ValueError, OverflowError):
            func_name = inspect.currentframe().f_code.co_name
            ida_kernwin.warning(f"{func_name}: Failed to convert to float value from address 0x{ea:x}\n")
            return (False, 0.0)

        return (True, value)

    def get_double(self, ea: int) -> Tuple[bool, float]:
        """
        Retrieves a double (floating-point) value at the specified address.

        Args:
            ea: The effective address.

        Returns:
            A pair of (success flag, value). If the flag is false, the value is undefined.
        """
        # Get data element size for double
        try:
            size = ida_bytes.get_data_elsize(ea, ida_bytes.double_flag())
        except:
            return (False, 0.0)

        if size <= 0 or size > 16:
            return (False, 0.0)

        # Read bytes from address
        data = ida_bytes.get_bytes(ea, size)
        if data is None or len(data) != size:
            func_name = inspect.currentframe().f_code.co_name
            ida_kernwin.warning(f"{func_name}: Failed to read double from address 0x{ea:x}\n")
            return (False, 0.0)

        # Convert bytes to double
        try:
            # Get processor endianness
            is_little_endian = not ida_ida.inf_is_be()
            endian = '<' if is_little_endian else '>'

            if size == 8:
                # IEEE 754 double precision
                value = struct.unpack(f'{endian}d', data)[0]
            elif size == 4:
                # Single precision treated as double
                float_value = struct.unpack(f'{endian}f', data)[0]
                value = float(float_value)
            else:
                # Handle other double sizes
                func_name = inspect.currentframe().f_code.co_name
                ida_kernwin.warning(f"{func_name}: Failed to interpret double from address 0x{ea:x}\n")
                return (False, 0.0)

        except (struct.error, ValueError, OverflowError):
            func_name = inspect.currentframe().f_code.co_name
            ida_kernwin.warning(f"{func_name}: Failed to convert to double value from address 0x{ea:x}\n")
            return (False, 0.0)

        return (True, value)

    def get_disassembly(self, ea: int) -> Tuple[bool, str]:
        """
        Retrieves the disassembly text at a specified address.

        Args:
            ea: The effective address.

        Returns:
            A pair of (success flag, disassembly string). If the flag is false, the string is undefined.
        """
        try:
            # Generate disassembly line with multi-line and remove tags flags
            line = ida_lines.generate_disasm_line(ea, ida_lines.GENDSM_MULTI_LINE | ida_lines.GENDSM_REMOVE_TAGS)
            if line:
                return (True, line)
            else:
                func_name = inspect.currentframe().f_code.co_name
                ida_kernwin.warning(f"{func_name}: Failed to generate disasm line for address 0x{ea:x}.\n")
                return (False, "")
        except:
            func_name = inspect.currentframe().f_code.co_name
            ida_kernwin.warning(f"{func_name}: Failed to generate disasm line for address 0x{ea:x}.\n")
            return (False, "")
