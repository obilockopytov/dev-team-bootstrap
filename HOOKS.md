# AI Wiki Hooks Setup

Автоматическое обновление wiki при работе с AI-ассистентами через IDE-хуки.

## Что делает

Хуки автоматически:
- Логируют использованные инструменты в `~/wiki/sessions/YYYY-MM-DD.md`
- Создают напоминание `~/wiki/UPDATE_REMINDER.md` при завершении сессии
- Синхронизируют активность между Cursor, Claude Code и Codex

## Установка

### 1. Скрипт обновления wiki

Создай `~/bin/ai-update-wiki.sh`:

```bash
#!/bin/bash
# AI Wiki Update Hook Script

INPUT=$(cat)

# Extract event type and tool info (handle different formats)
EVENT_TYPE=$(echo "$INPUT" | jq -r '.eventType // .type // "unknown"')
TOOL_NAME=$(echo "$INPUT" | jq -r '.toolName // .tool // .tool_call // empty')
TOOL_TYPE=$(echo "$INPUT" | jq -r '.toolType // .name // empty')
SESSION_ID=$(echo "$INPUT" | jq -r '.sessionId // .session // empty')
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

if [[ -z "$TOOL_NAME" && -n "$TOOL_TYPE" ]]; then
    TOOL_NAME="$TOOL_TYPE"
fi

WIKI_DIR="$HOME/wiki/sessions"
mkdir -p "$WIKI_DIR"

DATE_STR=$(date +"%Y-%m-%d")
SESSION_FILE="$WIKI_DIR/${DATE_STR}.md"

if [[ ! -f "$SESSION_FILE" ]]; then
    cat > "$SESSION_FILE" << EOF
# Session Log - $DATE_STR

Started: $(date +"%Y-%m-%d %H:%M:%S")

## Tools Used

EOF
fi

if [[ -n "$TOOL_NAME" && "$TOOL_NAME" != "null" ]]; then
    echo "- [$TIMESTAMP] \`$TOOL_NAME\`" >> "$SESSION_FILE"
fi

if [[ "$EVENT_TYPE" == "stop" || "$EVENT_TYPE" == "sessionEnd" || "$EVENT_TYPE" == "end" ]]; then
    REMINDER_FILE="$HOME/wiki/UPDATE_REMINDER.md"
    cat > "$REMINDER_FILE" << 'EOF'
# Wiki Update Reminder

> This file is automatically updated when a conversation ends.
> **Action required:** Review and update relevant wiki pages.

## Post-Session Checklist

- [ ] Review session logs in `sessions/`
- [ ] Update project documentation if new patterns were introduced
- [ ] Document architectural decisions in `_shared/`
- [ ] Update relevant `README.md` files
- [ ] Sync any reusable solutions to skills

## Quick Links

- [Today's Session](./sessions/EOF
    echo "$(date +%Y-%m-%d).md)" >> "$REMINDER_FILE"
    cat >> "$REMINDER_FILE" << 'EOF'
- [All Sessions](./sessions/)
- [Shared Notes](../_shared/)
EOF
fi

echo '{}'
```

Сделай исполняемым:
```bash
chmod +x ~/bin/ai-update-wiki.sh
```

### 2. Cursor hooks (`~/.cursor/hooks.json`)

```json
{
  "version": 1,
  "hooks": {
    "postToolUse": [
      {
        "command": "/Users/jammy/bin/ai-update-wiki.sh >> /tmp/ai-wiki-hook.log 2>&1",
        "timeout": 5
      }
    ],
    "sessionEnd": [
      {
        "command": "/Users/jammy/bin/ai-update-wiki.sh >> /tmp/ai-wiki-hook.log 2>&1",
        "timeout": 10
      }
    ],
    "stop": [
      {
        "command": "/Users/jammy/bin/ai-update-wiki.sh >> /tmp/ai-wiki-hook.log 2>&1",
        "timeout": 10
      }
    ]
  }
}
```

### 3. Claude Code hooks (`~/.claude/hooks.json`)

```json
{
  "version": 1,
  "hooks": {
    "postToolUse": [
      {
        "command": "/Users/jammy/bin/ai-update-wiki.sh >> /tmp/ai-wiki-hook.log 2>&1",
        "timeout": 5
      }
    ],
    "sessionEnd": [
      {
        "command": "/Users/jammy/bin/ai-update-wiki.sh >> /tmp/ai-wiki-hook.log 2>&1",
        "timeout": 10
      }
    ],
    "stop": [
      {
        "command": "/Users/jammy/bin/ai-update-wiki.sh >> /tmp/ai-wiki-hook.log 2>&1",
        "timeout": 10
      }
    ]
  }
}
```

### 4. Codex hooks (`~/.codex/hooks.json`)

```json
{
  "version": 1,
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Glob|Grep",
        "hooks": [
          {
            "type": "command",
            "command": "[ -f graphify-out/graph.json ] && echo '{\"hookSpecificOutput\":{\"hookEventName\":\"PreToolUse\",\"additionalContext\":\"graphify: Knowledge graph exists. Read graphify-out/GRAPH_REPORT.md for god nodes and community structure before searching raw files.\"}}' || true"
          }
        ]
      }
    ],
    "postToolUse": [
      {
        "type": "command",
        "command": "/Users/jammy/bin/ai-update-wiki.sh >> /tmp/ai-wiki-hook.log 2>&1",
        "timeout": 5
      }
    ],
    "sessionEnd": [
      {
        "type": "command",
        "command": "/Users/jammy/bin/ai-update-wiki.sh >> /tmp/ai-wiki-hook.log 2>&1",
        "timeout": 10
      }
    ],
    "stop": [
      {
        "type": "command",
        "command": "/Users/jammy/bin/ai-update-wiki.sh >> /tmp/ai-wiki-hook.log 2>&1",
        "timeout": 10
      }
    ]
  }
}
```

## Структура wiki

```
~/wiki/
├── README.md           # Документация wiki
├── UPDATE_REMINDER.md  # Создаётся автоматически при завершении сессии
└── sessions/
    └── 2026-04-23.md   # Лог сессий по датам
```

## Требования

- `jq` для обработки JSON
- `bash` и стандартные Unix утилиты

Установка jq:
```bash
# macOS
brew install jq

# Ubuntu/Debian
sudo apt-get install jq
```

## Отладка

Логи хуков пишутся в `/tmp/ai-wiki-hook.log`:
```bash
tail -f /tmp/ai-wiki-hook.log
```

## Кастомизация

- Измени `$WIKI_DIR` в скрипте для другого расположения
- Добавь свои события в `hooks.json`
- Модифицируй формат логов в `ai-update-wiki.sh`
