# Build Novel

An open Agent Skill for developing, drafting, revising, and preparing novels or series for publication. Works in the author's language and keeps the author in control of canon, voice, major choices, and endings.

It includes author interviews, worldbuilding, chapter and scene outlines, continuity checks, simulated reader panels, translation guidance, project templates, and optional publication utilities. Fantasy can stay lyrical, ritualistic, ambiguous, or mysterious: style checks preserve deliberate literary choices, and magic does not need a technical explanation.

## Install

Choose **one** installation method to avoid loading duplicate copies.

### Agent Skills: Codex, Claude Code, Cursor, and other supported agents

Run in your writing project:

```sh
npx skills add radianx/build-novel --skill build-novel
```

The installer asks which agents to use. Add `--global` for use across projects, or select one explicitly:

```sh
npx skills add radianx/build-novel --skill build-novel --agent codex --global
npx skills add radianx/build-novel --skill build-novel --agent claude-code --global
```

The current [Skills CLI](https://github.com/vercel-labs/skills) requires Node.js 22.20 or later. Its [agent compatibility list](https://github.com/vercel-labs/skills/blob/main/docs/agents.md) covers supported agents and installation paths. The skill itself is Markdown and does not require Node.js.

### Codex plugin marketplace

With a Codex CLI that supports `codex plugin`:

```sh
codex plugin marketplace add radianx/build-novel
codex plugin add build-novel@build-novel
```

Start a new session after installation. The repository includes native Codex plugin and marketplace manifests; workspace administrators can also import this GitHub marketplace where that feature is available. See [OpenAI's packaging guide](https://developers.openai.com/plugins/build/plugins).

### Claude Code plugin marketplace

```sh
claude plugin marketplace add radianx/build-novel
claude plugin install build-novel@build-novel
```

Start a new session and invoke `/build-novel:build-novel`. Inside Claude Code, the equivalent commands start with `/plugin` instead of `claude plugin`. See [Anthropic's marketplace guide](https://code.claude.com/docs/en/plugin-marketplaces).

### Manual installation and ZIP uploads

Copy the entire [`skills/build-novel`](skills/build-novel) directory, including its references, scripts, and templates, into your agent's skill directory. For example:

```sh
git clone https://github.com/radianx/build-novel.git
mkdir -p ~/.agents/skills
cp -R build-novel/skills/build-novel ~/.agents/skills/build-novel
```

Use an empty destination, or back up an existing installation before replacing it. Codex supports `~/.agents/skills`; Claude Code uses `~/.claude/skills`. Other agents may use a different directory.

After the first successful CI run, [release downloads](https://github.com/radianx/build-novel/releases/latest) provide `build-novel-skill.zip` for products that accept uploaded skills and `build-novel-plugin.zip` for plugin distribution. Product plans and workspace settings can restrict uploads. Agents without native skill support can read `skills/build-novel/SKILL.md` and follow its linked references, but automatic discovery and script execution depend on the host.

## Use

For a standalone installation in Codex:

```text
Use $build-novel to help me develop a fantasy novel.
Ask one consequential question at a time. Keep the magic mysterious.
```

In Claude Code, use `/build-novel` for a standalone skill or `/build-novel:build-novel` for the plugin. You can also ask the agent to use Build Novel in ordinary language.

Existing manuscripts are welcome. Specify the work you want, such as a continuity review, a blind simulated reader panel, or a revision of selected scenes. Reviews preserve the manuscript unless edits are authorized. Simulated readers are diagnostic aids, not human readers or quality guarantees.

### En español

La skill trabaja en el idioma del autor. Conserva la voz, el canon y la libertad literaria: lirismo, repeticiones rituales, narradores no fiables y magia inexplicable pueden ser decisiones válidas.

```text
Usá build-novel para desarrollar mi novela de fantasía.
Haceme una pregunta relevante por turno. No conviertas la magia en un sistema técnico.
```

## Optional utilities

The writing workflow only needs an agent that can read Markdown. The bundled scripts require Python 3.10 or later:

```sh
python3 skills/build-novel/scripts/init_project.py ./my-novel --title "Working title"
python3 skills/build-novel/scripts/manuscript_stats.py ./my-novel/manuscript
```

Cover generation requires Pillow. Publication checks use Pillow for images and Poppler (`pdfinfo`, `pdftotext`) for PDFs; EPUBCheck is optional but recommended for EPUB validation. Missing external validators are reported as skipped checks. Other output formats may require tools supplied by your agent or environment; this skill does not bundle a complete publishing application.

## Distribution and updates

This repository supplies a public, publisher-managed marketplace for Codex and Claude Code, plus a portable Agent Skills package. **It is not an approved listing in OpenAI's or Anthropic's official directories.** See [distribution notes](DISTRIBUTION.md) for the separate submission routes and requirements.

For Skills CLI installations, run `npx skills check` and `npx skills update`. For Claude Code plugins, run `claude plugin update build-novel@build-novel`. For Codex plugins, refresh with `codex plugin marketplace upgrade build-novel`, then reinstall with `codex plugin add build-novel@build-novel`. Start a new session after updates.

## Development

```sh
python3 -m pip install Pillow
python3 -B skills/build-novel/scripts/self_check.py
python3 scripts/check_distribution.py
claude plugin validate --strict .
mkdir -p dist
python3 -m zipfile -c dist/build-novel-skill.zip skills/build-novel
python3 -m zipfile -c dist/build-novel-plugin.zip .claude-plugin .codex-plugin .agents skills assets LICENSE README.md DISTRIBUTION.md
```

Run packaging from a clean checkout so generated caches cannot enter archives. Increment both plugin manifest versions when releasing changes. CI checks the utilities and distribution layout; successful pushes to `main` publish the tested ZIPs when that version has no release yet. Existing releases are preserved.

## Privacy and license

The package contains reusable instructions, blank templates, and local utilities. It has no bundled service, account requirement, telemetry, MCP server, or lifecycle hooks. Your chosen agent and model provider still govern how manuscript data is handled. Keep private manuscripts in a separate project.

MIT licensed. The license covers this skill package and does not claim ownership of your writing. [Humanizer](https://github.com/blader/humanizer) is referenced as an editorial resource; it is not installed or run as a dependency. Literary decisions remain governed by the author's goals.
