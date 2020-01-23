import glob
import gzip
import hashlib
import json
import os.path
import re
import shutil

DIGESTED_FILE_REGEX = r"-[a-f\d]{32}"


def compile(input_path, output_path, digest_blacklist_filter, gzip_files):
    """
    Generate md5 tagged static files that are also compressed with gzip.

    :param input_path: The source path of your static files
    :type input_path: str
    :param output_path: The destination path of your static files
    :type output_path: str
    :param digest_blacklist_filter: Ignore compiling these file types
    :type digest_blacklist_filter: list
    :param gzip_files: Whether or not gzipped files will be generated
    :type gzip_files: bool
    :return: None
    """
    if not os.path.exists(input_path):
        print(f"The input path '{input_path}' does not exist")
        return None

    if not os.path.exists(output_path):
        print(f"The output path '{output_path}' does not exist")
        return None

    files = _filter_files(input_path, digest_blacklist_filter)
    manifest = _generate_manifest(files, gzip_files, output_path)
    _save_manifest(manifest, output_path)

    print(f"Check your digested files at '{output_path}'")
    return None


def clean(output_path, digest_blacklist_filter, gzip_files):
    """
    Delete the generated md5 tagged and gzipped static files.

    :param input_path: The source path of your static files
    :type input_path: str
    :param output_path: The destination path of your static files
    :type output_path: str
    :param digest_blacklist_filter: Ignore compiling these file types
    :type digest_blacklist_filter: list
    :param gzip_files: Whether or not gzipped files will be generated
    :type gzip_files: bool
    :return: None
    """
    for item in glob.iglob(output_path + "**/**", recursive=True):
        if os.path.isfile(item):
            file_name, file_extension = os.path.splitext(item)
            basename = os.path.basename(item)

            if (re.search(DIGESTED_FILE_REGEX, basename)
                    and file_extension not in digest_blacklist_filter):
                if os.path.exists(item):
                    os.remove(item)

            if gzip_files and file_extension == ".gz":
                if os.path.exists(item):
                    os.remove(item)

    manifest_path = os.path.join(output_path, "cache_manifest.json")

    if os.path.exists(manifest_path):
        os.remove(manifest_path)

    print(f"Check your cleaned files at '{output_path}'")
    return None


def _filter_files(input_path, digest_blacklist_filter):
    filtered_files = []

    for item in glob.iglob(input_path + "**/**", recursive=True):
        if os.path.isfile(item):
            if not _is_compiled_file(item, digest_blacklist_filter):
                filtered_files.append(item)

    return filtered_files


def _is_compiled_file(file_path, digest_blacklist_filter):
    file_name, file_extension = os.path.splitext(file_path)
    basename = os.path.basename(file_path)

    return (re.search(DIGESTED_FILE_REGEX, basename)
            or file_extension in digest_blacklist_filter
            or file_extension == ".gz"
            or basename == "cache_manifest.json")


def _generate_manifest(files, gzip_files, output_path):
    manifest = {}

    for file in files:
        rel_file_path = os.path.relpath(file, output_path).replace("\\", "/")

        file_name, file_extension = os.path.splitext(rel_file_path)

        digest = _generate_digest(file)
        digested_file_path = f"{file_name}-{digest}{file_extension}"

        manifest[rel_file_path] = digested_file_path

        _write_to_disk(file, digested_file_path, gzip_files, output_path)

    return manifest


def _generate_digest(file):
    digest = None

    with open(file, "rb") as f:
        digest = hashlib.md5(f.read()).hexdigest()

    return digest


def _save_manifest(manifest, output_path):
    manifest_content = json.dumps(manifest)
    manifest_path = os.path.join(output_path, "cache_manifest.json")

    with open(manifest_path, "w") as f:
        f.write(manifest_content)

    return None


def _write_to_disk(file, digested_file_path, gzip_files, input_path):
    full_digested_file_path = os.path.join(input_path, digested_file_path)

    # Copy file while preserving permissions and meta data if supported.
    shutil.copy2(file, full_digested_file_path)

    if gzip_files:
        with open(file, "rb") as f_in:
            with gzip.open(f"{file}.gz", "wb") as f_out:
                shutil.copyfileobj(f_in, f_out)

        with open(full_digested_file_path, "rb") as f_in:
            with gzip.open(f"{full_digested_file_path}.gz", "wb") as f_out:
                shutil.copyfileobj(f_in, f_out)

    return None
