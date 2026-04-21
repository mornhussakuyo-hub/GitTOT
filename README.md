# GitTOT

按提交时间统计 Git 仓库的代码增加 / 删除情况，并输出终端图表、JSON 或 CSV。

支持：

* 本地 Git 仓库统计
* 远程 GitHub 仓库统计
* 按时间范围、作者、分支过滤
* 按小时、星期、日期、月份聚合
* 输出终端图表、JSON、CSV

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

## 快速开始

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

## 常用参数

### 过滤参数

* `--since` 只统计某个时间之后的提交
* `--until` 只统计某个时间之前的提交
* `--author` 只统计指定作者
* `--branch` 只统计指定分支可达的提交

### 聚合参数

* `--by hour` 按小时聚合
* `--by weekday` 按星期聚合
* `--by date` 按日期聚合
* `--by month` 按月份聚合

### 输出参数

* `--format chart` 输出终端图表
* `--format json` 输出 JSON
* `--format csv` 输出 CSV

---

## 时间格式

`--since` 和 `--until` 支持 ISO 风格时间：

```text
2026-04-01
2026-04-01T09:30:00
2026-04-01T09:30:00+08:00
2026-04-01T01:30:00Z
```

说明：

* 如果只传日期，例如 `2026-04-01`，`--since` 会按当天 `00:00:00` 处理
* 如果只传日期，例如 `2026-04-30`，`--until` 会按当天 `23:59:59` 处理
* 如果不带时区，默认按你当前机器的本地时区解释

---

## 使用示例

### 统计 2026 年 4 月之后的本地提交

```bash
gittot --since 2026-04-01
```

### 统计指定作者在 main 分支上的本地提交

```bash
gittot --author "alice@example.com" --branch main
```

### 按星期查看当前仓库的改动分布

```bash
gittot --by weekday
```

### 按日期输出 JSON

```bash
gittot --by date --format json
```

### 按月份输出 CSV

```bash
gittot --by month --format csv
```

### 统计远程 GitHub 仓库某个作者在指定时间范围内的提交

```bash
gittot \
  --repo https://github.com/OWNER/REPO \
  --token YOUR_GITHUB_TOKEN \
  --author octocat \
  --since 2026-01-01 \
  --until 2026-03-31 \
  --by month
```

### 将远程统计结果保存为 CSV

```bash
gittot \
  --repo https://github.com/OWNER/REPO \
  --token YOUR_GITHUB_TOKEN \
  --by date \
  --format csv > report.csv
```

---

## 输出说明

### `chart`

默认输出格式。左侧为删除行数，右侧为新增行数，同时显示每个时间桶内的提交数。

### `json`

输出结构如下：

```json
{
  "group_by": "weekday",
  "totals": {
    "add": 120,
    "del": 45,
    "commits": 8
  },
  "rows": [
    {
      "bucket": "Mon",
      "add": 30,
      "del": 10,
      "commits": 2
    }
  ]
}
```

### `csv`

输出列如下：

```text
bucket,add,del,commits
Mon,30,10,2
Tue,0,0,0
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
* 传入的 `--branch`、`--author`、时间范围是否正确

---

## License

MIT
