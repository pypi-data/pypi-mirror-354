# Falyx CLI Framework — (c) 2025 rtj.dev LLC — MIT Licensed
"""save_file_action.py"""
from pathlib import Path

from rich.tree import Tree

from falyx.action.base_action import BaseAction


class SaveFileAction(BaseAction):
    """ """

    def __init__(self, name: str, file_path: str):
        super().__init__(name=name)
        self.file_path = file_path

    def get_infer_target(self) -> tuple[None, None]:
        return None, None

    async def _run(self, *args, **kwargs):
        raise NotImplementedError(
            "SaveFileAction is not finished yet... Use primitives instead..."
        )

    async def preview(self, parent: Tree | None = None): ...

    def __str__(self) -> str:
        return f"SaveFileAction(file_path={self.file_path})"
