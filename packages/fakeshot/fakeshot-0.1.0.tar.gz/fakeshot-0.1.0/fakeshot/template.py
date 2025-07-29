from __future__ import annotations

from typing import Any, Iterator, Generator
from pathlib import Path
from itertools import product
from dataclasses import asdict, dataclass


def _split(s: str) -> list[str]:
    """Split by comma and strip white space."""
    return [s.strip() for s in s.split(',')]


@dataclass(frozen=True)
class Shot:
    show: str
    scene: str
    shot: str
    task: str
    version: str
    frame: int

    def generate_path(self, template: Template, output: str) -> Path:
        data = asdict(self)
        data['frame'] = f'{self.frame:04d}'

        path = f'{template.path_pattern}/{template.file_pattern}.exr'
        return Path(output, path.format(**data))


@dataclass(init=False)
class Template:
    show: str = 'prj'
    scene: str = '001,002'
    shot: str = '0010,0020'
    task: str = 'comp,anim'
    version: str = 'v001'
    start_frame: int = 1001
    end_frame: int = 1010
    width: int = 512
    height: int = 512
    path_pattern: str = '{show}/{scene}/{shot}/{task}/{version}'
    file_pattern: str = '{show}_{scene}_{shot}_{task}_{version}.{frame}'

    def _get_permutations(self) -> Iterator[Any]:
        """
        Generates all possible permutations of scene, shot, task, version, and frame range.

        Yields:
            Iterator[Any]: An iterator over tuples containing all combinations
            of the split values of show, scene, shot, task, version, and
            each frame in the specified range.
        """
        return product(
            [self.show],
            _split(self.scene),
            _split(self.shot),
            _split(self.task),
            _split(self.version),
            range(self.start_frame, self.end_frame),
        )

    def generate_shots(self) -> Generator[Shot, Any, None]:
        """Returns a generator of Shot objects based on the current template data."""
        for _shot_permutation in self._get_permutations():
            yield Shot(*_shot_permutation)

    def update(self, user_template: dict[str, Any]):
        """Update current instance with dictionary data."""
        for k, v in user_template.items():
            setattr(self, k, v)
