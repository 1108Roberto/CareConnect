To see what's missing, read the [TODO](./TODO.md) file.

<details>
<summary>Initialization and set-up.</summary>
Create a virtual environment:

```bash
python -m venv ./.venv
```

Then, install the required packages:

```bash
pip install -r ./env/requirements.txt
```

After that, run Docker:

```bash
docker-compose up -d
```

If that command doesn't work, please run:

```bash
docker-compose down -v
```

Then try to run `docker-compose up -d` again.

Finally, run Flask:

```bash
flask run
```

</details>

<details>
<summary>Open your local host and test the following <b>working</b> paths.</summary>

- http://localhost:5000/register
- http://localhost:5000/login
</details>

<details>
<summary><b>(Debug)</b> 500 Server Exception: <i>ProgrammingError</i>.</summary>

This error occurs because the database tables haven't been created in MySQL.

### Solution: Database Initialization

1. Destroy and recreate your Docker containers (**ensures clean slate**):

   - For Linux (Bash):

     ```bash
     ./env/reload.sh
     ```

   - For Windows (PowerShell):

     > [!NOTE]
     > This command will start another instance of PowerShell and execute the commands in `./env/reload.sh` automatically, this is normal.

     ```bash
     Get-Content -Path "./env/reload.sh" -Raw | pwsh
     ```

2. Verify MySQL permissions (**common issue with Docker MySQL**):
   Connect to MySQL directly and verify privileges:

```bash
docker-compose exec mysql mysql -u root -prootpassword
```

In MySQL shell:

```sql
GRANT ALL PRIVILEGES ON clinic_db.* TO 'clinic_user'@'%';
FLUSH PRIVILEGES;
EXIT;
```

### Explanation of the Fix:

1. Database Wipe: The `docker-compose down -v` removes existing data, clearing any legacy schema issues
2. Schema Creation: `db.create_all()` creates tables based on your SQLAlchemy models
3. Permission Fix: MySQL Docker users often need explicit privilege grants
4. Using `clinic_user` instead of root for database connection
5. Matches credentials from `docker-compose.yml`

Test the flow again:

1. Register a new user at `/register`
2. Login at `/login`
3. Access your dashboard

If this does not work, please report it at: [Medical-Appointments Issues](https://github.com/at-sso/Medical-Appointments/issues).

</details>
