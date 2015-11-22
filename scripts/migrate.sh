set -e

if [[ -z "$DATABASE_URL" ]]; then
    echo "ERROR: DATABASE_URL environment variable needs to be defined and not empty"
    exit 1
fi

for migration in $(ls slack_ascii/migrations); do
    echo "Migrating $migration..."
    psql $DATABASE_URL < migrations/$migration
done
