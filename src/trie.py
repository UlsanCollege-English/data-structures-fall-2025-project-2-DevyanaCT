"""
Trie implementation supporting autocomplete and frequency ranking.

Required public API for testing:
- class Trie
    insert(word, freq)
    remove(word) -> bool
    contains(word) -> bool
    complete(prefix, k) -> list[str]
    stats() -> (num_words, height, num_nodes)
    items() -> list[(word, freq)]
"""

import heapq


class TrieNode:
    """
    Node of a Trie. Stores children, whether it ends a word,
    and an associated frequency.
    """
    __slots__ = ("children", "is_end", "freq")

    def __init__(self):
        self.children = {}     # char -> TrieNode
        self.is_end = False    # marks full word
        self.freq = 0.0        # frequency for this word only


class Trie:
    def __init__(self):
        self.root = TrieNode()
        self._count_words = 0
        self._count_nodes = 1  # root included

    # --- internal helper -----------------------------------------------------

    def _walk(self, text):
        """
        Traverse the Trie along 'text'.
        Returns (node, path) or (None, empty list) if path breaks.
        path list contains (node, char) pairs used for removal pruning.
        """
        current = self.root
        path = [(current, '')]  # keep track for pruning

        for ch in text:
            nxt = current.children.get(ch)
            if nxt is None:
                return None, []
            current = nxt
            path.append((current, ch))

        return current, path

    # --- public interface ----------------------------------------------------

    def insert(self, word, freq):
        """
        Insert/update a word with the given frequency.
        Time: O(len(word))
        """
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
                self._count_nodes += 1
            node = node.children[ch]

        if not node.is_end:
            node.is_end = True
            self._count_words += 1

        node.freq = freq

    def remove(self, word):
        """
        Delete a word if present. Returns True if removed.
        Prunes nodes that become unused.
        Time: O(len(word))
        """
        node, path = self._walk(word)
        if node is None or not node.is_end:
            return False

        node.is_end = False
        node.freq = 0.0
        self._count_words -= 1

        # prune backwards
        for i in range(len(path) - 1, 0, -1):
            parent, ch_parent = path[i - 1]
            child, ch_child = path[i]

            if child.children or child.is_end:
                break  # still in use

            # remove this unused leaf node
            del parent.children[ch_child]
            self._count_nodes -= 1

        return True

    def contains(self, word):
        """
        Return True if word is stored.
        Time: O(len(word))
        """
        node, _ = self._walk(word)
        return node is not None and node.is_end

    def complete(self, prefix, k):
        """
        Return up to k words that begin with prefix, highest frequency first.
        Lexical sorting breaks ties.
        """
        start, _ = self._walk(prefix)
        if start is None:
            return []

        heap = []

        def explore(node, built):
            if node.is_end:
                pair = (node.freq, built)
                if len(heap) < k:
                    heapq.heappush(heap, pair)
                else:
                    heapq.heappushpop(heap, pair)

            # lexicographic ensures ties handled consistently
            for c in sorted(node.children):
                explore(node.children[c], built + c)

        explore(start, prefix)

        # sort by freq DESC then word ASC
        heap.sort(key=lambda x: (-x[0], x[1]))
        return [w for _, w in heap]

    def stats(self):
        """
        Returns (#words, height, #nodes).
        Height is the length of the longest word stored.
        """

        def height(node):
            if not node.children:
                return 0
            return 1 + max(height(child) for child in node.children.values())

        return (self._count_words, height(self.root), self._count_nodes)

    def items(self):
        """
        Return list of (word, freq) pairs.
        """
        collected = []

        def dfs(node, sofar):
            if node.is_end:
                collected.append((sofar, node.freq))

            for c, nxt in node.children.items():
                dfs(nxt, sofar + c)

        dfs(self.root, "")
        return collected
