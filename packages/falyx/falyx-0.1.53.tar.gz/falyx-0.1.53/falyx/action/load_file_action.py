# Falyx CLI Framework — (c) 2025 rtj.dev LLC — MIT Licensed
"""load_file_action.py"""
from pathlib import Path

from rich.tree import Tree

from falyx.action.base_action import BaseAction


class LoadFileAction(BaseAction):
    """ """

    def __init__(self, name: str, file_path: str):
        super().__init__(name=name)
        self.file_path = file_path

    def get_infer_target(self) -> tuple[None, None]:
        return None, None

    async def _run(self, *args, **kwargs):
        raise NotImplementedError(
            "LoadFileAction is not finished yet... Use primatives instead..."
        )

    async def preview(self, parent: Tree | None = None): ...

    def __str__(self) -> str:
        return f"LoadFileAction(file_path={self.file_path})"
