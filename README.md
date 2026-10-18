# International Macro Biweekly

用于检索指定国家在明确日期区间内的重要宏观经济、财政、货币政策、政治风险、外贸能源及主权评级新闻，并按照内置 Word 模板生成中文国际宏观资讯双周报和来源链接清单。

## 安装到另一台电脑

本仓库为公开仓库。在另一台电脑的 Codex 中提出：

```text
请使用 skill-installer，从 GitHub 仓库 gongruyin0730/cangcang 的根目录安装这个 Skill，名称设为 international-macro-biweekly。
```

也可以在本机执行 Codex 内置安装脚本：

```bash
python ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo gongruyin0730/cangcang \
  --path . \
  --name international-macro-biweekly
```

安装后，新建一个 Codex 任务即可使用：

```text
使用 $international-macro-biweekly，整理指定国家和日期区间的重要宏观资讯并生成双周报。
```

## 内容

- `SKILL.md`：触发条件和研究、写作、交付流程
- `references/`：筛选标准、信源优先级和国家检索范围
- `scripts/validate_research.py`：研究记录校验脚本
- `assets/国际宏观资讯双周报模板.docx`：Word 模板
- `agents/openai.yaml`：Codex 界面元数据和自动触发策略

## 更新

在一台电脑修改并推送后，其他电脑可删除旧安装目录后重新安装，或在确认无本地改动的情况下从仓库同步最新版。
