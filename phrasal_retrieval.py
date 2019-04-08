from typing import Dict, Tuple, List, BinaryIO
from .data_structures import LinkedList
from .search import load_positional_index


def retrieve_phrase(
        dictionary: Dict[str, Tuple[float, Tuple[int, int], Tuple[int, int]]],
        postings_file: BinaryIO,
        tokens: List[str]) -> LinkedList[Tuple[str, LinkedList[int]]]:
    """
    Returns a LinkedList of documents that contain a specific phrase.

    :param dictionary
    :param postings_file the read-only binary file descriptor
    :param tokens tokens in phrase
    :return: A LinkedList of document IDs ().
    """
    if not tokens:
        return LinkedList()

    positional_index = load_positional_index(postings_file, dictionary, tokens[0])
    for token in tokens[1:]:
        next_positional_index = load_positional_index(postings_file,
                                                      dictionary, token)
        positional_index = merge_positional_indexes(positional_index,
                                          next_positional_index)

    return positional_index


def merge_positional_indexes(before: LinkedList[Tuple[str, LinkedList[int]]],
                             after: LinkedList[Tuple[str, LinkedList[int]]]
                             ) -> LinkedList[Tuple[str, LinkedList[int]]]:
    result = LinkedList()
    before, after = before.get_head(), after.get_head()
    while before is not None and after is not None:
        before_id, before_positions = before.value
        after_id, after_positions = after.value
        if before_id == after_id:
            merge_result = merge_positions(before_positions, after_positions)
            if merge_result:
                result.append((before_id, merge_result))
            before = before.next()
            after = after.next()
        elif before_id < after_id:

            if before.skip() and before.skip().value[0] <= after_id:
                before = before.skip()
            else:
                before = before.next()
        elif after.skip() and after.skip().value[0] <= before_id:
            after = after.skip()
        else:
            after = after.next()
    return result


def merge_positions(before_positions: LinkedList[int],
                    after_positions: LinkedList[int]):
    result = LinkedList()
    before_position, after_position = before_positions.get_head(
    ), after_positions.get_head()

    while before_position is not None and after_position is not None:
        if before_position.value == after_position.value - 1:
            result.append(after_position.value)
            before_position = before_positions.next()
            after_position = after.next()
        elif before_position.value < after_position.value - 1:
            if before_position.skip(
            ) and before_positions.skip().value <= after_position.value - 1:
                before_position = before_positions.skip()
            else:
                before_position = before_positions.next()
        elif after_position.skip(
        ) and after.skip().value - 1 <= before_position.value:
            after_position = after.skip()
        else:
            after_position = after.next()
    return result