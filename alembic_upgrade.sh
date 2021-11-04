set -a && source pulse.env && set +a
alembic upgrade head
exec $SHELL
