---
name: setup
description: Configure the Pixel Pings notification sounds for Claude Code. Use this whenever someone wants to preview or replay the 8-bit sounds, make them louder or quieter, mute them, stop terminal or iTerm2 notification banners, or fix sounds that play twice, even if they never say "Pixel Pings". Також використовуй цей скіл для запитів українською, таких як програти звуки, зробити гучніше чи тихіше, вимкнути звук, прибрати сповіщення iTerm2 або звук грає двічі.
---

# Pixel Pings setup

The plugin's hooks already play the sounds, so this skill only handles preferences. Do the part the person asked for and leave the rest alone.

Preferences live in `~/.claude/settings.json`. Read the file before changing it and merge your change into what is there. A file with broken JSON silently turns off every setting in it, so run `python3 -m json.tool ~/.claude/settings.json >/dev/null` after each edit.

## Preview the sounds

Name each sound before playing it, so the person knows which is which:

| Sound | Plays when |
|---|---|
| `done` | Claude finishes a turn, waiting for any background subagents to finish first |
| `attention` | Claude needs a permission or an answer |
| `limit` | a turn stops on a rate limit |

```sh
sh "${CLAUDE_PLUGIN_ROOT}/scripts/play.sh" done
sh "${CLAUDE_PLUGIN_ROOT}/scripts/play.sh" attention
sh "${CLAUDE_PLUGIN_ROOT}/scripts/play.sh" limit
```

## Change the volume

Set `PIXEL_PINGS_VOLUME` in the `env` block of the settings file. It multiplies the sound's amplitude: `1` is the default, `1.5` is 50% louder, and `0` mutes.

Requests like "louder" are relative, so start from the current value. If they give no amount, multiply by 1.5 for louder or 0.7 for quieter. Above about 3 the sounds start to clip, so stop there and suggest raising the system volume instead.

Play `done` at the new level so they can judge it, for example `PIXEL_PINGS_VOLUME=1.5 sh "${CLAUDE_PLUGIN_ROOT}/scripts/play.sh" done`. Sessions that are already running keep the old value until they restart, so tell them that.

## Stop terminal banners

Claude Code's own terminal notifications, such as iTerm2 banners and the terminal bell, are separate from these sounds. Set this top-level key to stop them:

```json
"preferredNotifChannel": "notifications_disabled"
```

Hooks still run with this setting, so the sounds keep playing. Tell the person that permission requests will then be announced by sound alone. Setting the key back to `"auto"` undoes it.

## Fix sounds that play twice

Double sounds mean an older sound hook is still in the settings file. Look through `hooks.Stop`, `hooks.Notification` and `hooks.StopFailure` for commands that run a player such as `afplay`, `paplay`, `aplay` or `ffplay`.

Show the person what you found and remove those entries once they agree. Keep every other hook on those events, because status integrations such as iTerm2's `cc-status` share them and would break if removed.

## Turn it off

For silence that is easy to undo, set the volume to `0`. To stop the plugin entirely, the person can run `/plugin disable pixel-pings`.
