#!/bin/sh
# Plays one bundled sound: play.sh done|attention|limit
# Always exits 0, because a machine without a player should stay quiet
# rather than report a hook error after every turn.

root="${CLAUDE_PLUGIN_ROOT:-$(dirname "$0")/..}"
sound="$root/sounds/$1.wav"
volume="${PIXEL_PINGS_VOLUME:-1}"

case "$volume" in
  '' | *[!0-9.]*) volume=1 ;;
esac

[ -f "$sound" ] || exit 0

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
