#!/bin/sh
# Plays one bundled sound: play.sh done|attention|limit [--stop-hook]
# Always exits 0, because a machine without a player should stay quiet
# rather than report a hook error after every turn.
#
# With --stop-hook, the Stop hook's JSON input is read from stdin. While a
# background subagent is still running, the end of a turn is only a pause:
# Claude starts another turn when the subagent reports back, so the sound
# waits for the turn that finishes the work. Other background tasks, such as
# a dev server in a background shell, can run for the whole session, so
# they do not hold the sound back.

root="${CLAUDE_PLUGIN_ROOT:-$(dirname "$0")/..}"
sound="$root/sounds/$1.wav"
volume="${PIXEL_PINGS_VOLUME:-1}"

case "$volume" in
  '' | *[!0-9.]*) volume=1 ;;
esac

[ -f "$sound" ] || exit 0

if [ "$2" = "--stop-hook" ]; then
  input=$(cat)
  if printf '%s\n' "$input" | grep -q '"type"[[:space:]]*:[[:space:]]*"subagent"'; then
    exit 0
  fi
fi

if command -v afplay >/dev/null 2>&1; then
  afplay -v "$volume" "$sound"
elif command -v paplay >/dev/null 2>&1; then
  paplay --volume="$(awk -v v="$volume" 'BEGIN { printf "%d", v * 65536 }')" "$sound"
elif command -v ffplay >/dev/null 2>&1; then
  ffplay -nodisp -autoexit -loglevel quiet -af "volume=$volume" "$sound"
elif command -v aplay >/dev/null 2>&1; then
  aplay -q "$sound"
fi

exit 0
