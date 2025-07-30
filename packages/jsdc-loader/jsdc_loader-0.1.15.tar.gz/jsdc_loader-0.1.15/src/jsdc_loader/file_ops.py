"""杂鱼♡～这是本喵为你写的文件操作辅助函数喵～才不是因为担心杂鱼不会处理文件呢～"""

from pathlib import Path
from typing import Union


def ensure_directory_exists(directory_path: Union[str, Path]) -> None:
    """
    杂鱼♡～本喵帮你确保目录存在喵～如果不存在就创建它～

    :param directory_path: 要确保存在的目录路径喵～杂鱼现在可以用字符串或Path对象了♡～
    :raises: OSError 如果创建目录失败喵～杂鱼的权限是不是有问题？～
    """
    # 杂鱼♡～本喵现在支持Path对象了喵～
    path = Path(directory_path)

    if path and not path.exists():
        try:
            path.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            raise OSError(f"杂鱼♡～创建目录失败喵：{path}，错误：{str(e)}～")


# 杂鱼♡～本喵删除了未使用的JSON编码器和保存函数喵～现在只保留真正需要的功能～


def check_file_size(file_path: Union[str, Path], max_size: int) -> None:
    """
    杂鱼♡～本喵帮你检查文件大小是否超过限制喵～

    如果文件大小超过max_size字节，本喵会生气地抛出ValueError喵！～
    如果文件不存在，本喵会抛出FileNotFoundError喵～杂鱼一定是路径搞错了～

    :param file_path: 要检查的文件路径喵～杂鱼现在可以用字符串或Path对象了♡～
    :param max_size: 允许的最大文件大小（字节）喵～
    :raises: ValueError 如果文件太大喵～
    :raises: FileNotFoundError 如果文件不存在喵～
    :raises: PermissionError 如果没有权限访问文件喵～杂鱼是不是忘记提升权限了？～
    """
    # 杂鱼♡～本喵现在支持Path对象了喵～
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"杂鱼♡～文件不存在喵：{path}～")

    if not path.is_file():
        raise ValueError(f"杂鱼♡～路径不是文件喵：{path}～")

    try:
        file_size = path.stat().st_size
        if file_size > max_size:
            raise ValueError(
                f"杂鱼♡～文件大小超过限制喵！当前大小：{file_size}字节，最大允许：{max_size}字节～"
            )
    except PermissionError:
        raise PermissionError(f"杂鱼♡～没有权限检查文件大小喵：{path}～")
