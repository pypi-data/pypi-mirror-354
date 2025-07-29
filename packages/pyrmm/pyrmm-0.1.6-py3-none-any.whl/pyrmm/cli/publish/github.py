import click

@click.command()
@click.argument("project_path", default=".", required=False)
@click.option("--tag", "-t", help="Release标签名，默认使用项目版本 (例如: v1.0.0)")
@click.option("--name", "-n", help="Release名称，默认使用标签名")
@click.option("--body", "-b", help="Release描述")
@click.option("--draft", is_flag=True, help="创建为草稿")
@click.option("--prerelease", is_flag=True, help="标记为预发布版本")
@click.option("--dry-run", is_flag=True, help="模拟运行，不实际创建Release和上传文件")
@click.option("--no-proxy", is_flag=True, help="不添加代理加速链接到Release描述")
@click.pass_context
def github(ctx: click.Context, project_path: str, tag: str, name: str, body: str,
          draft: bool, prerelease: bool, dry_run: bool, no_proxy: bool) -> None:
    """发布到GitHub"""
    from pyrmm.usr.lib.project import RmmProject
    from pyrmm.usr.lib.git import RmmGit
    from pyrmm.usr.lib.proxy import ProxyManager
    from pathlib import Path

    token = ctx.obj.get('token', None)
    auto_yes = ctx.obj.get('yes', False)
    
    if auto_yes:
        click.echo("🤖 自动模式: 已启用 --yes 参数，将自动同意所有确认提示")
    
    try:# 安全检查：防止将GitHub token误用为tag
        if tag and (tag.startswith('ghp_') or tag.startswith('github_pat_') or len(tag) > 50):
            click.echo("🚨 安全警告：检测到可能的GitHub token！")
            click.echo("💡 您是否想要使用 --token 参数而不是 --tag？")
            click.echo("📋 正确用法:")
            click.echo("   rmm publish --token YOUR_TOKEN github .")
            click.echo("   rmm publish --token YOUR_TOKEN github --tag v1.0.0 .")
            click.echo("❌ 为了安全考虑，操作已取消。")
            return
        
        # 解析项目路径
        if project_path == ".":
            project_dir = Path.cwd()
        else:
            project_dir = Path(project_path).resolve()
            if not project_dir.exists():
                # 尝试作为项目名解析
                try:
                    project_dir = RmmProject.project_path(project_path)
                except Exception:
                    click.echo(f"❌ 项目路径不存在: {project_path}")
                    return
        
        click.echo(f"🔍 项目目录: {project_dir}")
        
        # 检查项目是否为Git仓库
        git_info = RmmGit.get_repo_info(project_dir)
        if not git_info:
            click.echo("❌ 当前目录不是Git仓库")
            return
        
        # 检查是否有origin远程仓库
        if 'origin' not in git_info.remotes:
            click.echo("❌ 未找到origin远程仓库")
            return
        
        origin_info = git_info.remotes['origin']
        if not origin_info.username or not origin_info.repo_name:
            click.echo(f"❌ 无法解析GitHub仓库信息: {origin_info.url}")
            return
        
        click.echo(f"📦 GitHub仓库: {origin_info.username}/{origin_info.repo_name}")        # 获取GitHub token
        github_token: str | None = token
        if not github_token:
            github_token = ctx.obj.get('token', None)
            if not github_token:
                click.echo(" rmm test github --TOKEN YOUR_GITHUB_ACCESS_TOKEN")
                click.echo("❌ 未提供GitHub访问令牌。请设置GITHUB_ACCESS_TOKEN环境变量或使用--token参数")
                click.echo("💡 GitHub token 需要以下权限:")
                click.echo("   - repo (完整仓库权限)")
                click.echo("   - contents:write (写入内容)")
                click.echo("   - metadata:read (读取元数据)")
                click.echo("🔗 创建token: https://github.com/settings/tokens/new")
                return
        
        # 验证GitHub token权限
        click.echo("🔑 验证GitHub访问权限...")
        if not RmmGit.check_repo_exists(origin_info.username, origin_info.repo_name, github_token):
            click.echo(" rmm test github --TOKEN YOUR_GITHUB_ACCESS_TOKEN")
            click.echo("❌ 无法访问GitHub仓库，请检查:")
            click.echo("   1. 仓库是否存在且可访问")
            click.echo("   2. GitHub token 是否有效")
            click.echo("   3. Token 是否有足够权限 (repo权限)")
            click.echo("🔗 检查token权限: https://github.com/settings/tokens")
            return
          # 检查仓库状态
        if not git_info.is_clean:
            click.echo("⚠️  警告: Git仓库有未提交的更改")
            if not auto_yes and not click.confirm("继续发布？", default=True):
                return
        
        # 检查构建输出目录
        dist_dir = project_dir / ".rmmp" / "dist"
        if not dist_dir.exists():
            click.echo("❌ 构建输出目录不存在: .rmmp/dist/")
            click.echo("请先运行构建命令: rmm build")
            return          # 收集要上传的文件（只处理模块包文件，忽略源代码文件）
        asset_files: list[Path] = []
        for file_path in dist_dir.rglob("*"):
            if file_path.is_file():
                # 只包含模块包文件，排除源代码压缩包
                if file_path.suffix.lower() == '.zip':
                    asset_files.append(file_path)
                elif file_path.name.endswith('.tar.gz'):
                    click.echo(f"🔍 跳过源代码文件: {file_path.relative_to(dist_dir)}")
                    continue
                else:
                    # 其他文件类型也包含（如果有的话）
                    asset_files.append(file_path)
        
        if not asset_files:
            click.echo("❌ 构建输出目录为空: .rmmp/dist/")
            return
          # 检查是否有多个文件，强制清理
        if len(asset_files) > 1:
            click.echo(f"⚠️  发现 {len(asset_files)} 个构建文件:")
            for asset in asset_files:
                click.echo(f"  - {asset.relative_to(dist_dir)}")
            
            click.echo("📋 发布时只能包含一个构建文件，请选择操作:")
            click.echo("  1. 清理旧文件并重新构建")
            click.echo("  2. 取消发布")
            
            if auto_yes or click.confirm("是否清理旧文件并重新构建？", default=True):
                click.echo("🧹 清理旧文件...")
                for asset in asset_files:
                    asset.unlink()
                    click.echo(f"删除: {asset.relative_to(dist_dir)}")
                
                # 自动调用构建命令
                click.echo("🔨 自动重新构建...")
                from pyrmm.cli.build import build
                  # 创建新的context来调用build命令
                build_ctx = click.Context(build, obj=ctx.obj)
                try:
                    build_ctx.invoke(build, project_name=project_dir.name)
                    click.echo("✅ 重新构建完成，继续发布流程...")
                      # 重新收集构建文件（应用相同的过滤逻辑）
                    asset_files = []
                    for file_path in dist_dir.rglob("*"):
                        if file_path.is_file():
                            # 只包含模块包文件，排除源代码压缩包
                            if file_path.suffix.lower() == '.zip':
                                asset_files.append(file_path)
                            elif file_path.name.endswith('.tar.gz'):
                                continue  # 跳过源代码文件
                            else:
                                # 其他文件类型也包含（如果有的话）
                                asset_files.append(file_path)
                    
                    if not asset_files:
                        click.echo("❌ 重新构建后仍然没有输出文件")
                        return
                        
                except Exception as e:
                    click.echo(f"❌ 重新构建失败: {e}")
                    click.echo("请手动运行构建命令: rmm build")
                    return
            else:
                click.echo("❌ 发布已取消")
                return
        
        click.echo(f"📁 找到 {len(asset_files)} 个文件待上传:")
        for asset in asset_files:
            click.echo(f"  - {asset.relative_to(dist_dir)}")# 确定标签名
        if not tag:
            try:
                # 尝试从项目配置获取版本
                project_info = RmmProject.project_info(project_dir)
                if 'version' in project_info and project_info['version']:
                    version: str  = project_info['version'] if isinstance(project_info['version'], str) else "1.0.0"
                    # 确保版本号以v开头，但不重复添加
                    if not version.startswith('v'):
                        tag = f"v{version}"
                    else:
                        tag = version
                else:
                    tag = "v1.0.0"
            except Exception:
                tag = "v1.0.0"

        # 确定release名称
        if not name:
            name = tag
          # 确定release描述        if not body:
            # 尝试获取最新提交信息
            commit_info = RmmGit.get_commit_info(project_dir)
            if commit_info:
                body = f"Release {tag}\n\n最新提交: {commit_info['message']}"
            else:
                body = f"Release {tag}"
        
        # 添加代理下载链接到 release 描述中
        if asset_files and not no_proxy:
            # 获取并保存代理信息（如果还没有的话）
            click.echo("🌐 获取代理节点信息...")
            proxy_success = False
            try:
                proxies, proxy_file = ProxyManager.get_and_save_proxies(project_dir)
                click.echo(f"✅ 获取到 {len(proxies)} 个代理节点，已保存到 {proxy_file.relative_to(project_dir)}")
                proxy_success = True
            except Exception as e:
                click.echo(f"⚠️  获取代理信息失败: {e}，将不添加代理下载链接")
                proxy_success = False            # 生成统一的代理下载链接段落
            proxy_section: str = ""
            
            if proxy_success:
                try:
                    # 构建文件下载链接列表
                    file_download_pairs: list[tuple[str, str]] = []
                    for asset_file in asset_files:
                        download_url = f"https://github.com/{origin_info.username}/{origin_info.repo_name}/releases/download/{tag}/{asset_file.name}"
                        file_download_pairs.append((asset_file.name, download_url))
                    
                    # 生成统一的代理链接段落
                    proxy_section = ProxyManager.generate_unified_proxy_links(project_dir, file_download_pairs)
                    if proxy_section:
                        click.echo(f"✅ 已生成统一代理下载链接段落（包含 {len(asset_files)} 个文件）")
                    else:
                        click.echo("⚠️  代理链接生成失败")
                except Exception as e:
                    click.echo(f"⚠️  代理链接生成异常: {e}")
            
            # 将代理链接段落添加到描述中
            if proxy_section:
                body = f"{body}\n\n{proxy_section}"
                click.echo("✅ 已将代理加速链接添加到Release描述中")
            else:
                click.echo("⚠️  没有生成代理链接，Release将不包含代理下载地址")
        elif no_proxy:
            click.echo("🚫 已禁用代理加速链接")
        
        click.echo(f"🏷️  标签: {tag}")
        click.echo(f"📋 名称: {name}")
        click.echo(f"📝 描述: {body}")
        
        if dry_run:
            click.echo("🔍 模拟运行模式 - 不会实际创建Release或上传文件")
            click.echo(f"📊 模拟发布到: {origin_info.username}/{origin_info.repo_name}")
            click.echo("✅ 模拟运行完成")
            return        # 确认发布
        if not auto_yes and not click.confirm(f"确定要发布到 {origin_info.username}/{origin_info.repo_name}？", default=True):
            return
        
        # 检查release是否已存在
        existing_release = RmmGit.get_release_by_tag(
            origin_info.username, 
            origin_info.repo_name, 
            tag, 
            github_token
        )
        
        if existing_release:
            click.echo(f"⚠️  Release {tag} 已存在")
            if not auto_yes and not click.confirm("是否要上传文件到现有Release？",default=True):
                return
            release_info = existing_release
        else:
            # 创建新release
            click.echo(f"🚀 创建Release: {tag}")
            release_info = RmmGit.create_release(
                origin_info.username,
                origin_info.repo_name,
                tag,
                name,
                body,
                draft,
                prerelease,
                github_token            
                )
            
            if not release_info:
                click.echo("❌ 创建Release失败")
                click.echo("\n💡 可能的解决方案:")
                click.echo("   1. 检查GitHub token权限 (需要 repo 权限)")
                click.echo("   2. 确认标签不重复")
                click.echo("   3. 检查网络连接")
                click.echo("   4. 手动在GitHub上创建Release后重新运行")
                click.echo(f"\n🔗 手动创建Release: https://github.com/{origin_info.username}/{origin_info.repo_name}/releases/new")
                return
            
            click.echo(f"✅ Release创建成功: {release_info['html_url']}")
        
        # 上传文件
        click.echo("📤 开始上传文件...")
        success = RmmGit.upload_release_assets(
            origin_info.username,
            origin_info.repo_name,
            tag,
            asset_files,
            github_token
        )
        
        if success:
            click.echo(f"🎉 发布成功! 访问: {release_info['html_url']}")
        else:
            click.echo("❌ 文件上传失败，试试：rmm sync.如果还不行，试试rmm test github")
            
    except Exception as e:
        click.echo(f"❌ 发布过程中出错: {e}")
        import traceback
        traceback.print_exc()