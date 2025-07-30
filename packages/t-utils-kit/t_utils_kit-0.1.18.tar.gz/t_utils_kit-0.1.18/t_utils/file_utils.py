"""Module for all methods related to folders and files handling."""
import os
import re
import shutil
import time
import zipfile

from datetime import datetime
from pathlib import Path
from typing import List, Union

import psutil

from t_utils.datetime_utils import Timer
from t_utils.lib_utils.logger import logger


def delete_folder(folder_path: Union[str, Path]) -> None:
    """Delete folder.

    Args:
        folder_path (Path): Path to folder
    """
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path, ignore_errors=True)


def create_or_clean_folder(folder_path: Union[str, Path]) -> None:
    """Creates a new folder or cleans an existing folder.

    This function checks if the specified directory exists:
    - If it exists, it removes all its contents (files and subdirectories).
    - If it does not exist, it creates the directory.

    Args:
        folder_path (Path): Path to the directory to be created or cleaned.

    Returns:
        None

    Raises:
        OSError: If there is an issue deleting files or creating the directory.

    Example:
        create_or_clean_folder(Path("output_folder"))
    """
    if isinstance(folder_path, str):
        folder_path = Path(folder_path)
    if folder_path.exists():
        shutil.rmtree(folder_path, ignore_errors=True)
    folder_path.mkdir(parents=True, exist_ok=True)


def zip_folder(
    folder_path: Union[str, Path],
    output_zip: Union[str, Path] = "output",
    zip_filename: str = "outputs.zip",
    extensions: Union[List[str], None] = None,
    contains_filter: Union[List[str], None] = None,
    recursively: bool = True,
    regex: Union[str, None] = None,
) -> Path:
    """Create a zip archive for the entire folder with optional filters for files.

    Args:
        folder_path (Union[str, Path]): Path to the folder to zip.
        output_zip (Union[str, Path]): Path to save the resulting zip file. Defaults to "output".
        zip_filename (str): Name for the resulting zip file. Defaults to "output.zip".
        extensions (List[str]): List of file extensions or specific
        file names to include in the zip. Defaults to None (no filtering).
        contains_filter (str): Filter to include only files whose names contain this string. Defaults to "" (no filter).
        recursively (bool): Whether to include files in subdirectories recursively. Defaults to True.
        regex (Union[str, None]): A regex pattern that filenames should match. Optional.

    Returns:
        Path: The path to the created zip file.
    """
    folder_path = Path(folder_path)
    output_zip = Path(output_zip)

    # Create parent directory for the zip file if it doesn't exist
    output_zip.mkdir(parents=True, exist_ok=True)

    # Combine the output path with the zip file name
    zip_path = output_zip / zip_filename

    # Get filtered list of files using the helper method
    files_to_zip = list_files_in_folder(folder_path, extensions, contains_filter, regex, recursive=recursively)

    # Create the zip archive
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for file in files_to_zip:
            file_path = Path(file)
            # Use relative path for files inside the zip
            arcname = file_path.relative_to(folder_path)
            zipf.write(file_path, arcname)
            os.remove(file_path)

    return zip_path


def create_folder_if_not_exist(folder_path: Union[str, Path]) -> None:
    """Creates a directory if it does not already exist.

    This function checks whether the specified directory exists. If not, it creates
    the directory along with any necessary intermediate directories.

    Args:
        folder_path (Union[str, Path]): The path of the folder to check or create.

    Returns:
        None
    """
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)


def list_files_in_folder(
    folder_path: Union[str, Path],
    extensions: Union[List[str], None] = None,
    filter_words: Union[List[str], None] = None,
    regex: Union[str, None] = None,
    recursive: bool = True,
) -> List[str]:
    """List all files in a directory with optional filters for extension, word containment, and regex.

    Args:
        folder_path (Union[str, Path]): Path to the directory to list files from.
        extensions (List[str]): File extensions to filter by (e.g., [".txt", ".csv"]). Optional.
        filter_words (Union[List[str], None]): Words that filenames should contain. Optional.
        regex (Union[str, None]): A regex pattern that filenames should match. Optional.
        recursive (bool): Whether to include files in subdirectories recursively. Defaults to True.

    Returns:
        List[str]: A list of file paths matching the specified criteria.
    """
    folder_path = Path(folder_path)
    if not folder_path.exists() or not folder_path.is_dir():
        return []

    files = []
    search_paths = folder_path.rglob("*") if recursive else folder_path.iterdir()

    for file in search_paths:
        if file.is_file():
            # Apply extension filter
            if extensions and file.suffix not in extensions:
                continue

            # Apply filter_words filter
            if filter_words and not any(word in file.name for word in filter_words):
                continue

            # Apply regex filter
            if regex and not re.search(regex, file.name):
                continue

            files.append(str(file))

    return files


def copy_files_from_folder_to_folder(
    src_folder: Union[str, Path],
    dst_folder: Union[str, Path],
    extensions: Union[List[str], None] = None,
    filter_words: Union[List[str], None] = None,
) -> None:
    """Copies all files from the source directory to the destination directory.

    This function ensures that all files in the source directory are copied to the
    destination directory. If the destination directory does not exist, it will
    be created automatically. Subdirectories within the source directory are ignored.

    Args:
        src_folder (Union[str, Path]): The path to the directory containing the files to be copied.
        dst_folder (Union[str, Path]): The path to the target directory where files will be copied.
        extensions (Union[List[str], None]): File extension to filter by (e.g., [".txt"]). Optional.
        filter_words (Union[List[str], None]): A word that filenames should contain. Optional.

    Returns:
        None

    Raises:
        FileNotFoundError: If the source directory does not exist.
        PermissionError: If there are permission issues accessing the directories or files.

    Example:
        copy_files_from_folder_to_folder("source_folder", "destination_folder")
    """
    create_folder_if_not_exist(dst_folder)

    for filename in list_files_in_folder(src_folder, extensions, filter_words):
        if os.path.isfile(os.path.join(src_folder, filename)):
            shutil.copy(os.path.join(src_folder, filename), dst_folder)


def move_files_from_folder_to_folder(
    src_folder: Union[str, Path],
    dst_folder: Union[str, Path],
    extensions: Union[List[str], None] = None,
    filter_words: Union[List[str], None] = None,
    recursive: bool = True,
) -> None:
    """Moves all files from the source directory to the destination directory.

    This function ensures that all files in the source directory are moved to the
    destination directory. If the destination directory does not exist, it will
    be created automatically. Files in subdirectories are also moved if `recursive` is True.

    Args:
        src_folder (Union[str, Path]): The path to the directory containing the files to be moved.
        dst_folder (Union[str, Path]): The path to the target directory where files will be moved.
        extensions (Union[List[str], None]): File extension to filter by (e.g., [".txt"]). Optional.
        filter_words (Union[List[str], None]): A word that filenames should contain. Optional.
        recursive (bool): Whether to include files in subdirectories recursively. Defaults to True.

    Returns:
        None

    Raises:
        FileNotFoundError: If the source directory does not exist.
        PermissionError: If there are permission issues accessing the directories or files.

    Example:
        move_files_from_folder_to_folder("source_folder", "destination_folder")
    """
    src_folder = Path(src_folder)
    dst_folder = Path(dst_folder)
    create_folder_if_not_exist(dst_folder)

    for filename in list_files_in_folder(src_folder, extensions, filter_words, recursive=recursive):
        src_file = Path(filename)
        if src_file.is_file():
            dst_file = dst_folder / src_file.name

            if dst_file.exists():
                dst_file.unlink()

            shutil.move(str(src_file), str(dst_file))


def zip_files(output_zip: Union[str, Path], files_list: List[Union[str, Path]], zip_filename: str) -> None:
    """Creates a ZIP archive containing the specified list of files.

    Args:
        output_zip (Union[str, Path]): The file path where the ZIP output will be created.
        files_list (List[str]): A list of file paths to include in the ZIP archive.
        zip_filename (str): The name of the ZIP file to be created.

    Returns:
        None

    Raises:
        FileNotFoundError: If any file in the files_list does not exist.
        OSError: If there is an issue creating the ZIP file or writing to it.

    Example:
        zip_files("archive.zip", ["file1.txt", "file2.txt", "file3.txt"])

    Notes:
        - Each file is added to the ZIP archive with its basename (i.e., without directory structure).
        - If the target archive path already exists, it will be overwritten.
    """
    zip_file_path = Path(output_zip) / zip_filename
    with zipfile.ZipFile(zip_file_path, mode="w", compression=zipfile.ZIP_DEFLATED) as zipf:
        for file_str in files_list:
            file = Path(os.path.join(output_zip, file_str))
            if file.exists():
                zipf.write(file, arcname=file.name)
            else:
                logger.warning(f"File {file_str} does not exist.")


def delete_file(file_path: Union[str, Path]) -> None:
    """Delete folder.

    Args:
        file_path (Path): Path to file to be deleted.
    """
    if os.path.exists(file_path):
        shutil.rmtree(file_path, ignore_errors=True)


def copy_file_to_folder(src_file: Union[str, Path], dst_folder: Union[str, Path]) -> None:
    """Copies a single file to the specified directory.

    If the destination directory does not exist, it will be created automatically.
    This function ensures the integrity of the file by only copying it if the source
    is a valid file.

    Args:
        src_file (Union[str, Path]): The path to the source file to be copied.
        dst_folder (Union[str, Path]): The path to the target directory where the file will be copied.

    Returns:
        None

    Raises:
        FileNotFoundError: If the source file does not exist.
        OSError: If there is an issue creating the directory or copying the file.

    Example:
        copy_file_to_folder("example.txt", "backup_folder")
    """
    create_folder_if_not_exist(dst_folder)

    if not os.path.isfile(src_file):
        raise FileNotFoundError(f"The source file '{src_file}' does not exist or is not a file.")

    shutil.copy(src_file, dst_folder)


def move_file_to_folder(src_path: Union[str, Path], dst_path: Union[str, Path]) -> None:
    """Moves a file from one location to another.

    If the destination directory does not exist, it is created automatically.
    If a file already exists at the destination path, it will be overwritten.

    Args:
        src_path (str): The full path to the source file to be moved.
        dst_path (str): The full path to the destination file.

    Returns:
        None

    Raises:
        FileNotFoundError: If the source file does not exist.
        Exception: For any other errors during the move operation.

    Example:
        move_file("source_folder/example.txt", "destination_folder/example.txt")
    """
    try:
        if not os.path.exists(src_path):
            raise FileNotFoundError(f"The source file '{src_path}' does not exist.")

        Path(dst_path).parent.mkdir(parents=True, exist_ok=True)
        if os.path.exists(dst_path):
            os.remove(dst_path)

        shutil.move(src_path, dst_path)

    except FileNotFoundError as fnf_error:
        raise fnf_error
    except Exception as e:
        raise Exception(f"Failed to move file from '{src_path}' to '{dst_path}'. Error: {str(e)}")


def wait_until_files_exist(
    file_identifier: Union[str, Path],
    folder_path: Union[str, Path, None] = None,
    is_regex: bool = False,
    wait_time: int = 30,
    expected_files_count: int = 1,
) -> List[str]:
    """Waits until a file (or files) with the specified name or matching a regex pattern is found in a directory.

    Args:
        file_identifier (Union[str, Path]): The file name or a regex pattern to match.
        folder_path (Union[str, Path, None]): Directory to monitor. If None, uses the current working directory.
        is_regex (bool, optional): If True, treats `file_identifier` as a regex pattern. Defaults to False.
        wait_time (int, optional): Maximum time to wait (in seconds). Defaults to 30.
        expected_files_count (int, optional): Number of files to expect. Defaults to 1.

    Returns:
        List[str]: A list containing the full paths of the matched files.

    Raises:
        AssertionError: If no matching file is found within the timeout.
    """
    if isinstance(folder_path, str):
        folder_path = Path(folder_path)
    if folder_path is None:
        folder_path = Path.cwd()

    file_identifier = str(file_identifier)

    logger.debug(
        f"Waiting for {'files matching pattern' if is_regex else 'a file named'}"
        f" '{file_identifier}' in '{folder_path}'."
    )

    timer = Timer(wait_time)
    while timer.not_expired:
        matched_files = []
        for file_name in list_files_in_folder(folder_path, recursive=False):
            if is_regex:
                if re.match(file_identifier, file_name):
                    matched_files.append(str(folder_path / file_name))
            else:
                if Path(file_name).name == Path(file_identifier).name:
                    matched_files.append(str(folder_path / file_name))

        if len(matched_files) >= expected_files_count:
            return matched_files

        time.sleep(1)

    raise AssertionError(
        f"{'Files matching the pattern' if is_regex else 'File'} "
        f"not found: {file_identifier} within {wait_time} seconds."
    )


def wait_until_file_exist(
    file_identifier: Union[str, Path],
    folder_path: Union[str, Path, None] = None,
    is_regex: bool = False,
    wait_time: int = 30,
) -> str:
    """Waits until a file with the specified name or matching a regex pattern is found in a directory.

    Args:
        file_identifier (Union[str, Path]): The file name or a regex pattern to match.
        folder_path (Union[str, Path, None]): Directory to monitor. If None, uses the current working directory.
        is_regex (bool, optional): If True, treats `file_identifier` as a regex pattern. Defaults to False.
        wait_time (int, optional): Maximum time to wait (in seconds). Defaults to 30.

    Returns:
        str: The full path of the first matched file.

    Raises:
        AssertionError: If no matching file is found within the timeout.
    """
    matched_files = wait_until_files_exist(file_identifier, folder_path, is_regex, wait_time, expected_files_count=1)
    return matched_files[0] if matched_files else ""


def create_time_based_file_name(base_name: str, extension: str, date_formate: str = "%Y%m%d_%H%M%S") -> str:
    """Create a file name with the current date time.

    Args:
        base_name (str): the file name
        extension (str): the file type
        date_formate (str): the format of datetime default value is %Y%m%d_%H%M%S

    Returns:
        str: The generated filename
    """
    # Get the current time and format it
    timestamp = datetime.now().strftime(date_formate)

    # Construct the filename
    filename = f"{base_name}_{timestamp}.{extension}"

    return filename


def rename_file(original_file: Union[str, Path], new_filename: str) -> str:
    """Rename the downloaded file with the new filename.

    Args:
        original_file (Union[str, Path]): The path to the original file.
        new_filename (str): The new filename.

    Returns:
        str: The path to the renamed file.
    """
    file_path = Path(original_file)
    new_file_path = os.path.join(file_path.parent, new_filename)
    os.rename(original_file, new_file_path)
    logger.debug(f"File renamed: {new_file_path}")
    return new_file_path


def wait_until_file_is_written(file_path: Union[str, Path], wait_time: int = 10) -> bool:
    """Wait until a file is no longer being written to.

    Args:
        file_path (Union[str, Path]): The path to the file.
        wait_time (int): The maximum time to wait in seconds. Default is 10.

    Returns:
        bool: True if the file is no longer being written to, False otherwise.
    """
    timer = Timer(wait_time)
    while timer.not_expired:
        size1 = os.path.getsize(file_path)
        time.sleep(1)
        size2 = os.path.getsize(file_path)
        if size1 == size2:
            return True
    return False


def is_file_open(file_path: Union[str, Path]) -> bool:
    """Verifies if given file is opened by other program.

    Args:
        file_path Union[str, Path]: File system path.

    Returns:
        Boolean.
    """
    file_path = str(file_path)
    for proc in psutil.process_iter(["pid", "name", "open_files"]):
        try:
            for file in proc.info["open_files"] or []:
                if file.path == file_path:
                    return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return False


def is_folder_empty(file_path: Union[str, Path]) -> bool:
    """Check if the given folder is empty, excluding the '__pycache__' directory.

    Args:
        file_path (Union[str, Path]): The path of the folder to check.

    Returns:
        bool: True if the folder is empty (ignoring '__pycache__'), False otherwise.

    Raises:
        ValueError: If the provided path does not exist or is not a directory.
    """
    if not os.path.exists(file_path):
        raise ValueError(f"The folder path '{file_path}' does not exist.")
    if len(os.listdir(file_path)) == 0:
        return True
    return False
