# Standard library imports
from pathlib import Path
# import os
# import toml

# Third-party imports
# from yors_pano_ansi_color import info_status, info_step, msg_padd, log_msg

# feat(core): path_resolve - resolve path to absolute path with root path
def path_resolve(path: str,root:str):
    """
    resolve path to absolute path with root path

    INIT_PY_REl='../'
    root = path_resolve(INIT_PY_REl,str(Path(__file__)))
    path_resolve(root,'pyproject.toml')
    """
    return str(Path(root).joinpath(path).resolve().as_posix())

# feat(core): path_dirname - get dirname of path
def path_dirname(path: str):
    """
    get dirname of path

    path_dirname("/root/dir/file.txt") # "/root/dir"
    """
    return str(Path(path).parent.as_posix())

# feat(core): path_unix - convert path to unix path
def path_unix(input_path:str):
    """
    convert path to unix path
    """
    path = Path(input_path)
    unix_path = str(path.as_posix())
    return (unix_path,)


# feat(core): path_parse - parse path to name, stem, suffix, parent
def path_parse(path:str):
    """
    parse path to name, stem, suffix, parent

    name, stem, suffix, parent=path_parse(root)
    """
    flag = Path(path)
    name = flag.name
    stem = flag.stem
    suffix = flag.suffix
    parent = str(flag.parent.as_posix())
    return (name, stem, suffix, parent)

# feat(core): path_comfy_get - Get ComfyUI models directory path by traversing up from specified path
def path_comfy_get(start_path: str = None, levels_or_path = 3,name:str='models') -> str:
    """
    Get ComfyUI models directory path by traversing up from specified path
    
    path_comfy_get(__file__,'../../models')

    path_comfy_get(__file__,2,'models')
    """
    current_dir = Path(start_path if start_path else __file__).parent
    
    if isinstance(levels_or_path, int):
        target_dir = current_dir
        for _ in range(levels_or_path):
            target_dir = target_dir.parent
        models_dir = target_dir / name
    else:
        models_dir = (current_dir / levels_or_path).resolve()
    
    return str(models_dir.absolute().as_posix())