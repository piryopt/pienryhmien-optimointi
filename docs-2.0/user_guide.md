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
# PostgreSQL settings
POSTGRES_USER=your_db_user
POSTGRES_PASSWORD=your_db_password
POSTGRES_DB=your_db_name

# Flask settings
SECRET_KEY=your_secret_key
FLASK_DEBUG=1

# Database URL for Flask SQLAlchemy
DATABASE_URL=postgresql://your_db_user:your_db_password@db:5432/your_db_name
```

---

## 3. Start the Project with Docker Compose

Make sure Docker is installed and running. Then, in your project root, run:

```bash
docker-compose up --build
```

- This will build and start both the web application and the PostgreSQL database.
- The web app will be available at [http://localhost:5001](http://localhost:5001) (or the port you set in `docker-compose.yml`).

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

If you make changes to the code and want to restart the application:

1. Stop the containers (`Ctrl+C`).
2. remove the containers:
   ```bash
   docker compose down
   ```
3. Rebuild and start again:

   ```bash
   docker compose up --build
   ```

   This ensures your changes are included in the running containers.

---

## Troubleshooting

- If you get a "port already in use" error, change the port mapping in `docker-compose.yml`.
- Ensure your `.env` file matches the variables used in `docker-compose.yml` and your Flask configuration.

---
