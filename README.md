# ROSA 系统 (Ronghua Wiki)

本仓库是 [ROSA 系统](https://MUYU46548.github.io/ronghua-wiki/) 的源代码与内容仓库。ROSA 系统是“绒花计划”的官方设定资料百科，致力于收集和整理关于绒花计划世界观的一切信息。

本网站基于 **Quartz 5.0** 构建，一个将 Markdown 笔记转换为静态网站的工具。

感谢原作者 jackyzha0 的杰出工作。

## 🚀 本地预览

如果你想在本地预览此 Wiki，请确保已安装 Node.js，然后执行以下命令：

```bash
# 1. 安装依赖
npm install

# 2. 构建并启动本地预览服务器
npx quartz build --serve
```

默认端口为8080，访问 `http://localhost:8080` 即可查看。

## 📂 仓库结构

- content/: 所有 Wiki 的 Markdown 源文件。
- quartz/: Quartz 的核心代码与配置文件。
- public/: npx quartz build 命令生成的静态网站文件（构建后可在本地预览）。
- quartz.config.yaml: Quartz 的主要配置文件，不建议修改。

## 致谢与许可说明

- 本项目基于 [Quartz](https://github.com/jackyzha0/quartz) 构建，Quartz 以 MIT 许可证发布，其版权归属见仓库 `LICENSE.txt`。
- 本仓库中 `content/` 目录下的原创内容（文本、图片等）采用 CC BY-NC-SA 4.0 许可。
- 有关 Quartz 本身的许可与使用限制，请以 Quartz 官方仓库为准。
