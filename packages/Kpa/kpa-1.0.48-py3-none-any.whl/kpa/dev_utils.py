import time, random, sys, argparse, os, subprocess as subp, re
from pathlib import Path
from functools import wraps
from typing import Optional,Iterator,List

class ExecutableNotFound(Exception): pass


# TODO: Instead of listing what to ignore, list what to include
flake8_ignore_strict  = 'B007,E116,E124,E126,E127,E128,E129,E201,E202,E203,E221,E222,E225,E226,E227,E228,E231,E241,E251,E252,E261,E265,E266,E301,E302,E303,E305,E306,E401,E402,E501,E701,E702,E704,F401,F811,W292,W293,W391,W504'
flake8_ignore_default = flake8_ignore_strict + ',E115,E122,E242,E262,E271,E274,E713,E722,E741,W191,W291'


def lint_cli(argv:List[str]) -> int:  # returns a ReturnCode
    parser = argparse.ArgumentParser(prog='kpa lint')
    parser.add_argument('files', nargs='*', help='If no files are passed, this uses **/*.py')
    #parser.add_argument('--no-mypy-cache', action='store_true', help="Don't make .mypy_cache/")  # Conflicts with `--install-types`.  Consider using `--cache-dir=/tmp/{slugify(abspaths(args.files))}`.
    parser.add_argument('--run-rarely', action='store_true', help="Only when file is modified in last 30 seconds, or otherwise 1%% of the time")
    parser.add_argument('--flake8-only', action='store_true', help="Run flake8 and not mypy")
    parser.add_argument('--flake8-strict', action='store_true', help="Run non-essential checks in flake8")
    parser.add_argument('--extra-flake8-ignores', help="Extra errors/warnings for flake8 to ignore")
    parser.add_argument('--venv-bin-dir', help="A path to venv/bin that has flake8 or mypy")
    parser.add_argument('--verbose', action='store_true')
    parser.add_argument('--watch', action='store_true', help='Watch files, and re-lint when files are updated')
    args = parser.parse_args(argv)
    if not args.files: args.files = list(get_all_py_files())
    return _lint_cli(args)
def _lint_cli(args:argparse.Namespace) -> int:
    if args.watch:
        from .watcher import yield_when_files_update
        args.watch = False
        for changeset in yield_when_files_update(args.files, and_also_immediately=True):
            if changeset is not None: print('\n'*5)
            if len(args.files)<5: print(f'=====> linting {args.files}...')
            else: print(f'=====> linting {len(args.files)} files...')
            _lint_cli(args)
            print('.')
        return 0

    if args.run_rarely:
        seconds_since_last_change = time.time() - max(Path(path).stat().st_mtime for path in args.files)
        if seconds_since_last_change > 30 and random.random() > 0.01: exit(0)

    def find_exe(name:str) -> str:
        for path in find_exe_options(name):
            if os.path.exists(path): return path
        print(f"[Failed to find {name}]")
        raise ExecutableNotFound()
    def find_exe_options(name:str) -> Iterator[str]:
        if args.venv_bin_dir: yield f'{args.venv_bin_dir}/{name}'
        yield f'{os.path.dirname(sys.executable)}/{name}'
        yield f'{os.path.dirname(sys.argv[0])}/{name}'
        try: yield subp.check_output(['which',name], stderr=subp.DEVNULL).decode().strip()
        except Exception: pass
        yield f'venv/bin/{name}'
        for file in args.files: yield f'{os.path.dirname(os.path.abspath(file))}/venv/bin/{name}'
    def print_and_run(cmd:List[str]) -> int:  # Returns the returncode
        if args.verbose: print('=>', cmd)
        p = subp.run(cmd)
        if p.returncode != 0: print(f"\n{cmd[0]} failed")
        return p.returncode

    flake8_ignore = (flake8_ignore_strict if args.flake8_strict else flake8_ignore_default) + (f',{args.extra_flake8_ignores}' if args.extra_flake8_ignores else '')
    try: flake8_exe = find_exe('flake8')
    except ExecutableNotFound: print("flake8 not found"); return 11
    retcode = print_and_run([flake8_exe, '--show-source', f'--ignore={flake8_ignore}', *args.files])
    if retcode != 0 or args.flake8_only: return retcode

    try: mypy_exe = find_exe('mypy')
    except ExecutableNotFound: print("mypy not found"); return 12
    return print_and_run([mypy_exe, '--pretty', '--ignore-missing-imports', '--non-interactive', '--install-types', *args.files])


def lint(filepath:str = '', make_cache:bool = True, run_rarely:bool = False) -> None:
    if run_rarely:
        seconds_since_last_change = time.time() - Path(filepath).stat().st_mtime
        if seconds_since_last_change > 30 and random.random() > 0.01:
            return  # Don't run
    lint_flake8(filepath)
    lint_mypy(filepath, make_cache=make_cache)
run = lint

def lint_flake8(filepath:str = '') -> None:
    try: flake8_exe = find_exe('flake8', filepath=filepath)
    except ExecutableNotFound: return None
    p = subp.run([flake8_exe, '--show-source', f'--ignore={flake8_ignore_default}', filepath])
    if p.returncode != 0: sys.exit(1)

def lint_mypy(filepath:str = '', make_cache:bool = True) -> None:
    try: mypy_exe = find_exe('mypy', filepath=filepath)
    except ExecutableNotFound: return None
    cmd = [mypy_exe, '--pretty', '--ignore-missing-imports']
    if not make_cache: cmd.append('--cache-dir=/dev/null')
    if filepath: cmd.append(filepath)
    p = subp.run(cmd)
    if p.returncode != 0: sys.exit(1)

def find_exe(name:str, filepath:str = '') -> str:
    for path in find_exe_options(name, filepath=filepath):
        if os.path.exists(path): return path
    print(f"[Failed to find {name}]")
    raise ExecutableNotFound()
def find_exe_options(name:str, filepath:str = '') -> Iterator[str]:
    try: yield subp.check_output(['which',name], stderr=subp.DEVNULL).decode().strip()
    except Exception: pass
    yield f'venv/bin/{name}'
    if filepath: yield f'{os.path.dirname(os.path.abspath(filepath))}/venv/bin/{name}'

def get_all_py_files(directory_:Optional[str] = None) -> Iterator[str]:
    directory = Path(directory_) if directory_ else Path().absolute()
    for filepath in directory.rglob('*.py'):
        if '#' in filepath.name: continue
        rel_path = filepath.relative_to(directory)
        if any(str(name).startswith('.') and str(name)!='.' for name in rel_path.parents): continue
        if re.search(r'(^|/)build/lib/', str(rel_path)): continue
        if re.search(r'(^|/)venv/', str(rel_path)): continue
        yield str(filepath)


def get_size(obj, seen:Optional[set] = None) -> int:
    """Recursively calculates bytes of RAM taken by object"""
    # From https://code.activestate.com/recipes/577504/ and https://github.com/bosswissam/pysize/blob/master/pysize.py
    if seen is None: seen = set()
    size = sys.getsizeof(obj)
    obj_id = id(obj)
    if obj_id in seen:
        return 0
    seen.add(obj_id)  # Mark as seen *before* recursing to handle self-referential objects

    if isinstance(obj, dict):
        size += sum(get_size(v, seen) for v in obj.values())
        size += sum(get_size(k, seen) for k in obj.keys())
    elif hasattr(obj, '__dict__'):
        size += get_size(obj.__dict__, seen)
    elif hasattr(obj, '__iter__') and not isinstance(obj, (str, bytes, bytearray)):
        size += sum(get_size(i, seen) for i in obj)

    if hasattr(obj, '__slots__'):  # obj can have both __slots__ and __dict__
        size += sum(get_size(getattr(obj, s), seen) for s in obj.__slots__ if hasattr(obj, s))

    return size
