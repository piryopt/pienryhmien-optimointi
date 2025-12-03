# OpenShift Guide

For more details, read the tutorial on the [course repository](https://github.com/HY-TKTL/TKT20007-Ohjelmistotuotantoprojekti/tree/master/openshift).

## Staging Environment

You can find the web console from [this link](https://console-openshift-console.apps.ocp-test-0.k8s.it.helsinki.fi).

Alternatively, use the OC CLI, to which you can login with

```bash
oc login -w https://api.ocp-test-0.k8s.it.helsinki.fi:6443
```

## Production Environment

Replace "test" with "prod" in the above links to access the production environment.

## Database Migration

**_NOTE! This method was not used in our project due to many road blocks explained below. If a future group continues development, they can attempt the methods again._**

Install Alembic locally, and initialize it for the project.

Define the database_url for the staging environment and production environment in your .env file. These can be found in OpenShift's Secrets.

The [versions](/migrations/versions) directory contains revisions and the executed SQL command.

Otherwise, you can define more specific configurations in [alembic.ini](/alembic.ini)

SSL / certificate / permission issues...

So far, only manual database editing has been successful.

## Example:

### Step 1. Openshift Deployments

To make database changes, the db-tools pod has to be scaled to 1.

```bash
oc scale deployment db-tools --replicas=1
```

### Step 2. Database access

You need to find the db-tools pod as well as the database url. Once you have them, you can access the database and make edits.

```bash
oc get pods # used for <db-tools-numbers>
```

```bash
oc exec -it <db-tools-numbers> -- psql postgresql://<db_user>:<db_password>@<db>:5432/<db_name>
```

### Step 3. Database edits

In the psql environment, you can make database changes.
BEWARE! CHANGING THE DATABASE CAN BREAK CERTAIN FEATURES, BE CAREFUL AND ADJUST THE CODE ACCORDINGLY!

A line that was used on the staging environment:

```bash
ALTER TABLE survey_choices ADD COLUMN mandatory BOOLEAN DEFAULT FALSE;
```

Production environment works the same.

After the changes set db-tools back to 0:

```bash
oc scale deployment db-tools --replicas=0
```

## Thoughts on solving the issue?

I get a few different kinds of errors when trying to run Alembic for migrations.

### 1. "No pg_hba.conf access for host"

The pg_hba file defines which connections the database can accept. Locally I was able to locate and change the file.

```bash
docker exec -it <container id> bash
cd /var/lib/postgresql/data
echo "hostssl all all 0.0.0.0/0 md5" >> pg_hba.conf
```

This makes it so that valid SSL connections should go through, but that's not the full story. There's another file, postgresql.conf, in the same directory. ssl = off was the default option for me.

```bash
cat postgresql.conf | grep ssl
sed -i 's/ssl = off/ssl = on/' postgresql.conf
```

But even with this turned on, Alembic didn't go through.

I did mention that I changed things locally but that doesn't mean anything for the OpenShift deployment. When I tried to access the same files through the real database, I didn't have the proper permissions in place to access the files.

### 2. "SSL certificate validation failed"

I tried using the certificates found on OpenShift. I would define sslmode=verify-ca in the env.py file, and then point it to the crt files I acquired from OpenShift's Secrets.

But since we are still here, you can guess that it didn't work. I'm kind of stuck here but I've spent too much time on these migrations, so manual changes it is!
