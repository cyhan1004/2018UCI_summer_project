from enum import Enum

class Conflict_flag(Enum):
    """
    Indirect Conflict
    """
    indirect_conflict = 6


    """
    Direct Conflict
    """
    # Already conflicted
    getting_severity = 5
    same_severity = 4
    lower_severity = 3

    # First conflict
    same_function = 2
    same_class = 1
    file_in = 0

    # Conflict solved
    conflict_finished = -1