set -e

if [[ -z "$DATABASE_URL" ]]; then
    echo "ERROR: DATABASE_URL environment variable needs to be defined and not empty"
    exit 1
fi

MIGRATIONS_DIR='slack_ascii/migrations'
for migration in $(ls $MIGRATIONS_DIR); do
    echo "Migrating $migration..."
    psql $DATABASE_URL < $MIGRATIONS_DIR/$migration
done
