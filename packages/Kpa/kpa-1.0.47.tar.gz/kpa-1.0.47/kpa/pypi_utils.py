from pathlib import Path
import urllib.request
import subprocess, json, sys, types, importlib.util
from typing import Union


def upload_package(package_name:str, current_version:str='') -> None:
    package_name = package_name.lower()

    version_path = Path(f'{package_name}/version.py')
    if not current_version:
        current_version = load_module_from_path(version_path).version
    assert current_version, current_version

    # Make sure there's no unstaged changes
    git_workdir_returncode = subprocess.run('git diff-files --quiet'.split()).returncode
    assert git_workdir_returncode in [0,1]
    if git_workdir_returncode == 1:
        print('=> git workdir has changes')
        print('=> please either revert or stage them')
        sys.exit(1)

    # If the local version is the same as the PyPI version, increment it.
    pypi_url = f'https://pypi.python.org/pypi/{package_name}/json'
    latest_version = json.loads(urllib.request.urlopen(pypi_url).read())['info']['version']
    # Note: it takes pypi a minute to update the API, so this can be wrong.
    if latest_version == current_version:
        new_version = next_version(current_version)
        print(f'=> autoincrementing version {current_version} -> {new_version}')
        version_path.write_text(f"version = '{new_version}'\n")
        current_version = new_version
        subprocess.run(['git','stage',f'{package_name}/version.py'], check=True)

    # Commit any staged changes
    git_index_returncode = subprocess.run('git diff-index --quiet --cached HEAD'.split()).returncode
    assert git_index_returncode in [0,1]
    if git_index_returncode == 1:
        print('=> git index has changes; committing them')
        subprocess.run(['git','commit','-m',current_version], check=True)

    # Clean and repopulate ./dist/*
    if Path('dist').exists() and list(Path('dist').iterdir()):
        # Double check that we are where we think we are
        setuppy = Path('dist').absolute().parent / 'setup.py'
        assert setuppy.is_file() and package_name in setuppy.read_text().lower()
        for child in Path('dist').absolute().iterdir():
            assert child.name.lower().startswith(f'{package_name}-'), child
            print('=> unlinking', child)
            child.unlink()
    subprocess.run('python3 setup.py sdist bdist_wheel'.split(), check=True)

    # Upload
    if not Path('~/.pypirc').expanduser().exists():
        print('=> warning: you need a ~/.pypirc')
    try: subprocess.run(['twine','--version'], check=True)
    except Exception: print('Run `pip3 install twine` and try again'); sys.exit(1)
    subprocess.run('twine upload dist/*'.split(), check=True)

    if git_index_returncode == 1:
        print('=> Now do `git push`.')


def next_version(version:str) -> str:
    version_parts = version.split('.')
    version_parts[-1] = str(1+int(version_parts[-1]))
    return '.'.join(version_parts)
assert next_version('1.1.9') == '1.1.10'
assert next_version('0.0') == '0.1'


def load_module_from_path(filepath:Union[str,Path], module_name:str='') -> types.ModuleType:
    if not module_name: module_name = Path(filepath).name.removesuffix('.py')
    spec = importlib.util.spec_from_file_location(module_name, str(filepath)); assert spec and spec.loader, filepath
    module = importlib.util.module_from_spec(spec); assert module, filepath
    spec.loader.exec_module(module)
    return module
