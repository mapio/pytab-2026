#!/bin/bash

USERS="snd:sndp@foo.bar,rec:recp@goo.bar"

DIR="$(cd "$(dirname "$0")" && pwd)"
JAR="$DIR/greenmail-standalone-2.1.8.jar"

stop_all() {
    echo "Stopping..."
    docker rm -f roundcube 2>/dev/null || true
    [ -n "$GREENMAIL_PID" ] && kill "$GREENMAIL_PID" 2>/dev/null || true
}

if [ "${1-}" = "cleanup" ]; then
    echo "Cleaning up stale processes..."
    docker rm -f roundcube 2>/dev/null || true
    pkill -f 'greenmail-standalone' 2>/dev/null || true
    exit 0
fi

trap stop_all INT TERM

java -jar \
    -Dgreenmail.setup.test.all \
    -Dgreenmail.users.login=email \
    "-Dgreenmail.users=${USERS}" \
    "$JAR" >/dev/null 2>&1 &
GREENMAIL_PID=$!
echo "GreenMail started (pid $GREENMAIL_PID)"
sleep 2

docker run -d \
    --name roundcube \
    --network host \
    -e ROUNDCUBEMAIL_DEFAULT_HOST=127.0.0.1 \
    -e ROUNDCUBEMAIL_DEFAULT_PORT=3143 \
    -e ROUNDCUBEMAIL_SMTP_SERVER=127.0.0.1 \
    -e ROUNDCUBEMAIL_SMTP_PORT=3025 \
    -e 'ROUNDCUBEMAIL_SMTP_USER=%u' \
    -e 'ROUNDCUBEMAIL_SMTP_PASS=%p' \
    -e ROUNDCUBEMAIL_DB_TYPE=sqlite \
    -v roundcube-data:/var/roundcube/db \
    roundcube/roundcubemail >/dev/null
echo "Roundcube started at http://localhost  (Ctrl-C to stop)"

wait $GREENMAIL_PID
