#!/bin/bash

# PostgreSQL pg_dumpall Backup Script (for all databases)

# --- Configuration ---
DB_USER="your_superuser_user" # A superuser is typically required for pg_dumpall
DB_HOST="localhost"           # PostgreSQL host
DB_PORT="5432"                # PostgreSQL port
BACKUP_DIR="/tmp/pg_cluster_backups" # Temporal directory to store the full cluster backup
# Optional: Set PGPASSWORD environment variable if not using .pgpass or trust authentication
# export PGPASSWORD="your_db_password"

# --- Script Logic ---

# Create the backup directory if it doesn't exist
mkdir -p "$BACKUP_DIR"

# Check if the directory was created successfully
if [ ! -d "$BACKUP_DIR" ]; then
    echo "Error: Could not create backup directory $BACKUP_DIR"
    exit 1
fi

# Generate a timestamp for the filename
TIMESTAMP=$(date +%Y%m%d)
BACKUP_FILE="pg_dump_${TIMESTAMP}.sql.gz" # .gz for gzip compression

# Full path to the backup file
FULL_BACKUP_PATH="${BACKUP_DIR}/${BACKUP_FILE}"

echo "Starting PostgreSQL cluster backup (all databases and globals)..."
echo "Backup will be saved to: ${FULL_BACKUP_PATH}"

# Perform the backup using pg_dumpall and compress it with gzip
# Note: pg_dumpall output is plain SQL, so gzip is very effective.
pg_dumpall -U "$DB_USER" -h "$DB_HOST" -p "$DB_PORT" | gzip > "$FULL_BACKUP_PATH"

# Check if pg_dumpall was successful
if [ $? -eq 0 ]; then
    echo "Cluster backup completed successfully!"
    echo "Backup size: $(du -sh "$FULL_BACKUP_PATH" | awk '{print $1}')"
    # Set restrictive permissions on the backup file
    chmod 600 "$FULL_BACKUP_PATH"
    echo "Permissions set to 600 for $FULL_BACKUP_PATH"
else
    echo "Error: PostgreSQL cluster backup failed!"
    exit 1
fi

echo "Script finished."
exit 0
