# Agent Instructions

## Skill 存放规则

- 本仓库中的新增 skill，统一存放在：`/Users/flowkehurly/Documents/AAA/skills/skills/`
- 不要把新的 skill 直接创建在仓库根目录：`/Users/flowkehurly/Documents/AAA/skills/`
- 每个 skill 必须使用独立目录，目录名与 skill 名保持一致
- 在修改已有 skill 时，优先修改其 source 目录下的真实文件，不要直接把内容写进 `~/.codex/skills` 中的链接目标路径

## Skill 启用规则

- 当需要让 Codex 使用本仓库中的 skill 时，优先通过 `codex-skill-linker` 建立软链接到 `~/.codex/skills`
- 不要通过复制目录的方式把 skill 同步到 `~/.codex/skills`，除非用户明确要求复制而不是 link

## 默认约定

- 若用户要求“创建一个新 skill 到 AAA skills 仓库”，默认目标目录应为：`/Users/flowkehurly/Documents/AAA/skills/skills/<skill-name>`
- 若用户未特别说明，创建完成后可使用 `codex-skill-linker` 将该 skill link 到 `~/.codex/skills`
