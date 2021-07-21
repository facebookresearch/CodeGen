# This file is adapted from https://github.com/Cobertos/bobskater

"""
Utility classes for tracking identifiers in Python scopes
"""

import builtins  # Do not use __builtins__, it's different in different implementations (like IPython vs CPython)
import ast


# TODO: After coming back to this a second time, the names aren't really sticking,
# Consider the name changes
# Source ==> sourceAstNode
# Parent ==> parentFrame
# Children ==> childFrames
# ids ==> entries
class Frame:
    """
    Keeps track of a stack frame and all the identifiers that exist in that frame
    """

    __slots__ = ["source", "parent", "children", "ids"]

    def __init__(self, source=None, parent=None, children=None, ids=None):
        self.source = source
        self.parent = parent
        self.children = children or []
        self.ids = ids or {}

    def __str__(self):
        return (
            "\n"
            + str(self.source.__class__.__name__ + " " if self.source else "Frame ")
            + "{"
            + "\n  ".join([s + ": " + str(i) for s, i in self.ids.items()])
            + "}"
            + ("\n=> v v v v" if len(self.children) else "")
            + (
                "\n=> ".join(" && ".join([str(s) for s in self.children]).split("\n"))
                if self.children
                else ""
            )
        )

    def __repr__(self):
        return str(self)

    def addFrame(self, frame):
        """Adds the given frame as a child of this frame"""
        assert isinstance(frame, Frame)
        assert frame != self

        self.children.append(frame)
        frame.parent = self

    def addEntry(self, frameEntry):
        """Adds an entry for the given identifier to this frame"""
        assert isinstance(frameEntry, FrameEntry)
        if frameEntry.id in self.ids:
            # Only record the first instance as subsequent instances arent _really_
            # allowed to redefine the scope. A global statement after a local assign
            # is ignored (Python 3.5). A local assign after a global ctx.Load is an error.
            # Im not really sure about nonlocal but if it acts like global then we
            # should be fine
            return

        self.ids[frameEntry.id] = frameEntry
        frameEntry.parent = self

    def getStack(self):
        """Returns a stack from the root frame to this current frame"""
        frames = [self]
        frame = frames[0].parent
        while frame:
            frames.insert(0, frame)
            frame = frames[0].parent
        return frames

    def getScopedEntry(self, frameEntryId):
        """
        Searches upward through parents looking for the first instance
        of frameEntryId, as if it was doing a scoped search
        """
        for frame in reversed(self.getStack()):
            if frameEntryId in frame.ids:
                entry = frame.ids[frameEntryId]
                if isinstance(entry.source, (ast.Global)):
                    # Return the special scopeParent pointing to
                    # the root
                    return entry.scopeParent.ids[entry.id]
                if isinstance(entry.ctx, ast.Store) and not isinstance(
                    entry.source, (ast.Global, ast.Nonlocal)
                ):
                    # Only ast.Store will actually define the scope for an ID
                    # and global and nonlocal nodes need to be pass through as well
                    return entry

        # This happens if the identifier was not seen in the given scope stack.
        # Most likely passing something erroneously in
        # logging.getLogger(self.__class__.__name__).error("Queried identifier \"" + frameEntryId + "\" was not been seen at the given scope stack")
        return None

    def findEntryAtStack(self, nodeStack, frameEntryId):
        """
        Using the nodeStack, finds the frameEntry for frameEntryId
        """
        # Find top frame mentioned in nodeStack. then traverse
        # down to find the scoped entry
        return self.getFrameStack(nodeStack)[-1].getScopedEntry(frameEntryId)

    def getAllIds(self):
        """
        Return all the IDs we can see from here in scoped order
        TODO: Convert to iterator, not list generator
        """
        ids = []
        for frame in reversed(self.getStack()):
            ids += frame.ids.keys()
        return ids

    def getFrameStack(self, nodeStack):
        """
        Using this frame as a root frame, returns the list of descendant frames
        that parallel the nodeStack. Otherwise, it will most likely throw
        a StopIteration error (TODO: Make it return None)
        """
        # Find the frame in question by traversing through the frames
        # using the stack frame creating nodes to compare to those
        # previously bookmarked
        # TODO: This could be better an iterator, not a list return
        frameStack = [self]
        for node in filter(Frame.nodeCreatesFrame, nodeStack):
            frame = frameStack[-1]
            frame = next(filter(lambda f: f.source == node, frame.children))
            frameStack.append(frame)
        return frameStack

    @staticmethod
    def nodeCreatesFrame(node):
        """Whether or not the given node should be creating a stack frame"""
        # todo: Comprehensions need to push a frame too
        return isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.Module))

    @staticmethod
    def getBuiltinFrame():
        """
        Gets a frame with entries for all the builtin variables in Python
        which is commonly the root frame for scope operations
        """
        frame = Frame()
        for b in dir(builtins) + ["__file__"]:
            frame.addEntry(FrameEntry(b))
        return frame


class FrameEntry:
    """
    Keeps track of data related to a scoped identifier that lives in a
    a stack frame.
    * Source is the node the identifier came from
    * Parent is the parent Frame
    * Ctx is ast.Load or ast.Store to catalog if it will push to the stack or not
    * Value is the return from onEnterStackFrame that was stored for this scoped identifier
    * Id is the identifier of this entry
    * ScopeParent is the actual parent (like for a global)
    """

    __slots__ = ["source", "parent", "ctx", "value", "id", "scopeParent"]

    def __init__(self, id, source=None, ctx=ast.Store(), scope=None, value=None):
        self.source = source
        self.ctx = ctx
        self.value = value
        self.id = id
        self.scopeParent = scope
        self.parent = None  # The actual frame parent

    def __str__(self):
        return (
            str(self.source.__class__.__name__)
            + (("(" + str(self.ctx.__class__.__name__) + ")") if self.ctx else "")
            + (("=" + str(self.value)) if self.value else "")
        )

    def __repr__(self):
        return str(self)


def getIdsFromNode(node):
    """
    Python ast does not make it easy to act simply on the identifiers of a node
    (and you have to switch over node types and get specific attributes). To
    ease this pain we return an array of all the identifiers flatly in a node
    and provide a set() function that takes a similar array.
    TODO: Properties that are not defined (that are None) just come back as blanks,
    do we want this? Do we want to be able to set the names of ids that aren't
    a thing
    TODO: If we need more granularity, we need to edit how this works (would need
    to return key'd objects)
    """
    # Handle global/nonlocal (Python3) statement
    if isinstance(node, (ast.Global, ast.Nonlocal)):
        return node.names
    # Handle import alias's
    elif isinstance(node, ast.alias):
        return [node.name if node.asname is None else node.asname]
    # Except
    elif isinstance(node, ast.ExceptHandler):
        # Is raw only in Python 3, Name node in Python 2, None if not included
        return [node.name] if hasattr(node, "name") and type(node.name) == str else []
    # FunctionDef or ClassDef
    elif isinstance(node, (ast.FunctionDef, ast.ClassDef)):
        return [node.name]
    # arguments
    # Up to Python 3.3, ast.arguments has kwargs and args as a raw string and not
    # as an ast.arg(which we handle in another case) so handle it
    elif isinstance(node, ast.arguments):
        ret = []
        if hasattr(node, "args") and type(node.args) == str:
            ret.append(node.args)
        if hasattr(node, "kwargs") and type(node.kwargs) == str:
            ret.append(node.kwargs)
    # TODO:keyword (in Python <3.3)
    # arg
    elif isinstance(node, ast.arg):
        return [node.arg] if type(node.arg) == str else []
    # TODO: Annotations (for everything x:)
    # Handle Name (which handles anything that doesn't use raw strings)
    elif isinstance(node, ast.Name):
        return [node.id]
    elif isinstance(node, ast.Attribute):
        return [node.attr]
    return []


def setIdsOnNode(node, names):
    """
    Tightly coupled to the implementation of getIdsFromNode. It must unpack
    it the EXACT same way
    """
    if not names:
        return  # Passed an empty array, don't do anything

    if isinstance(node, (ast.Global, ast.Nonlocal)):
        node.names = names
    elif isinstance(node, (ast.alias)):
        if node.asname is None:
            node.name = names[0]
        else:
            node.asname = names[0]
    elif isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.ExceptHandler)):
        node.name = names[0]
    elif isinstance(node, ast.arguments):
        # pop in reverse order
        if hasattr(node, "kwargs") and type(node.kwargs) == str:
            node.kwargs = names.pop()
        if hasattr(node, "args") and type(node.args) == str:
            node.args = names.pop()
    elif isinstance(node, ast.arg):
        node.arg = names[0]
    elif isinstance(node, ast.Name):
        node.id = names[0]
    elif isinstance(node, ast.Attribute):
        node.attr = names[0]
