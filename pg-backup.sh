#!/bin/bash

# PostgreSQL Backup Script

# --- Configuration ---
DB_USER="your_db_user"         # PostgreSQL username
DB_HOST="localhost"            # PostgreSQL host (e.g., localhost, or IP/hostname)
DB_PORT="5432"                 # PostgreSQL port
DB_NAME="your_database_name"   # Name of the database to back up
BACKUP_DIR="/tmp/pg_backups"   # Temporal directory to store backups
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
BACKUP_FILE="${DB_NAME}_${TIMESTAMP}.sql.gz" # .gz for gzip compression

# Full path to the backup file
FULL_BACKUP_PATH="${BACKUP_DIR}/${BACKUP_FILE}"

echo "Starting PostgreSQL backup for database: ${DB_NAME}..."
echo "Backup will be saved to: ${FULL_BACKUP_PATH}"

# Perform the backup using pg_dump and compress it with gzip
# Using -Fc for custom format, which is often more flexible for restores,
# or -Fp | gzip for plain SQL compressed.
# For simplicity, let's use plain SQL compressed with gzip.
pg_dump -U "$DB_USER" -h "$DB_HOST" -p "$DB_PORT" -Fp "$DB_NAME" | gzip > "$FULL_BACKUP_PATH"

# Check if pg_dump was successful
if [ $? -eq 0 ]; then
    echo "Backup completed successfully!"
    echo "Backup size: $(du -sh "$FULL_BACKUP_PATH" | awk '{print $1}')"
    # Set restrictive permissions on the backup file
    chmod 600 "$FULL_BACKUP_PATH"
    echo "Permissions set to 600 for $FULL_BACKUP_PATH"
else
    echo "Error: PostgreSQL backup failed!"
    exit 1
fi

# --- Optional: Further actions ---
# At this point, you would typically upload this file to cloud storage,
# or move it to a more permanent backup location, and then clean up the /tmp file.
# Example:
# rclone copy "$FULL_BACKUP_PATH" "my-remote:backups/postgresql/"
# rm "$FULL_BACKUP_PATH" # Delete the temporary file after successful upload

echo "Script finished."
exit 0
