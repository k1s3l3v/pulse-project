set -a && source pulse.env && set +a
alembic revision --autogenerate -m "$1"
exec $SHELL
