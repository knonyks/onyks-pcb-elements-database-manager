#!/bin/bash
set -e

echo "--- START ENTRYPOINT ---"

# 1. Wait for PostgreSQL to be ready
echo "Czekam na uruchomienie PostgreSQL..."
until pg_isready -h postgres -p 5432 -U "$POSTGRES_USER"; do
  echo "Postgres nie gotowy... czekam..."
  sleep 2
done
echo "Postgres jest gotowy!"

# 2. Create SVN repository if it doesn't exist
if [ ! -d "/var/svn/$SVN_REPO_NAME" ]; then
    echo "Tworzenie repozytorium SVN: $SVN_REPO_NAME"
    mkdir -p /var/svn
    svnadmin create /var/svn/$SVN_REPO_NAME
    chown -R www-data:www-data /var/svn
fi

# 3. Generate Apache config from template
envsubst '\$POSTGRES_USER \$POSTGRES_PASSWORD \$POSTGRES_DB \$SVN_REPO_NAME' \
    < /usr/local/apache2/conf/httpd.conf.template \
    > /usr/local/apache2/conf/httpd.conf

4. Loop for syncing authz file from PostgreSQL
sync_authz_file() {
    echo "Uruchamiam proces synchronizacji uprawnień w tle..."
    
    # Infinite loop for syncing authz file every 10 seconds
    while true; do
        # Create a temporary file with the header
        echo "[/]" > /tmp/svn-authz.tmp
        
        export PGPASSWORD=$POSTGRES_PASSWORD
        
        # Download login and rank from PostgreSQL and append to the temp authz file
        # If the query fails (e.g. database is down), we skip this iteration and try again in 10 seconds
        if psql "host=postgres dbname=$POSTGRES_DB user=$POSTGRES_USER" -Atc \
           "SELECT login, rank FROM private.users;" >> /tmp/svn-authz.tmp 2>/dev/null; then
           
           # Process the downloaded data to convert ranks to permissions
           # Here we read the temp file line by line, convert ranks to permissions, and write to another temp file
           # We use a case statement to map ranks to permissions (admin and editor get rw, user gets r)
           
           # Clean up the tmp file to only have login and rank
           psql "host=postgres dbname=$POSTGRES_DB user=$POSTGRES_USER" -Atc \
           "SELECT login, rank FROM private.users;" | while IFS='|' read login rank; do
                case $rank in
                    admin) echo "$login = rw" ;;
                    editor) echo "$login = rw" ;;
                    user) echo "$login = r" ;;
                esac
           done > /tmp/svn-perms.tmp

           # Concat the header and permissions into the final authz file
           echo "[/]" > /tmp/svn-authz.final
           cat /tmp/svn-perms.tmp >> /tmp/svn-authz.final

           # Replace the main authz file if there are changes
           if ! cmp -s /tmp/svn-authz.final /etc/svn-authz; then
               cp /tmp/svn-authz.final /etc/svn-authz
               chown www-data:www-data /etc/svn-authz
               chmod 640 /etc/svn-authz
               echo "$(date) - Zaktualizowano uprawnienia SVN z bazy."
           fi
        fi
        
        # Wait for 10 seconds before next sync
        sleep 10
    done
}

# Run the sync_authz_file function in the background
sync_authz_file &

# =================================================================

echo "Konfiguracja gotowa. Uruchamiam Apache."

# 5. Start Apache in foreground
exec "$@"