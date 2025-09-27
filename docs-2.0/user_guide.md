# User Guide: Project Setup

This guide will help you set up the project from scratch using Docker Compose, including creating the necessary environment variables and PostgreSQL database.

---

## 1. Clone the Repository

```bash
git clone <your-repo-url>
cd pienryhmien-optimointi
```

---

## 2. Create the `.env` File

Create a file named `.env` in the project root with the following content. Replace the values with your own secure choices:

```env
# For dev
POSTGRES_USER=devuser
POSTGRES_PASSWORD=devpass
POSTGRES_DB=dev_db_name
DEV_DATABASE_URL=postgresql://devuser:devpass@db:5432/dev_db_name
DEV_SECRET_KEY=dev_secret

# For test
TEST_POSTGRES_USER=testuser
TEST_POSTGRES_PASSWORD=testpass
TEST_POSTGRES_DB=test_db_name
TEST_DATABASE_URL=postgresql://testuser:testpass@test-db:5432/test_db_name
TEST_SECRET_KEY=test_secret


# Debug on "1" else "0"
FLASK_DEBUG=1
```

---

## 3. Start the Project with Docker Compose (development environment or testing environment)

Make sure Docker is installed and running. Then, in your project root, run development environment with:

```bash
docker compose up web db --build
```

- This will build and start both the web application and the PostgreSQL development database
- The web app will be available at [http://localhost:5001](http://localhost:5001) (or the port you set in `docker-compose.yml`).

To run the application in testing environment which uses the test database run:

```bash
docker compose run --rm test
```

---

## 4. Access the Application

- Open your browser and go to [http://localhost:5001](http://localhost:5001).
- For local development, you can log in using the mock login page at `/auth/login`.
- Username will be either robottiStudent or robottiTeacher and any password.

---

## 5. Managing Docker Containers

### Stop the Containers

To stop the running containers, press `Ctrl+C` in the terminal where Docker Compose is running.

Alternatively, in a new terminal window, run:

### Remove Containers and Volumes

To stop and **remove** all containers, networks, and volumes created by Docker Compose, run:

```bash
docker compose down -v
```

- The `-v` flag also removes named volumes (including your database data), so use with caution if you want to keep your data.

### Restart the Application After Code Changes

Changes to web page should be automatically visible after refreshing the page.

But just in case if you make changes to the code and want to restart the application manually:

1. Stop the containers (`Ctrl+C`).
2. remove the containers:

   ```bash
   docker compose down
   ```

3. Rebuild and start again:

   ```bash
   docker compose up web db --build
   ```

   This ensures your changes are included in the running containers.

---

## Troubleshooting

- If you get a "port already in use" error, change the port mapping in `docker-compose.yml`.
- Ensure your `.env` file matches the variables used in `docker-compose.yml` and your Flask configuration.

---
