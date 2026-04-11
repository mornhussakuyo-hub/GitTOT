# GitTOT

按小时统计 Git 代码增删，并在终端输出图表。

## 依赖

- Python 3.10+
- Git

## 安装

```bash
pip install -e .
```

## 用法

统计当前本地仓库：

```bash
gittot
```

在 Git 仓库目录里运行。

统计远程 GitHub 仓库：

```bash
gittot --repo https://github.com/OWNER/REPO --token YOUR_GITHUB_TOKEN
```

限制远程提交数：

```bash
gittot --repo https://github.com/OWNER/REPO --token YOUR_GITHUB_TOKEN --max-commits 500
```

## 输出

- `00:00` 到 `23:00`
- 左侧是删除
- 右侧是增加

