import click

@click.group()
def test():
    """Pyrmm Test Command group"""
    pass

from pyrmm.cli.test.github import github
test.add_command(github)
"""
github 连接性测试
"""

from pyrmm.cli.test.basic import basic
test.add_command(basic)
"""
基本测试命令 -- 依赖于 shellcheck 工具
"""

