# GitTOT

按小时统计 Git 仓库的代码增加 / 删除情况，并在终端输出可视化图表。

支持：

* 本地 Git 仓库统计
* 远程 GitHub 仓库统计

---

## 环境要求

* Python 3.10+
* Git

---

## 安装

### 方式一：开发安装

```bash
git clone https://github.com/mornhussakuyo-hub/GitTOT.git
cd GitTOT
pip install -e .
```

### 方式二：虚拟环境安装

```bash
git clone https://github.com/mornhussakuyo-hub/GitTOT.git
cd GitTOT
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

### Arch Linux 依赖

```bash
sudo pacman -S python python-pip git
```

### Ubuntu / Debian 依赖

```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv git
```

---

## 用法

### 统计当前本地仓库

进入任意 Git 仓库目录后运行：

```bash
gittot
```

### 统计远程 GitHub 仓库

```bash
gittot --repo https://github.com/OWNER/REPO --token YOUR_GITHUB_TOKEN
```

### 限制远程拉取的提交数

```bash
gittot --repo https://github.com/OWNER/REPO --token YOUR_GITHUB_TOKEN --max-commits 500
```

---

## 绑定 GitHub Token

首次绑定：

```bash
gittot --bind YOUR_GITHUB_TOKEN
```

绑定后可直接使用：

```bash
gittot --repo https://github.com/OWNER/REPO
```

查看是否已绑定：

```bash
gittot --show-bind
```

取消绑定：

```bash
gittot --unbind
```

临时覆盖已绑定的 token：

```bash
gittot --repo https://github.com/OWNER/REPO --token ANOTHER_TOKEN
```

Token 优先级：

```text
--token > 本地绑定 token > 环境变量 GITHUB_TOKEN
```

---

## 配置文件

本地绑定的 token 默认保存到：

```text
~/.config/gittot/config.json
```

---

## 常见问题

### `gittot: command not found`

重新安装：

```bash
pip install -e .
```

如果你使用虚拟环境，先激活环境：

```bash
source .venv/bin/activate
```

### 本地仓库统计失败

请确认当前目录是 Git 仓库：

```bash
git status
```

### 远程仓库统计失败

请检查：

* 仓库地址是否正确
* GitHub Token 是否有效
* 是否有访问该仓库的权限

---

## License

MIT
