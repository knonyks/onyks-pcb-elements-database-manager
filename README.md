![](/other/banner.png)

### 📖 Description

A centralized database system for Altium PCB components, integrated with an SVN repository for `SchLib` and `PcbLib` files. This project provides a web interface for managing component data (footprints, symbols, stock quantities) and ensures seamless access control for organizational users.

The system acts as a bridge between the Altium Designer environment and a Postgres database, managed via a web application.

## Installation Guide

Follow the steps below to set up the environment, configure the database, and start the services.

#### 1. Download the repository

Download the project using one of the following methods:

```bash
# 1. Download the latest released version (recommended)
git clone --branch v0.2.0-beta --depth 1 https://github.com/knonyks/onyks-bloodstone.git

# 2. Download the latest version
git clone https://github.com/knonyks/onyks-bloodstone.git

# 3. Download the development branch
git clone --branch dev --single-branch https://github.com/knonyks/onyks-bloodstone.git
```

#### 2. Create the configuration file
Go to the project directory and create a `.env` file:

```bash
# go to the repository folder
cd onyks-bloodstone

# Linux
touch .env

# Windows
notepad .env
```

Add your configuration values. For example:
```dotenv
# login to the database
POSTGRES_USER=appuser

# password to the database
POSTGRES_PASSWORD=strongpassword

# database's name
POSTGRES_DB=appdb

# All paths can be absolute
# Destination folder for PostgreSQL data
POSTGRES_DATA_PATH=./path/to/postgres

# Host port for PostgreSQL
POSTGRES_PORT=8112

# Host port for the whole server - website, repository, etc.
PROXY_PORT=8113

# Repository name
SVN_REPO_NAME=elements

# Destination path for repository files
SVN_DATA_PATH=./path/to/svn

# Host port for SVN
SVN_PORT=8111

# Destination path for datasheet PDFs
DATASHEET_UPLOAD_PATH=./path/to/datasheets
```

#### 3. Run the containers
Start the containers with your configuration:
```bash
docker compose --env-file .env up
```

#### 4. Add a user to the database

Finally, create a database user who can access the repository. First, identify the database container:

```bash
docker ps
```

Find the database container in the `NAMES` column. It is typically named `onyks-bloodstone-database`. Then open a PostgreSQL shell in the container:

```bash
docker exec -it onyks-bloodstone-database psql -U appuser -d appdb
```


In the PostgreSQL shell, add a user with your preferred credentials:
```bash
INSERT INTO private.users (login, password, email, rank)
VALUES ('admin', crypt('admin', gen_salt('bf')), 'admin@test.pl', 'editor');
```

When finished, exit PostgreSQL by typing:
```bash
\q
```

The application should now be ready to use.

### Third-Party Software

This project uses third-party software, including Docker, PostgreSQL, Apache Subversion (SVN), and other tools that will be added in the future.

<!-- ### License -->



Altium is trademark of Altium Limited. All other trademarks are property of their respective owners.

<!-- ---

### 🚀 Current Status

#### ✅ Working Features
- [x] **SVN Repository Initialization**: Automated setup of the Subversion repository.
- [x] **User Authentication**: Access to SVN via database credentials (login/password).
- [x] **RBAC (Role-Based Access Control)**:
    - User ranking system.
    - Commit and update permissions based on user rank.
- [x] **Database Integration**: PostgreSQL backend for user and component data.
- [x] **Server Configuration**:
    - **Nginx**: Serving the SVN repository.
    - **Apache**: Handling user management for SVN access.
- [x] **Docker Integration**: Basic containerization support for easy deployment.

#### 🚧 Todo / Roadmap
- [ ] **Backend Migration**: Implement **FastAPI** to replace the legacy Flask system.
- [ ] **Frontend Framework**: Implement **Vue.js** for a modern web interface.
- [ ] **Time-Limited Access**: Implement SVN access checks based on `expiration_time`.
- [ ] **Management App**: Develop a dedicated dashboard for system administration.
- [ ] **AI Integration**: Implement LLM (Large Language Model) for automatic component description generation.
- [ ] **Auth System Overhaul**: Modernize the logging and authentication system.

---

### 🛠 Tech Stack
*   **Version Control:** Subversion (SVN)
*   **Database:** PostgreSQL
*   **Infrastructure:** Docker, Nginx, Apache
*   **Backend:** Python (Flask → moving to FastAPI)
*   **Frontend:** Vue.js (planned)



```bash
# list of containers
docker ps

# 
docker exec -it postgres psql -U appuser -d appdb
```

#### 1. Generate SSL Certificates
First, create a directory for the certificates and generate a self-signed SSL certificate (or place your own valid certificates in the directory).

```bash
mkdir -p /home/xyz/certs
openssl req -x509 -nodes -days 365 \
  -newkey rsa:2048 \
  -keyout /home/xyz/certs/privkey.pem \
  -out /home/xyz/certs/fullchain.pem \
  -subj "/CN=localhost"
```

#### 2. Configuration
Create an environment file (e.g., `example.env`) in the root of your project repository. Customize the paths and credentials to match your system configuration.

**File:** `example.env`
```dotenv
# PostgreSQL Configuration
POSTGRES_USER=appuser
POSTGRES_PASSWORD=strongpassword
POSTGRES_DB=appdb
POSTGRES_DATA_PATH=/home/xyz/postgres
POSTGRES_PORT=8112

# SVN / Apache Configuration
SVN_REPO_NAME=elements
SVN_DATA_PATH=/home/xyz/svn
SVN_PORT=8111

# Nginx / SSL Configuration
DOMAIN=localhost   # Local IP address or domain name
SSL_CERT_PATH=/home/xyz/certs
FRONTEND_PORT=8110
SVN_PATH=/svn
```

#### 3. Build and Start Services
Navigate to the project folder and run the following command to build and start the containers using the specified environment file:

```bash
CONFIG_FILE=example.env docker-compose --env-file example.env up -d --build
```

#### 4. Create Initial User
Once the containers are running, you need to create the first user in the database.

1. Access the PostgreSQL container:
   ```bash
   docker exec -it postgres psql -U appuser -d appdb
   ```

2. Insert the user record (you can assign ranks like `user`, `editor`, or `admin`):
   ```sql
   INSERT INTO private.users (login, password, email, rank)
   VALUES ('admin', crypt('admin', gen_salt('bf')), 'admin@test.pl', 'editor');
   ```

3. Exit the database console:
   ```bash
   exit
   ```

#### 5. SVN Usage Examples
You can now interact with the SVN repository using the following commands:

```bash
# Checkout the repository
svn checkout https://localhost:8111/svn/elements --username admin --password admin --trust-server-cert --non-interactive

# Add files
svn add --force .

# Commit changes
svn commit -m "Initial commit" --username admin --password admin --trust-server-cert --non-interactive

# Update repository
svn update --username admin --password admin --trust-server-cert --non-interactive
```

Altium is trademark of Altium Limited. All other trademarks are property of their respective owners. -->


<!-- docker compose --env-file .env up database proxy backend

docker compose up -d --build backend

docker-compose down -v; docker-compose build; CONFIG_FILE=.env docker compose --env-file .env up database proxy svn -->