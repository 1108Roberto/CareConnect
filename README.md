## Running the Application

1. **Start the Docker containers** for MariaDB:

   ```bash
   docker-compose up -d
   ```

2. **Initialize the Database**:
   You need to apply the SQL schema from `db/init.sql` to your database. You can do this using a MySQL client or by running:

   ```bash
   docker exec -i care-connect_db_1 mysql -uroot -pAdminroot123 < db/init.sql
   ```

3. **Install dependencies**:

   ```bash
   npm install
   ```

4. **Run the development server**:

   ```bash
   npm run dev
   ```

5. **Access the application**:
   Open your browser and navigate to `http://localhost:3000`

## Testing the Application

You can test the application with the following credentials:

- **Cedula**: 123456789
- **Password**: password123

For password reset functionality, the token will be displayed in the console since we're running locally without email capabilities.
