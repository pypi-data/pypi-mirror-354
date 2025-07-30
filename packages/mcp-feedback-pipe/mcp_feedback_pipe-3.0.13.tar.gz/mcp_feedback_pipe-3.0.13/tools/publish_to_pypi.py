#!/usr/bin/env python
"""
MCP反馈通道 - PyPI发布脚本
用于将项目发布到Python Package Index (PyPI)
支持版本管理和自动更新
"""

import os
import sys
import subprocess
import getpass
import json
from pathlib import Path
from dotenv import load_dotenv

# 导入版本管理器
try:
    from version_manager import VersionManager
    VERSION_MANAGER_AVAILABLE = True
except ImportError:
    print("⚠️  版本管理器不可用，将使用基础功能")
    VERSION_MANAGER_AVAILABLE = False

def mask_token(cmd):
    """脱敏token信息"""
    if "--token" in cmd:
        parts = cmd.split()
        for i, part in enumerate(parts):
            if part == "--token" and i + 1 < len(parts):
                token = parts[i + 1]
                if token.startswith("pypi-") and len(token) > 10:
                    # 只显示前缀和后4位，中间用*代替
                    masked = f"pypi-{'*' * (len(token) - 9)}{token[-4:]}"
                    parts[i + 1] = masked
                break
        return " ".join(parts)
    return cmd

def run_command(cmd, check=True, mask_sensitive=False):
    """运行命令并返回结果"""
    display_cmd = mask_token(cmd) if mask_sensitive else cmd
    print(f"🔧 执行: {display_cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if check and result.returncode != 0:
        print(f"❌ 命令失败: {result.stderr}")
        sys.exit(1)
    return result

def check_dependencies():
    """检查发布依赖"""
    print("🔍 检查发布依赖...")
    
    # 检查uv
    result = run_command("uv --version", check=False)
    if result.returncode != 0:
        print("❌ uv未安装，正在安装...")
        run_command("pip install uv")
        print("✅ uv安装完成")
    else:
        print(f"✅ uv已安装: {result.stdout.strip()}")

def get_project_info():
    """获取项目信息"""
    print("📋 读取项目信息...")
    
    # 读取pyproject.toml
    pyproject_path = Path("pyproject.toml")
    if not pyproject_path.exists():
        print("❌ 未找到pyproject.toml文件")
        sys.exit(1)
    
    with open(pyproject_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 简单解析版本号（更健壮的方式应该用toml库）
    for line in content.split('\n'):
        if line.strip().startswith('version ='):
            version = line.split('=')[1].strip().strip('"\'')
            break
    else:
        print("❌ 未找到版本号")
        sys.exit(1)
    
    return {
        "name": "mcp-feedback-pipe",
        "version": version
    }

def prepare_package_structure():
    """准备包结构 - 自动配置入口点并确保必要文件存在"""
    print("📦 准备包结构...")
    
    # 检查server.py是否存在，如果不存在就从backend/server.py复制
    server_py = Path("server.py")
    backend_server_py = Path("backend/server.py")
    
    if not server_py.exists():
        if backend_server_py.exists():
            print("🔧 从backend/server.py复制到根目录...")
            import shutil
            shutil.copy2(backend_server_py, server_py)
            print("✅ server.py已复制到根目录")
        else:
            print("❌ 未找到server.py文件（根目录或backend/目录）")
            sys.exit(1)
    
    # 读取当前的pyproject.toml
    pyproject_path = Path("pyproject.toml")
    if not pyproject_path.exists():
        print("❌ 未找到pyproject.toml文件")
        sys.exit(1)
    
    with open(pyproject_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查当前的入口点配置
    import re
    
    # 查找 [project.scripts] 部分
    scripts_pattern = r'(\[project\.scripts\]\s*\n)(.*?)(?=\n\[|$)'
    scripts_match = re.search(scripts_pattern, content, re.DOTALL)
    
    target_entry_point = 'mcp-feedback-pipe = "server:main"'
    
    if scripts_match:
        current_scripts = scripts_match.group(2).strip()
        print(f"📝 当前入口点配置: {current_scripts}")
        
        # 检查是否需要更新
        if target_entry_point not in current_scripts:
            print("🔧 更新入口点配置...")
            new_scripts = f"[project.scripts]\n{target_entry_point}\n"
            content = content[:scripts_match.start()] + new_scripts + content[scripts_match.end():]
            
            # 写回文件
            with open(pyproject_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print("✅ 入口点配置已更新")
        else:
            print("✅ 入口点配置已正确")
    else:
        print("❌ 未找到[project.scripts]配置")
        sys.exit(1)
    
    # 确保MANIFEST.in包含server.py
    manifest_path = Path("MANIFEST.in")
    if manifest_path.exists():
        with open(manifest_path, 'r', encoding='utf-8') as f:
            manifest_content = f.read()
        
        if "include server.py" not in manifest_content:
            print("🔧 更新MANIFEST.in...")
            # 在文件开头添加server.py
            lines = manifest_content.split('\n')
            # 找到第一个include语句的位置
            insert_pos = 0
            for i, line in enumerate(lines):
                if line.strip().startswith('include '):
                    insert_pos = i
                    break
            
            lines.insert(insert_pos, "include server.py                    # 主服务器脚本")
            
            with open(manifest_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(lines))
            print("✅ MANIFEST.in已更新")
        else:
            print("✅ MANIFEST.in配置已正确")
    else:
        print("⚠️  未找到MANIFEST.in文件")
    
    print("✅ 包结构准备完成")

def build_package():
    """构建Python包"""
    print("🏗️ 构建Python包...")
    
    # 清理旧的构建文件
    run_command("rm -rf dist/", check=False)
    
    # 构建包
    run_command("uv build")
    
    # 检查构建结果
    dist_files = list(Path("dist").glob("*"))
    if len(dist_files) == 0:
        print("❌ 构建失败，没有生成分发文件")
        sys.exit(1)
    
    print("✅ 构建完成:")
    for file in dist_files:
        print(f"   📦 {file.name}")
    
    return dist_files

def get_testpypi_token():
    """获取TestPyPI API token"""
    # 首先尝试从环境变量读取
    token = os.getenv('TESTPYPI_TOKEN')
    
    if token and token.startswith("pypi-"):
        print("🔑 使用环境变量中的TestPyPI token")
        return token
    
    print("\n🔑 TestPyPI认证配置")
    print("请访问 https://test.pypi.org/manage/account/token/ 创建TestPyPI API token")
    print("Token范围选择: 'Entire account' (首次发布) 或 'Scope to project' (后续)")
    print("💡 提示: 您可以将token保存到.env文件中的TESTPYPI_TOKEN变量")
    
    token = getpass.getpass("请输入TestPyPI API token (格式: pypi-...): ")
    
    if not token.startswith("pypi-"):
        print("❌ Token格式错误，应该以 'pypi-' 开头")
        return get_testpypi_token()
    
    return token

def get_pypi_token():
    """获取PyPI API token"""
    # 首先尝试从环境变量读取
    token = os.getenv('PYPI_TOKEN')
    
    if token and token.startswith("pypi-"):
        print("🔑 使用环境变量中的PyPI token")
        return token
    
    print("\n🔑 PyPI认证配置")
    print("请访问 https://pypi.org/manage/account/token/ 创建PyPI API token")
    print("Token范围选择: 'Entire account' (首次发布) 或 'Scope to project' (后续)")
    print("💡 提示: 您可以将token保存到.env文件中的PYPI_TOKEN变量")
    
    token = getpass.getpass("请输入PyPI API token (格式: pypi-...): ")
    
    if not token.startswith("pypi-"):
        print("❌ Token格式错误，应该以 'pypi-' 开头")
        return get_pypi_token()
    
    return token

def publish_to_testpypi(token):
    """发布到TestPyPI（测试环境）"""
    print("🧪 发布到TestPyPI（测试环境）...")
    
    cmd = f'uv publish --token {token} --publish-url https://test.pypi.org/legacy/'
    result = run_command(cmd, check=False, mask_sensitive=True)
    
    if result.returncode == 0:
        print("✅ TestPyPI发布成功!")
        print("🔗 查看: https://test.pypi.org/project/mcp-feedback-pipe/")
        print("🧪 测试安装: pip install -i https://test.pypi.org/simple/ mcp-feedback-pipe")
        return True
    else:
        print(f"❌ TestPyPI发布失败: {result.stderr}")
        if "403 Forbidden" in result.stderr:
            print("💡 可能的解决方案:")
            print("   1. 确认您使用的是TestPyPI的token (https://test.pypi.org/manage/account/token/)")
            print("   2. 确认token权限正确（建议使用'Entire account'权限）")
            print("   3. 确认包名在TestPyPI上没有被占用")
        return False

def publish_to_pypi(token):
    """发布到正式PyPI"""
    print("🚀 发布到正式PyPI...")
    
    # 检查是否自动确认
    auto_confirm = os.getenv('AUTO_CONFIRM_PYPI', 'false').lower() == 'true'
    
    if auto_confirm:
        print("⚡ 自动确认模式已启用（来自环境变量）")
        confirm = 'y'
    else:
        confirm = input("确认发布到正式PyPI？这将公开发布包 (y/N): ")
    
    if confirm.lower() != 'y':
        print("❌ 用户取消发布")
        return False
    
    cmd = f'uv publish --token {token}'
    result = run_command(cmd, check=False, mask_sensitive=True)
    
    if result.returncode == 0:
        print("🎉 正式PyPI发布成功!")
        print("🔗 查看: https://pypi.org/project/mcp-feedback-pipe/")
        return True
    else:
        print(f"❌ 正式PyPI发布失败: {result.stderr}")
        if "403 Forbidden" in result.stderr:
            print("💡 可能的解决方案:")
            print("   1. 确认您使用的是PyPI的token (https://pypi.org/manage/account/token/)")
            print("   2. 确认token权限正确（建议使用'Entire account'权限）")
            print("   3. 确认包名在PyPI上没有被占用")
        return False

def test_installation():
    """测试安装"""
    print("\n🧪 测试uvx安装...")
    
    # 清除可能的本地缓存
    run_command("uvx cache clean", check=False)
    
    # 测试从PyPI安装
    print("测试命令: uvx mcp-feedback-pipe")
    print("如果成功，应该启动MCP服务器")

def save_publish_config(project_info, success_testpypi, success_pypi):
    """保存发布配置"""
    config = {
        "project": project_info,
        "last_publish": {
            "testpypi": success_testpypi,
            "pypi": success_pypi,
            "timestamp": subprocess.check_output("date", shell=True, text=True).strip()
        }
    }
    
    config_path = Path(".publish_config.json")
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print(f"📝 发布配置已保存到 {config_path}")

def manage_version():
    """版本管理功能"""
    if not VERSION_MANAGER_AVAILABLE:
        print("⚠️  版本管理器不可用，跳过版本管理")
        return False
    
    print("\n📋 版本管理选项:")
    print("1. 使用当前版本")
    print("2. 自动递增版本号")
    print("3. 手动指定版本号")
    
    choice = input("请选择 (1-3): ").strip()
    
    if choice == "1":
        print("✅ 使用当前版本")
        return False
    
    # 初始化版本管理器
    vm = VersionManager(Path.cwd())
    
    if choice == "2":
        # 自动递增版本
        info = vm.get_version_info()
        print(f"\n📈 当前版本: {info['current_version']}")
        print("选择递增类型:")
        print(f"  1. Patch (补丁): {info['next_patch']}")
        print(f"  2. Minor (次要): {info['next_minor']}")
        print(f"  3. Major (主要): {info['next_major']}")
        
        inc_choice = input("请选择递增类型 (1-3): ").strip()
        if inc_choice == "1":
            new_version = info['next_patch']
        elif inc_choice == "2":
            new_version = info['next_minor']
        elif inc_choice == "3":
            new_version = info['next_major']
        else:
            print("❌ 无效选择")
            return False
            
    elif choice == "3":
        # 手动指定版本
        new_version = input("请输入新版本号 (格式: x.y.z): ").strip()
        try:
            vm.parse_version(new_version)
        except ValueError as e:
            print(f"❌ {e}")
            return False
    else:
        print("❌ 无效选择")
        return False
    
    # 确认并更新版本
    print(f"\n🔄 准备更新版本: {vm.current_version} → {new_version}")
    confirm = input("确认更新版本? (y/N): ").strip().lower()
    
    if confirm in ['y', 'yes']:
        if vm.update_all_versions(new_version):
            print(f"✅ 版本更新成功: {new_version}")
            return True
        else:
            print("❌ 版本更新失败")
            return False
    else:
        print("❌ 用户取消版本更新")
        return False

def main():
    """主函数"""
    print("🎯 MCP反馈通道 - PyPI发布工具")
    print("=" * 50)
    
    # 检查是否在项目根目录
    if not Path("pyproject.toml").exists():
        print("❌ 请在项目根目录运行此脚本")
        sys.exit(1)
    
    # 加载环境变量
    env_file = Path(".env")
    if env_file.exists():
        load_dotenv(env_file)
        print("✅ 已加载.env环境变量")
    else:
        print("⚠️  未找到.env文件，将使用交互式输入")
    
    try:
        # 0. 版本管理
        version_updated = manage_version()
        if version_updated:
            print("💡 版本已更新，继续发布流程...")
        
        # 1. 检查依赖
        check_dependencies()
        
        # 2. 获取项目信息
        project_info = get_project_info()
        print(f"📦 项目: {project_info['name']} v{project_info['version']}")
        
        # 3. 准备包结构
        prepare_package_structure()
        
        # 4. 构建包
        dist_files = build_package()
        
        # 5. 选择发布方式
        print("\n📤 发布选项:")
        print("1. 仅发布到TestPyPI（推荐首次发布）")
        print("2. 发布到TestPyPI + 正式PyPI")
        print("3. 仅发布到正式PyPI")
        
        choice = input("请选择 (1-3): ").strip()
        
        success_testpypi = False
        success_pypi = False
        
        # 6. 根据选择获取相应token并发布
        if choice in ['1', '2']:
            testpypi_token = get_testpypi_token()
            success_testpypi = publish_to_testpypi(testpypi_token)
            
        if choice in ['2', '3'] and (choice == '3' or success_testpypi):
            pypi_token = get_pypi_token()
            success_pypi = publish_to_pypi(pypi_token)
        
        # 7. 保存配置
        save_publish_config(project_info, success_testpypi, success_pypi)
        
        # 8. 测试指导
        if success_pypi:
            test_installation()
        
        print("\n🎊 发布流程完成!")
        if success_pypi:
            print("🌟 用户现在可以使用: uvx mcp-feedback-pipe")
        
    except KeyboardInterrupt:
        print("\n❌ 用户中断发布")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 发布过程中出错: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
