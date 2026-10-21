# Distribution

Reviewed against official documentation on 2026-10-21. Requirements can change; check the linked guides before submitting.

## Available from this repository

| Route | Package | Installation |
| --- | --- | --- |
| Agent Skills | `skills/build-novel/` | `npx skills add radianx/build-novel --skill build-novel` |
| Codex marketplace | `.agents/plugins/marketplace.json` and `.codex-plugin/plugin.json` | Add `radianx/build-novel`, then install `build-novel@build-novel` |
| Claude Code marketplace | `.claude-plugin/marketplace.json` and `.claude-plugin/plugin.json` | Add `radianx/build-novel`, then install `build-novel@build-novel` |
| Skill uploads | `build-novel-skill.zip` | Upload where the product supports custom skills |
| Plugin uploads | `build-novel-plugin.zip` | Import or submit where the product supports this package format |

These routes share one skill directory. No marketplace membership, paid API key, or connection to a publisher-operated service is required to download it. Running an agent may require its own account or subscription.

## OpenAI directory

The [submission guide](https://developers.openai.com/plugins/deploy/submission) describes ZIP upload, scans, review, and publication. The publishing account needs the appropriate organization permission and verified developer identity. Complete the listing fields and test the imported skill before requesting review. This repository's manifests support local distribution; they do not establish directory eligibility or approval.

Workspace administrators can also [import GitHub marketplaces](https://help.openai.com/en/articles/20001504-importing-and-syncing-plugin-marketplaces-from-github). Workspace distribution does not create a public directory listing.

## Anthropic directory

The current [publishing guide](https://code.claude.com/docs/en/plugins/publish#submit-to-anthropics-directory) directs submissions to [claude.ai/directory/manage](https://claude.ai/directory/manage), using an eligible paid account and the required role. Validate locally, then complete the portal's additional checks and review. The directory route is separate from the `claude-plugins-official` marketplace, whose listing route involves an Anthropic partner contact.

Our own GitHub marketplace is installable independently of those reviews. A passing local validation does not mean directory approval.

## Other agents

The skill follows the [Agent Skills specification](https://agentskills.io/specification). The [Skills CLI](https://github.com/vercel-labs/skills) can install it into supported hosts. Compatibility with an untested agent is not guaranteed; file access, shell execution, context limits, and invocation syntax vary.

## Release checks

1. Keep the two plugin manifest versions equal and update them for a release.
2. Run the utility self-check and distribution check described in the README.
3. Validate the Claude manifest and test marketplace installation locally.
4. Build archives from the clean public tree and inspect their file lists.
5. Publish the tested tree and archives; verify public access and installation discovery.

Publish only reusable skill files. Do not add manuscripts, author interviews, personal canon, local credentials, or generated Python caches.
