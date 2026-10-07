"""Carrega o motor resvg_py do pacote, sem pip, rede ou programas externos."""
from contextlib import contextmanager
import hashlib
import importlib.util
import json
from pathlib import Path
import platform
import sys
import sysconfig
import tempfile
from zipfile import ZipFile

ASSETS = Path(__file__).resolve().parents[1] / 'assets/renderizador'


def plataforma_wheel():
    if sys.implementation.name != 'cpython' or sys.version_info < (3, 10):
        raise RuntimeError('Usar CPython 3.10 ou superior para o motor incluído.')
    if sysconfig.get_config_var('Py_GIL_DISABLED'):
        raise RuntimeError('O motor incluído exige CPython convencional, com GIL.')
    arch = platform.machine().lower()
    arch = {'amd64': 'x86_64', 'arm64': 'aarch64'}.get(arch, arch)
    system = platform.system()
    if sys.maxsize <= 2**32:
        raise RuntimeError('O pacote de renderização exige Python de 64 bits.')
    if system == 'Linux':
        libc, version = platform.libc_ver()
        if libc == 'glibc':
            if tuple(int(x) for x in version.split('.')[:2]) < (2, 17):
                raise RuntimeError('Usar Linux com glibc 2.17 ou superior.')
            return {'x86_64': 'manylinux_2_17_x86_64.manylinux2014_x86_64', 'aarch64': 'manylinux_2_17_aarch64.manylinux2014_aarch64'}.get(arch)
        if any(Path('/lib').glob('ld-musl-*.so.1')):
            return {'x86_64': 'musllinux_1_2_x86_64', 'aarch64': 'musllinux_1_2_aarch64'}.get(arch)
        raise RuntimeError('Biblioteca C do Linux não identificada como glibc ou musl.')
    if system == 'Windows':
        return {'x86_64': 'win_amd64', 'aarch64': 'win_arm64'}.get(arch)
    if system == 'Darwin':
        return {'x86_64': 'macosx_10_12_x86_64', 'aarch64': 'macosx_11_0_arm64'}.get(arch)
    return None


@contextmanager
def carregar_renderizador():
    tag = plataforma_wheel()
    if not tag:
        raise RuntimeError(f'Plataforma sem motor incluído: {platform.system()} {platform.machine()}.')
    manifest = json.loads((ASSETS / 'manifesto-renderizador.json').read_text(encoding="utf-8"))
    name = f"resvg_py-{manifest['versao']}-cp310-abi3-{tag}.whl"
    record = next((r for r in manifest['wheels'] if r['arquivo'] == name), None)
    if record is None:
        raise RuntimeError(f'Motor ausente no pacote: {name}')
    wheel = ASSETS / name
    if hashlib.sha256(wheel.read_bytes()).hexdigest() != record['sha256']:
        raise ValueError(f'Motor divergente: {wheel}')
    # O arquivo é extraído apenas para carregar a extensão nativa na memória.
    # Nada é instalado no Python do usuário ou na pasta da skill.
    with tempfile.TemporaryDirectory(prefix='resvg-skill-', ignore_cleanup_errors=True) as tmp:
        dest = Path(tmp)
        with ZipFile(wheel) as archive:
            for item in archive.infolist():
                target = (dest / item.filename).resolve()
                if not target.is_relative_to(dest):
                    raise ValueError('Caminho inválido no pacote do motor.')
            archive.extractall(dest)
        module_name = '_resvg_skill_incluido'
        spec = importlib.util.spec_from_file_location(module_name, dest / 'resvg_py/__init__.py', submodule_search_locations=[str(dest / 'resvg_py')])
        if spec is None or spec.loader is None:
            raise RuntimeError('Não foi possível carregar o motor incluído.')
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        try:
            spec.loader.exec_module(module)
            yield module, {'motor': manifest['motor'], 'versao': manifest['versao'], 'wheel': record['arquivo'], 'sha256': record['sha256'], 'plataforma': tag}
        finally:
            for key in list(sys.modules):
                if key == module_name or key.startswith(module_name + '.'):
                    sys.modules.pop(key, None)
