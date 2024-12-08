import argparse
import asyncio
import logging
import shutil
import signal
import sys
from pathlib import Path
from random import randint, choice, choices

import numpy
from PIL import Image

MESSAGE = "Hello, Привіт"

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Глобальний прапорець для відслідковування чи програма вже отримала Ctrl+C
interrupted = False


def handle_sigint(signum, frame):
    global interrupted
    if not interrupted:
        interrupted = True
        logger.info("Operation cancelled (Ctrl+C). Exiting the application.")
    sys.exit(0)


# Реєструємо обробник сигналу Ctrl+C
signal.signal(signal.SIGINT, handle_sigint)


async def get_random_filename() -> str:
    """
    Generate a random filename using a set of allowed characters.

    Args:
        None

    Returns:
        str: A randomly generated filename (without extension).
    """
    random_value = (
        "()+,-0123456789;=@ABCDEFGHIJKLMNOPQRSTUVWXYZ[]^_`abcdefghijklmnopqrstuvwxyz"
        "{}~абвгдеєжзиіїйклмнопрстуфхцчшщьюяАБВГДЕЄЖЗИІЇЙКЛМНОПРСТУФХЦЧШЩЬЮЯ"
    )
    return "".join(choices(random_value, k=8))


async def generate_text_files(path: Path) -> None:
    """
    Generate a text-like file with a random filename and a random document extension,
    and write a predefined message into it.

    Args:
        path (Path): The directory in which to create the file.

    Returns:
        None
    """
    documents = ("DOC", "DOCX", "TXT", "PDF", "XLSX", "PPTX")
    filename = await get_random_filename()
    file_path = path / f"{filename}.{choice(documents).lower()}"

    await asyncio.to_thread(file_path.write_bytes, MESSAGE.encode())


async def generate_archive_files(path: Path) -> None:
    """
    Generate an archive file (zip, gztar, tar) with a random name in the given directory.

    Args:
        path (Path): The directory where the archive should be created.

    Returns:
        None
    """
    archive = ("ZIP", "GZTAR", "TAR")
    filename = await get_random_filename()
    archive_name = path / filename

    await asyncio.to_thread(
        shutil.make_archive,
        str(archive_name),
        choice(archive).lower(),
        str(path),
    )


async def generate_image(path: Path) -> None:
    """
    Generate a random image (JPEG, PNG, JPG) and save it in the given directory.

    Args:
        path (Path): The directory to store the generated image.

    Returns:
        None
    """
    images = ("JPEG", "PNG", "JPG")
    filename = await get_random_filename()
    image_file_path = path / f"{filename}.{choice(images).lower()}"

    image_array = numpy.random.rand(100, 100, 3) * 255
    image = Image.fromarray(image_array.astype("uint8"))
    await asyncio.to_thread(image.save, image_file_path)


async def generate_folders(path: Path) -> None:
    """
    Generate a nested set of folders with random names from a predefined list.

    Args:
        path (Path): The directory under which new folders will be created.

    Returns:
        None
    """
    folder_name = [
        "temp",
        "folder",
        "dir",
        "tmp",
        "OMG",
        "is_it_true",
        "no_way",
        "find_it",
    ]
    chosen_folders = choices(
        folder_name,
        weights=[10, 10, 1, 1, 1, 1, 1, 1],
        k=randint(5, len(folder_name)),
    )
    folder_path = Path(path, *chosen_folders)

    await asyncio.to_thread(folder_path.mkdir, parents=True, exist_ok=True)


async def generate_folder_forest(path: Path) -> None:
    """
    Generate several nested folder structures under the given path.

    Args:
        path (Path): The base directory under which nested folder forests will be created.

    Returns:
        None
    """
    tasks = []
    for _ in range(randint(2, 5)):
        tasks.append(generate_folders(path))

    if tasks:
        await asyncio.gather(*tasks)


async def generate_random_files(path: Path) -> None:
    """
    Generate a random number of files (text, archive, image) in the given directory.

    Args:
        path (Path): The directory in which random files will be created.

    Returns:
        None
    """
    count = randint(5, 7)
    tasks = []
    function_list = [generate_text_files, generate_archive_files, generate_image]
    for _ in range(3, count):
        tasks.append(choice(function_list)(path))

    if tasks:
        await asyncio.gather(*tasks)


async def parse_folder_recursion(path: Path, visited: set[Path]) -> None:
    """
    Recursively traverse directories under the given path and generate random files in them,
    preventing infinite recursion by tracking visited directories via absolute paths.

    Args:
        path (Path): The directory from which to start the recursive traversal.
        visited (set[Path]): A set of already visited directories to avoid infinite loops.

    Returns:
        None
    """
    real_path = path.resolve()
    if real_path in visited:
        return
    visited.add(real_path)

    try:
        elements = await asyncio.to_thread(lambda: list(real_path.iterdir()))
    except Exception as e:
        logger.error(f"Error reading directory {real_path}: {e}")
        return

    tasks = []
    for element in elements:
        if await asyncio.to_thread(element.is_dir):
            tasks.append(generate_random_files(element))
            tasks.append(parse_folder_recursion(element, visited))

    if tasks:
        await asyncio.gather(*tasks)


async def file_generator(path: Path) -> None:
    """
    Generate a random folder structure and files within the given parent directory.

    Args:
        path (Path): The parent directory in which to generate files and folders.

    Returns:
        None
    """
    # Тут ми більше не створюємо теки, якщо вона вже існує,
    # оскільки це перевіримо перед викликом file_generator.
    await generate_folder_forest(path)
    visited = set()
    await parse_folder_recursion(path, visited)


async def main() -> None:
    """
    Main asynchronous entry point of the script. Parses command-line arguments to determine the path
    for file generation and then invokes the generation process.

    Args:
        None

    Returns:
        None
    """
    parser = argparse.ArgumentParser(
        description="Generate a random folder structure and files."
    )
    parser.add_argument(
        "target_dir",
        help="Path to the target directory where random files and folders will be generated.",
    )
    args = parser.parse_args()

    parent_folder_path = Path(args.target_dir).resolve()

    # Перевірка існування теки
    if parent_folder_path.exists():
        logger.error(f"Directory {parent_folder_path} already exists. Exiting.")
        return

    # Створюємо батьківську теку, якщо її немає
    await asyncio.to_thread(parent_folder_path.mkdir, parents=True, exist_ok=True)

    logger.info(f"Starting file generation in {parent_folder_path}")
    await file_generator(parent_folder_path)
    logger.info("File generation completed.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except EOFError:
        logger.error("Input ended unexpectedly. Exiting the application.")
    except KeyboardInterrupt:
        logger.info("Operation cancelled (Ctrl+C). Exiting the application.")
