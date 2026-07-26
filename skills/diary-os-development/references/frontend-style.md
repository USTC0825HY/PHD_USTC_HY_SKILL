# Frontend Style Reference

## Information Architecture

Current left navigation labels:

- 今日指挥台
- 今日日记
- 周月年复盘
- 财务核对台
- Obsidian 联动
- 环境配置
- 数据与索引

The startup page is `今日指挥台`. It should answer "today, what should I do first?" rather than showing a generic analytics dashboard.

Homepage structure:

- Top hero/summary area inspired by Obsidian `00_日记中心`.
- Internal quick-entry cards for today diary, work plan, reviews, finance, sync, and environment config.
- Today status strip.
- Work backlog, recent diary, sync status, and other secondary operational panels.
- Work-time charts and heavier analytics lower on the page, not in the first viewport.

Do not add external Obsidian shortcut cards unless the user explicitly asks. The command center should use internal app destinations.

## Layout Rules

Current shell layout:

```css
body {
  min-width: 960px;
  height: 100%;
  overflow: hidden;
}

.app-shell {
  display: grid;
  grid-template-columns: 232px minmax(0, 1fr);
  height: 100vh;
  overflow: hidden;
}

.sidebar {
  display: flex;
  flex-direction: column;
  height: 100vh;
  overflow: hidden;
}

nav {
  min-height: 0;
  overflow: auto;
}

.sidebar-footer {
  margin-top: auto;
}

.main {
  height: 100vh;
  overflow: auto;
}
```

Preserve this split-scroll model:

- The left sidebar must remain visible when the main content scrolls.
- The refresh/status footer must stay inside the same fixed sidebar UI, not fall below scroll content.
- Main content scrolls independently.

## Color Tokens

The app uses a quiet green/cream local-workbench palette, not a marketing gradient style.

Core tokens:

```css
:root {
  --bg: #eef3ee;
  --surface: #fbfaf4;
  --surface-subtle: #f4f7f1;
  --surface-muted: #e8eee7;
  --border: #d5ded4;
  --border-strong: #bdcabf;
  --text: #24312b;
  --muted: #66736a;
  --muted-2: #8a968e;
  --nav: #34443f;
  --nav-muted: #c7d0c9;
  --nav-active: #dce8df;
  --nav-active-text: #24352f;
  --primary: #6f927d;
  --primary-strong: #5b7d6b;
  --primary-soft: #e3ede5;
  --primary-tint: #f1f6ef;
  --primary-border: #c8d8cc;
  --on-primary: #f7faf5;
  --warning: #92743e;
  --warning-soft: #f0ead8;
  --warning-border: #d8cab0;
  --warning-tint: #f7f2e6;
  --danger: #a26058;
  --danger-soft: #eee1dc;
  --danger-border: #d8c4be;
  --danger-tint: #f5eeea;
  --morning: #5f927d;
  --afternoon: #aa925a;
  --evening: #707fa0;
  --other: #87918a;
  --input-bg: #fdfbf5;
  --hover: #f6f8f3;
  --table-head: #edf3ec;
  --topbar-bg: rgba(251, 250, 244, 0.92);
  --tooltip-bg: rgba(251, 250, 244, 0.98);
  --shadow: rgba(52, 68, 63, 0.11);
}
```

When adding UI, reuse tokens instead of introducing unrelated palettes. Keep contrast readable and avoid one-note saturated themes.

## Typography

Current global type:

```css
font-family: "Segoe UI", "Microsoft YaHei", system-ui, sans-serif;
```

Guidelines:

- Keep body text compact and operational.
- Use 24px topbar headings and 16px panel headings unless a true hero requires more.
- Do not scale type directly with viewport width.
- Keep letter spacing at normal `0`.
- Use Chinese labels consistently with the current product language.

## Components

Cards and panels:

- Use `border-radius: 8px` or less.
- Use `border: 1px solid var(--border)`.
- Use `background: var(--surface)`.
- Do not nest cards inside cards.
- Use panels for functional sections, repeated cards for item groups, and modals only for focused overlays.

Buttons:

- Primary: `var(--primary-strong)` background and `var(--on-primary)` text.
- Secondary: `var(--surface-muted)` background.
- Danger/ghost: danger tokens.
- Icon-only buttons should be square, usually 36px.
- Prefer lucide icons already used in `App.tsx`.

Controls:

- Use segmented controls for mode choice.
- Use checkboxes for binary state.
- Use inputs/selects/textareas for structured fields.
- Use tables for dense index or ledger views.
- Use toolbars with compact grouped actions for repeated workflows.

## Dashboard Cards

Command-center cards should contain:

- A small icon block.
- Short title.
- Operational metadata.
- A direct internal action.

Keep text direct and task-focused. Avoid in-app explanatory prose that describes features or teaches the UI.

## Responsive Boundary

The app currently assumes desktop use with `min-width: 960px`. Do not add mobile-first layout changes unless the user asks for mobile/web work. Future online/mobile clients should be planned as separate surfaces, not squeezed into the current Windows desktop shell.

## Interaction State

After local saves that affect sync, update visible sync state without forcing a page switch.

Relevant frontend functions:

- `persistWorkTasks`
- daily save handlers around `createOrUpdateDailyEntry`
- review save handlers around `createOrUpdateReviewEntry`
- sync preview loader around `previewObsidianSync`

Keep status text concise:

- Say when work plan save completed.
- Say when sync preview shows pending items.
- Say when environment is ready or needs action.
