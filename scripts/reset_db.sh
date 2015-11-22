set -e

if [[ -z "$DATABASE_URL" ]]; then
    echo "ERROR: DATABASE_URL environment variable needs to be defined and not empty"
    exit 1
fi

for migration in $(ls slack_ascii/migrations); do
    echo -en 'Removing all tables...\n'
    psql $DATABASE_URL --command="DROP TABLE IF EXISTS emoticon_alias"
    psql $DATABASE_URL --command="DROP TABLE IF EXISTS emoticon"
    echo "Migrating forwards..."
    ./scripts/migrate.sh
done
