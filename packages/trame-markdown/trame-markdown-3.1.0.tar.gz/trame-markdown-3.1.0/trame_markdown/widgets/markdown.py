from trame_client.widgets.core import AbstractElement
from trame_markdown import module


def theme_light():
    module.force_theme("light")


def theme_dark():
    module.force_theme("dark")


class Markdown(AbstractElement):
    """
    Create a markdown viewer element

    >>> component = Markdown("**Bold**")
    >>> component.update(another_md_content)

    >>> content = \"\"\"
    ...
    ... # My document
    ... 1. First
    ... 2. Second
    ... 3. Third
    ...
    ... Hello "trame"
    ... \"\"\"
    >>> component = Markdown(content=("document2", content))
    """

    _next_md_id = 0

    def __init__(self, _md_content="**Some Mardown content**", **kwargs):
        """
        :param _md_content: Markdown to start with
        :type _md_content: str

        :param content: If provided it will be process as a regular attribute
                        for the Markdown content handling.
        """
        super().__init__("markdown", **kwargs)
        if self.server:
            self.server.enable_module(module)

        self._attr_names += ["content"]

        if "content" not in kwargs:
            Markdown._next_md_id += 1
            self._key = f"trame__markdown_{Markdown._next_md_id}"
            self.server.state[self._key] = _md_content
            self._attributes["content"] = f':content="{self._key}"'
        elif not isinstance(kwargs["content"], (tuple, list)):
            raise Exception("Markdown widget should only pass data as variable")
        else:
            self._key = kwargs["content"][0]

    @property
    def key(self):
        """Return the name of the state variable used internally"""
        return self._key

    @property
    def md_content(self):
        """Return the markdown content currently used for that widget"""
        return self.server.state[self._key]

    def update(self, _md_content, **kwargs):
        """
        Update the Markdown content to show.

        :param _md_content: Markdown syntax as string
        """
        self.server.state[self._key] = _md_content


__all__ = [
    "Markdown",
    "theme_light",
    "theme_dark",
]
