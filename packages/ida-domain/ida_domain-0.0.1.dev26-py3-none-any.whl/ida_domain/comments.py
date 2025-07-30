from typing import Tuple, TYPE_CHECKING
import inspect
import ida_bytes
import ida_kernwin
import ida_idaapi
from ida_ida import inf_get_min_ea, inf_get_max_ea

if TYPE_CHECKING:
    from .database import Database


class Comments:
    """
    Provides access to user-defined comments in the IDA database.
    """

    def __init__(self, database: "Database"):
        """
        Constructs a comment manager for the given database.

        Args:
            database: Reference to the active IDA database.
        """
        self.m_database = database

    def get(self, ea: int) -> Tuple[bool, str]:
        """
        Retrieves the comment at the specified address.

        Args:
            ea: The effective address.

        Returns:
            A pair (success, comment string). If no comment exists, success is false.
        """
        if not self.m_database.is_open():
            ida_kernwin.warning(f"{inspect.currentframe().f_code.co_name}: Database is not loaded. Please open a database first.")
            return (False, "")

        comment = ida_bytes.get_cmt(ea, False)
        if comment:
            return (True, comment)

        # Try repeatable comment
        rep_comment = ida_bytes.get_cmt(ea, True)
        if rep_comment:
            return True, rep_comment

        return False, ""

    def set(self, ea: int, comment: str) -> bool:
        """
        Sets a comment at the specified address.

        Args:
            ea: The effective address.
            comment: The comment text to assign.

        Returns:
            True if the comment was successfully set, false otherwise.
        """
        if not self.m_database.is_open():
            ida_kernwin.warning(f"{inspect.currentframe().f_code.co_name}: Database is not loaded. Please open a database first.")
            return False
        return ida_bytes.set_cmt(ea, comment, False)

    def get_all(self, include_repeatable: bool):
        """
        Creates an iterator for all comments in the database.

        Args:
            include_repeatable: Whether to include repeatable comments during iteration.

        Returns:
            A CommentsIterator instance.
        """
        current = inf_get_min_ea()

        while current < inf_get_max_ea():
            comment = ida_bytes.get_cmt(current, include_repeatable)
            if comment:
                yield current, comment

            current = ida_bytes.next_head(current, inf_get_max_ea())
