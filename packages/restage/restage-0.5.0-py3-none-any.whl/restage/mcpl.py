from pathlib import Path


def mcpl_real_filename(filename: Path) -> Path:
    """MCPL_output from McCode instruments has the bad habit of changing the output file name silently.
    Find the _real_ output file name by looking for the expected variants"""
    if filename.exists() and filename.is_file():
        return filename
    if filename.with_suffix('.mcpl').exists() and filename.with_suffix('.mcpl').is_file():
        return filename.with_suffix('.mcpl')
    if filename.with_suffix('.mcpl.gz').exists() and filename.with_suffix('.mcpl.gz').is_file():
        return filename.with_suffix('.mcpl.gz')
    raise FileNotFoundError(f'Could not find MCPL file {filename}')


# def mcpl_particle_count(filename):
    # from mcpl import MCPLFile
    # with MCPLFile(mcpl_real_filename(filename)) as f:
    #     n = f.nparticles
    # return n


def mcpl_particle_count(filename):
    """Call the MCPL command line tool to get the number of particles in an MCPL file"""
    # There _is_ a Python module for reading MCPL files, but it doesn't close file handles!
    from subprocess import run, PIPE
    import re
    command = ['mcpltool', '--justhead', str(mcpl_real_filename(filename))]
    result = run(command, stdout=PIPE)
    if result.returncode != 0:
        raise RuntimeError(f'mcpltool failed with return code {result.returncode}')
    info = result.stdout.decode('utf-8')
    r = re.compile(r'No\. of particles\s*:\s*(\d+)')
    m = r.search(info)
    if m is None:
        raise RuntimeError(f'Could not find number of particles in {info}')
    return int(m.group(1))


def mcpl_merge_files(files: list[Path], filepath: Path, keep_originals: bool = False):
    """Merge a list of MCPL files into a single file using mcpltool.

    :param files: The list of files to merge.
    :param filename: The name of the output file.
    :param keep_originals: Whether to keep the original files.

    :raises RuntimeError: If mcpltool fails.

    :note: This function is not thread-safe.
        A future version of the Python mcpl package might include a merge function.
    """
    from subprocess import run
    real_filenames = [mcpl_real_filename(f) for f in files]
    # if the real filenames have .mcpl or .mcpl.gz, the merged filename should too
    ext = ''
    if real_filenames[0].name.endswith('.mcpl.gz'):
        ext = '.mcpl.gz'
    elif real_filenames[0].name.endswith('.mcpl'):
        ext = '.mcpl'
    filename = filepath.with_suffix(ext).as_posix()

    command = ['mcpltool', '--merge', filename] + [str(f) for f in real_filenames]
    result = run(command)
    if result.returncode != 0:
        raise RuntimeError(f'mcpltool failed with return code {result.returncode} for command {" ".join(command)}')
    if not keep_originals:
        for file in real_filenames:
            file.unlink()


def mcpl_rename_file(source: Path, dest: Path, strict: bool = False):
    filepath = mcpl_real_filename(source)
    filename = filepath.name  # this could be '{name}', '{name}.mcpl', or '{name}.mcpl.gz'
    ext = ''
    if filepath.name.endswith('.mcpl.gz'):
        ext = '.mcpl.gz'
    elif filepath.name.endswith('.mcpl'):
        ext = '.mcpl'

    if not dest.name.endswith(ext):
        if strict:
            raise RuntimeError(f"Destination {dest} does not have extension matching {source}")
        dest = dest.with_suffix(ext)

    filepath.rename(dest)
    return dest
