from __future__ import annotations
from typing import Tuple, TYPE_CHECKING
from .decorators import decorate_all_methods, check_db_open
import inspect
import ida_ua
import ida_bytes
import ida_lines
import ida_kernwin
import ida_idaapi

if TYPE_CHECKING:
    from .database import Database


@decorate_all_methods(check_db_open)
class Instructions:
    """
    Provides access to instruction-related operations.
    """

    def __init__(self, database: "Database"):
        """
        Constructs an instructions handler for the given database.

        Args:
            database: Reference to the active IDA database.
        """
        self.m_database = database

    def is_valid(self, insn: object) -> bool:
        """
        Checks if the given instruction is valid.

        Args:
            insn: The instruction to validate.

        Returns:
            `true` if the instruction is valid, `false` otherwise.
        """
        if insn is None:
            return False

        # Check if instruction has valid itype (instruction type)
        try:
            return hasattr(insn, 'itype') and insn.itype != 0
        except:
            return False

    def decode(self, ea: int) -> Tuple[bool, object]:
        """
        Decodes the instruction at the specified address.

        Args:
            ea: The effective address of the instruction.

        Returns:
            A pair <bool, insn_t>. The bool indicates success; if false, the instruction is invalid.
        """
        insn = ida_ua.insn_t()
        ret = ida_ua.decode_insn(insn, ea) > 0
        return ret, insn

    def get_disassembly(self, insn: object) -> Tuple[bool, str]:
        """
        Retrieves the disassembled string representation of the given instruction.

        Args:
            insn: The instruction to disassemble.

        Returns:
            A pair <bool, string>. If disassembly fails, the bool is false.
        """
        if not self.is_valid(insn):
            return (False, "")

        try:
            # Generate disassembly line
            line = ida_lines.generate_disasm_line(insn.ea, ida_lines.GENDSM_MULTI_LINE | ida_lines.GENDSM_REMOVE_TAGS)
            if line:
                return (True, line)
            else:
                ida_kernwin.warning(f"{inspect.currentframe().f_code.co_name}: Failed to generate disasm line for address 0x{insn.ea:x}")
                return (False, "")
        except:
            ida_kernwin.warning(f"{inspect.currentframe().f_code.co_name}: Failed to generate disasm line for address 0x{insn.ea:x}")
            return (False, "")

    def get_between(self, start: int, end: int):
        """
        Retrieves instructions between the specified addresses.

        Args:
            start: Start of the address range.
            end: End of the address range.

        Returns:
            An instruction iterator.
        """
        current = start
        while current < end:
            insn = ida_ua.insn_t()
            if ida_ua.decode_insn(insn, current) > 0:
                # Move to next instruction for next call
                current = ida_bytes.next_head(current, end)
                yield insn
