set -a && source pulse.env && set +a
alembic downgrade -1
exec $SHELL
