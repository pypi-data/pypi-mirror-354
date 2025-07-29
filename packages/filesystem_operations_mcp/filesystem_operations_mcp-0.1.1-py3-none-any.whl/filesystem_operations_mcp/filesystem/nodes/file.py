import base64
import mimetypes
import re
from pathlib import Path

from aiofiles import open as aopen
from aiofiles.os import remove as aremove
from magika.types import ContentTypeInfo, Status
from pydantic import BaseModel, Field, RootModel

from filesystem_operations_mcp.filesystem.detection.file_type import init_magika
from filesystem_operations_mcp.filesystem.errors import FileAlreadyExistsError, FileIsNotTextError, FilesystemServerOutsideRootError
from filesystem_operations_mcp.filesystem.mappings.magika_to_tree_sitter import code_mappings, data_mappings, script_mappings, text_mappings
from filesystem_operations_mcp.filesystem.nodes.base import BaseNode
from filesystem_operations_mcp.filesystem.patches.file import FileMultiplePatchTypes, FilePatchTypes

magika = init_magika()


class FileLine(RootModel):
    root: tuple[int, str] = Field(description="The line number and line of text")

    @property
    def line_number(self) -> int:
        return self.root[0]

    @property
    def line(self) -> str:
        return self.root[1]


class FileEntryMatch(BaseModel):
    match: FileLine = Field(description="The line of text that matches the pattern")
    before: list[FileLine] = Field(description="The lines of text before the line")
    after: list[FileLine] = Field(description="The lines of text after the line")


class FileEntry(BaseNode):
    """A file entry in the filesystem."""

    @property
    def stem(self) -> str:
        """The stem of the file."""
        return self.absolute_path.stem

    @property
    def file_path(self) -> str:
        """The path of the file."""
        return str(self.relative_path)

    @property
    def extension(self) -> str:
        """The extension of the file."""
        return self.absolute_path.suffix

    @property
    def is_binary(self) -> bool:
        if self.is_binary_mime_type:
            return True

        if magika := self.magika_content_type:
            return not magika.is_text

        return False

    @property
    def is_code(self) -> bool:
        return (
            self.magika_content_type_label in code_mappings  # bad linter
            or self.magika_content_type_label in script_mappings
        )

    @property
    def is_text(self) -> bool:
        return self.magika_content_type_label in text_mappings

    @property
    def is_data(self) -> bool:
        return self.magika_content_type_label in data_mappings

    @property
    def magika_content_type_label(self) -> str | None:
        result = magika.identify_path(self.absolute_path)
        if result.status != Status.OK:
            return None
        return result.output.label

    @property
    def magika_content_type(self) -> ContentTypeInfo | None:
        result = magika.identify_path(self.absolute_path)
        if result.status != Status.OK:
            return None
        return result.output

    @property
    def mime_type(self) -> str:
        return mimetypes.guess_type(self.absolute_path)[0] or "unknown"

    @property
    def is_binary_mime_type(self) -> bool:
        mime_type = self.mime_type

        if mime_type.startswith(("image/", "video/", "audio/")):
            return True

        if mime_type.startswith("application/") and not (mime_type.endswith(("json", "xml"))):  # noqa: SIM103
            return True

        return False

    @property
    async def size(self) -> int:
        stat_result = await self._stat
        return stat_result.st_size

    @property
    async def read_binary_base64(self) -> str:
        """Read the binary contents of the file and convert it to a base64 string."""

        async with aopen(self.absolute_path, mode="rb") as f:
            binary = await f.read()

        return base64.b64encode(binary).decode("utf-8")

    @property
    async def read_text(self) -> str:
        """The contents of the file as text."""
        if self.is_binary_mime_type:
            raise FileIsNotTextError(file_path=self.file_path)

        async with aopen(self.absolute_path, encoding="utf-8") as f:
            return await f.read()

    @property
    async def read_text_lines(self) -> list[str]:
        """The lines of the file as a list of strings."""
        # get the file encoding from the magika content type
        async with aopen(self.absolute_path, encoding="utf-8") as f:
            lines = await f.readlines()
            return [line.strip() for line in lines]

    @property
    async def read_text_line_numbers(self) -> list[FileLine]:
        """The lines of the file as a list of FileLine objects which are a tuple of the line number and the line of text."""
        lines = await self.read_text_lines
        return self._get_lines(lines)

    @classmethod
    async def create_file(cls, file_path: Path, content: str) -> None:
        """Creates a file."""
        if file_path.exists():
            raise FileAlreadyExistsError(file_path=str(file_path))

        async with aopen(file_path, mode="w", encoding="utf-8") as f:
            await f.write(content)

    async def delete(self) -> None:
        """Deletes the file."""
        await aremove(self.absolute_path)

    async def apply_patch(self, patch: FilePatchTypes) -> None:
        """Applies the patch to the file."""
        lines = await self.read_text_lines
        lines = patch.apply(lines)
        await self.save(lines)

    async def apply_patches(self, patches: FileMultiplePatchTypes) -> None:
        """Applies the patches to the file."""
        lines = await self.read_text_lines

        # Reverse the patches if they are a list so that they are applied in the correct order.
        patches_to_apply: list[FilePatchTypes] = list(reversed(patches)) if isinstance(patches, list) else [patches]

        for patch in patches_to_apply:
            lines = patch.apply(lines)

        await self.save(lines)

    async def save(self, lines: list[str]) -> None:
        """Saves the file with the given lines."""
        async with aopen(self.absolute_path, mode="w", encoding="utf-8") as f:
            await f.write("\n".join(lines))

    async def preview_contents(self, head: int) -> str:
        """The first `head` bytes of the file."""
        async with aopen(self.absolute_path, encoding="utf-8") as f:
            return await f.read(head)

    def validate_in_root(self, root: Path) -> None:
        """Validates that the file is in the root."""
        if not self.is_relative_to(root.resolve()):
            raise FilesystemServerOutsideRootError(self.absolute_path, root)

    def is_relative_to(self, other: Path) -> bool:
        """Checks if the file is relative to another path."""
        return self.absolute_path.is_relative_to(other)

    async def contents_match(self, pattern: str, before: int = 0, after: int = 0) -> list[FileEntryMatch]:
        """Searches for a pattern in the file and returns the line numbers of the matches.

        Args:
            pattern: The pattern to search for.
            before: The number of lines before the match to include.
            after: The number of lines after the match to include.
        """
        lines = await self.read_text_lines
        match_lines: list[int] = [i for i, line in enumerate(lines) if pattern in line]
        return [
            FileEntryMatch(
                match=self._get_line(lines, i),
                before=self._get_lines_before(lines, i, before),
                after=self._get_lines_after(lines, i, after),
            )
            for i in match_lines
        ]

    async def contents_match_regex(self, pattern: str, before: int = 0, after: int = 0) -> list[FileEntryMatch]:
        """Searches for a regex pattern in the file and returns the line numbers of the matches.

        Args:
            pattern: The regex pattern to search for.
            before: The number of lines before the match to include.
            after: The number of lines after the match to include.
        """
        lines = await self.read_text_lines
        return [
            FileEntryMatch(
                match=self._get_line(lines, i),
                before=self._get_lines_before(lines, i, before),
                after=self._get_lines_after(lines, i, after),
            )
            for i, line in enumerate(lines)
            if re.search(pattern, line)
        ]

    async def get_lines(self, line_numbers: list[int]) -> list[FileLine]:
        """Gets the lines of the file at the given line numbers."""
        from_lines = await self.read_text_lines
        return [self._get_line(from_lines, i) for i in line_numbers]

    @classmethod
    def _get_line(cls, from_lines: list[str], line_number: int) -> FileLine:
        return FileLine(root=(line_number, from_lines[line_number]))

    @classmethod
    def _get_lines(cls, from_lines: list[str]) -> list[FileLine]:
        return [FileLine(root=(i, line)) for i, line in enumerate(from_lines)]

    @classmethod
    def _get_lines_range(cls, from_lines: list[str], start: int, end: int) -> list[FileLine]:
        return [FileLine(root=(i, line)) for i, line in enumerate(from_lines[start:end])]

    @classmethod
    def _get_lines_before(cls, from_lines: list[str], line_number: int, before: int) -> list[FileLine]:
        return [FileLine(root=(i, line)) for i, line in enumerate(from_lines[line_number - before : line_number])]

    @classmethod
    def _get_lines_after(cls, from_lines: list[str], line_number: int, after: int) -> list[FileLine]:
        return [FileLine(root=(i, line)) for i, line in enumerate(from_lines[line_number : line_number + after])]
