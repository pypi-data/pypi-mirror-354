import click

@click.command()
@click.option("--token", envvar="GITHUB_ACCESS_TOKEN", help="GitHub访问令牌，默认从环境变量GITHUB_ACCESS_TOKEN获取")
def repo(token: str):
    """发布RMM 模块提交PR 到RMM GitHub仓库"""
    RMM_REPO = "https://github.com/LIghtJUNction/RMMREPO.git"
    # 提交路径： $RMM_REPO/USERNAME/MODULE_ID/id-tag.zip
    # 本地文件： ./dist/id-tag.zip

    

