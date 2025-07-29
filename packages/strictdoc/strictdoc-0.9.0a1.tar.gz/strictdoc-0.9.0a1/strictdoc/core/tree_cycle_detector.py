# mypy: disable-error-code="no-untyped-call,no-untyped-def"
from collections import deque
from typing import Deque, Tuple

from strictdoc.backend.sdoc.errors.document_tree_error import DocumentTreeError
from strictdoc.backend.sdoc.models.model import SDocNodeIF

BEFORE = 1
AFTER = 2


class TreeCycleDetector:
    def __init__(self):
        self.checked = set()

    def check_node(self, node: SDocNodeIF, links_function):
        if node in self.checked:
            return
        stack: Deque[Tuple[SDocNodeIF, int]] = deque()
        stack.append((node, BEFORE))
        visited = set()
        while stack:
            current_node, token = stack[-1]
            if token == BEFORE:
                visited.add(current_node)
                stack[-1] = (current_node, AFTER)
                node_links = links_function(current_node)
                for node_link in reversed(node_links):
                    if node_link in visited:
                        cycled_nodes = []
                        for uid, token in stack:
                            if token == BEFORE:
                                continue
                            cycled_nodes.append(uid)
                        raise DocumentTreeError.cycle_error(
                            node_link, cycled_nodes
                        )
                    if node_link not in self.checked:
                        stack.append((node_link, BEFORE))
            elif token == AFTER:
                visited.remove(current_node)
                self.checked.add(current_node)
                stack.pop()
        self.checked.add(node)


class SingleShotTreeCycleDetector:
    def check_node(self, new_uid, node, links_function):
        checked = set()

        stack: Deque[Tuple[SDocNodeIF, int]] = deque()
        stack.append((node, BEFORE))
        visited = {new_uid}
        while stack:
            current_node, token = stack[-1]
            if token == BEFORE:
                visited.add(current_node)
                stack[-1] = (current_node, AFTER)
                node_links = links_function(current_node)
                for node_link in reversed(node_links):
                    if node_link in visited:
                        cycled_nodes = [new_uid]
                        for uid, token in stack:
                            if token == BEFORE:
                                continue
                            cycled_nodes.append(uid)
                        raise DocumentTreeError.cycle_error(
                            node_link, cycled_nodes
                        )
                    if node_link not in checked:
                        stack.append((node_link, BEFORE))
            elif token == AFTER:
                visited.remove(current_node)
                checked.add(current_node)
                stack.pop()
