#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Quartz 自动构建与发布工具
用法: python update_site.py [--serve] [--push] [--port PORT] [--path PATH] [--help]

双分支策略：
  - v5 分支：源码与设定备份
  - deploy 分支：仅 public/ 构建产物（GitHub Pages 发布）

推送逻辑（方案 A）：
  使用 git worktree 将 public/ 内容全量覆盖到 deploy 分支后提交。
  worktree 路径：项目根目录同级的 .quartz-deploy 目录。
"""

import subprocess
import sys
import os
import argparse
import shutil
import datetime
from pathlib import Path

# ===== 默认配置 =====
DEFAULT_PROJECT_ROOT = r"E:\图书馆\quartz"
DEFAULT_PORT = 8080
DEFAULT_BRANCH = "v5"          # 源码分支
DEPLOY_BRANCH = "deploy"       # 发布分支


def find_quartz_root():
    """自动检测 Quartz 项目根目录"""
    env_root = os.environ.get("QUARTZ_ROOT")
    if env_root and os.path.exists(os.path.join(env_root, "quartz.config.yaml")):
        return env_root
    if os.path.exists("quartz.config.yaml"):
        return os.getcwd()
    return DEFAULT_PROJECT_ROOT


def run_command(cmd, cwd=None):
    """执行命令，实时打印输出，返回 (返回码, 输出文本)"""
    print(f"\n>>> {cmd}")
    if cwd:
        print(f"    cwd: {cwd}")
    process = subprocess.Popen(
        cmd, shell=True, cwd=cwd,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        text=True, bufsize=1, encoding='utf-8', errors='replace'
    )
    output_lines = []
    for line in process.stdout:
        print(line, end='')
        output_lines.append(line)
    process.wait()
    return process.returncode, ''.join(output_lines)


def check_dependencies():
    """检查 node, npx 是否可用"""
    missing = []
    for name, cmd in [("node", "node --version"), ("npx", "npx --version")]:
        try:
            subprocess.run(cmd, shell=True, check=True, capture_output=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            missing.append(name)
    if missing:
        print(f"❌ 缺少依赖: {', '.join(missing)}")
        return False
    return True


def build_quartz(project_root):
    """执行 npx quartz build"""
    print("\n🚀 构建 Quartz ...")
    return run_command("npx quartz build", cwd=project_root)


def copy_tree_force(src, dst):
    """递归复制，覆盖目标"""
    if not os.path.exists(dst):
        os.makedirs(dst)
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            if os.path.exists(d):
                shutil.rmtree(d)
            shutil.copytree(s, d)
        else:
            shutil.copy2(s, d)


def clear_directory_keep_git(directory):
    """清空目录内容，保留 .git"""
    for item in os.listdir(directory):
        if item == ".git":
            continue
        item_path = os.path.join(directory, item)
        if os.path.isdir(item_path):
            shutil.rmtree(item_path)
        else:
            os.unlink(item_path)


def git_push_deploy(project_root):
    """
    方案 A：使用 worktree 将 public/ 全量覆盖到 deploy 分支后提交推送。
    """
    print(f"\n📤 推送构建产物到 {DEPLOY_BRANCH} 分支（方案 A：worktree）...")

    # worktree 路径：与项目根目录同级
    parent_dir = os.path.dirname(project_root.rstrip("/\\"))
    worktree_dir = os.path.join(parent_dir, ".quartz-deploy")

    # 检查 worktree 是否已存在
    worktree_git = os.path.join(worktree_dir, ".git")
    worktree_exists = os.path.exists(worktree_git)

    if not worktree_exists:
        # 创建 worktree
        print(f"   创建 worktree: {worktree_dir}")
        ret, output = run_command(
            f"git worktree add {worktree_dir} {DEPLOY_BRANCH}",
            cwd=project_root
        )
        if ret != 0:
            print("   ❌ 创建 worktree 失败")
            return False
    else:
        # 已有 worktree，确保在正确分支并同步远程
        print(f"   使用已有 worktree: {worktree_dir}")
        run_command(f"git checkout -f {DEPLOY_BRANCH}", cwd=worktree_dir)
        run_command(f"git fetch origin {DEPLOY_BRANCH}", cwd=worktree_dir)
        run_command(f"git reset --hard origin/{DEPLOY_BRANCH}", cwd=worktree_dir)

    # 清空 worktree（保留 .git）
    print("   清空旧文件...")
    clear_directory_keep_git(worktree_dir)

    # 复制 public/ 到 worktree
    public_dir = os.path.join(project_root, "public")
    if not os.path.exists(public_dir):
        print(f"   ❌ public 目录不存在: {public_dir}")
        return False

    print("   复制构建产物...")
    copy_tree_force(public_dir, worktree_dir)

    # 提交
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("   提交中...")
    run_command("git add -A", cwd=worktree_dir)

    ret, output = run_command(
        f'git commit -m "deploy: {timestamp}"',
        cwd=worktree_dir
    )
    if ret != 0:
        if "nothing to commit" in output or "no changes" in output:
            print("   ℹ️ 无变更，跳过提交")
            return True
        print("   ❌ 提交失败")
        return False

    # 推送
    ret, output = run_command(f"git push origin {DEPLOY_BRANCH}", cwd=worktree_dir)
    if ret != 0:
        print("   ❌ 推送失败")
        return False

    print("   ✅ 推送完成")
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Quartz 自动构建与发布工具（双分支策略）",
        epilog="示例: python update_site.py --serve --push"
    )
    parser.add_argument("--serve", "-s", action="store_true",
                        help="构建后启动预览服务器")
    parser.add_argument("--push", "-p", action="store_true",
                        help="构建后推送到 deploy 分支")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT,
                        help=f"预览端口（默认 {DEFAULT_PORT}）")
    parser.add_argument("--path", type=str,
                        help="Quartz 项目根目录（默认自动检测）")
    args = parser.parse_args()

    # 确定项目根目录
    project_root = args.path if args.path else find_quartz_root()
    config_file = os.path.join(project_root, "quartz.config.yaml")
    if not os.path.exists(config_file):
        print(f"❌ 找不到 quartz.config.yaml: {project_root}")
        sys.exit(1)

    print(f"📁 项目根目录: {project_root}")

    # 检查依赖
    if not check_dependencies():
        sys.exit(1)

    # 构建
    ret, _ = build_quartz(project_root)
    if ret != 0:
        print("\n❌ 构建失败")
        sys.exit(1)
    print("\n✅ 构建成功！")

    # 推送（可选）
    if args.push:
        git_push_deploy(project_root)

    # 预览（可选）
    if args.serve:
        public_dir = os.path.join(project_root, "public")
        # 使用 Quartz 自带的开发服务器（支持 SPA 路由）
        print("\n🌐 启动预览服务器...")
        cmd = f"npx quartz build --serve --port {args.port}"
        ret, output = run_command(cmd, cwd=project_root)
        if ret != 0:
            print("❌ 启动预览服务器失败")
            sys.exit(1)
    else:
        print("\n🎉 完成！")
        print("   预览: python update_site.py --serve")
        print("   发布: python update_site.py --push")


if __name__ == "__main__":
    main()
