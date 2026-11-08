# Pixel Pings

8-bit notification sounds for [Claude Code](https://claude.com/claude-code). You hear a short chiptune cue when Claude finishes or needs you, and nothing nags you if you step away.

[Українська версія](README.uk.md)

## What it does

| Sound | Plays when | Character |
|---|---|---|
| [`done`](sounds/done.wav) | Claude finishes a turn | quick rising arpeggio, like clearing a level |
| [`attention`](sounds/attention.wav) | Claude needs a permission or an answer | double beep with a questioning tone |
| [`limit`](sounds/limit.wav) | a turn stops on a rate limit | falling phrase with a noise hit, like losing a life |

Claude Code also sends a reminder after about a minute of waiting for you. Pixel Pings stays silent on that one, so a finished task gets one sound rather than a second ping while you are away.

When Claude runs subagents in the background, its turn can end while they are still working and resume as each one reports back. Pixel Pings stays silent on those in-between turns and plays `done` once, after the last subagent has finished.

## Install

At the prompt of a Claude Code terminal session:

```
/plugin install pixel-pings --marketplace DaKoshin/pixel-pings
```

Answer `y` to add the marketplace, then pick a scope. The user scope is the first option and covers all your projects.

From a shell:

```sh
claude plugin install pixel-pings --marketplace DaKoshin/pixel-pings
```

In the desktop app, click **+** next to the prompt box, then **Plugins**, **Add marketplace** with `DaKoshin/pixel-pings`, then **Add plugin**.

## Configure

Ask Claude in your own words, or run `/pixel-pings:setup`. It can:

- play the sounds so you can hear them
- make them louder, quieter or silent
- turn off Claude Code's terminal banners, such as iTerm2 notifications
- remove older sound hooks if you hear everything twice

The volume is the `PIXEL_PINGS_VOLUME` variable in the `env` block of `~/.claude/settings.json`. `1` is the default, `1.5` is 50% louder, and `0` mutes.

## Make your own sounds

Every sound is synthesized by [`scripts/generate.py`](scripts/generate.py) using only the Python standard library. Fork the repository, edit the notes in `SOUNDS`, and run:

```sh
python3 scripts/generate.py
```

## Requirements

| Platform | Status |
|---|---|
| macOS | Tested. Uses the built-in `afplay`. |
| Linux | Should work with `paplay`, `ffplay` or `aplay`, but is untested. `aplay` ignores the volume setting. |
| Windows | Not supported yet. |

## License

[MIT](LICENSE). The sounds were made for this project, so you can use them under the same license.

This is an unofficial community plugin, not affiliated with Anthropic.
