from __future__ import annotations

import io
import csv
from itertools import product

import numpy as np
import OpenEXR
from PIL import Image, ImageDraw, ImageFont

from .logger import LOGGER
from .template import Template


def generate_dummy_exr(
    *,
    path: str,
    label: str,
    width: int = 512,
    height: int = 512
) -> None:
    """
    Generates a dummy EXR image file with a centered label.

    ```
    generate_dummy_exr(
        path='/path/to/file.1001.exr',
        label='myfile.1001',
        width=1920,
        height=1080
    )
    ```

    Args:
        path (str): The file path where the EXR image will be saved.
        label (str): The text label to display in the center of the image.
        width (int, optional): The width of the image in pixels. Defaults to 512.
        height (int, optional): The height of the image in pixels. Defaults to 512.

    Returns:
        None
    """
    #  Create a grayscale pillow image
    img = Image.new('RGB', (width, height), color=(20, 20, 20))  # dark gray background
    draw = ImageDraw.Draw(img)

    font = ImageFont.load_default(24)

    bbox = draw.textbbox((0, 0), label, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    text_position = ((width - text_w) // 2, (height - text_h) // 2)
    draw.text(text_position, label, font=font, fill=(220, 220, 220))

    # Convert Pillow image to NumPy
    img_np = np.asarray(img).astype(np.float32) / 255.0  # Normalize to 0.0–1.0

    # Create EXR header + save
    header = OpenEXR.Header(width, height)
    exr = OpenEXR.OutputFile(path, header)

    # Split RGB channels
    exr.writePixels({
        'R': img_np[:, :, 0].tobytes(),
        'G': img_np[:, :, 1].tobytes(),
        'B': img_np[:, :, 2].tobytes()
    })

    exr.close()


def generate_dummy_shots(template: Template, output: str) -> None:
    """
    Generates dummy EXR files for all permutations defined by the template.

    This function creates directories and generates dummy EXR files for each combination
    of scene, shot, task, version, and frame as specified by the template.

    ```
    template = Template(...)
    generate_dummy_shots(template, './data')
    ```

    Args:
        template (Template): The template object containing shot parameters and file patterns.
        output (str): The root directory where the generated EXR files will be saved.

    Returns:
        None
    """
    LOGGER.info('Generating shots...')
    for shot in template.generate_shots():

        shot_path = shot.generate_path(template, output)
        shot_path.parent.mkdir(exist_ok=True, parents=True)

        LOGGER.debug('Generating: %s', shot_path)

        generate_dummy_exr(
            path=shot_path.as_posix(),
            label=shot_path.stem,
            width=template.width,
            height=template.height
        )

    LOGGER.info('EXR files generated.')


def generate_csv(template: Template, output: str = '') -> None:
    """
    Generates a CSV file containing all combinations of scenes, shots, and tasks
    from the provided template.

    Args:
        template (Template): A Template object
        output (str, optional): The directory path where the 'shots.csv' file
        will be saved. If not provided, the CSV content will be printed to stdout.

    Returns:
        None

    """
    out = open(f'{output}/shots.csv', 'w', newline='') if output else io.StringIO()

    writer = csv.DictWriter(out, fieldnames=['scene', 'shot', 'task'])
    writer.writeheader()

    scenes = template.get_scenes()
    shots = template.get_shots()
    tasks = template.get_tasks()

    for scene, shot, task in product(scenes, shots, tasks):
        writer.writerow(dict(scene=scene, shot=shot, task=task))

    if isinstance(out, io.StringIO):
        print(out.getvalue())

    out.close()
