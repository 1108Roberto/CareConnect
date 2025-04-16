## Running the Application

1. **Start the Docker containers** for MariaDB:

```bash
docker-compose up -d
```

2. **Install dependencies**:

```bash
npm install bcrypt jsonwebtoken mysql2
```

3. **Run the development server**:

```bash
npm run dev
```

4. **Access the application**:
   Open your browser and navigate to `http://localhost:3000`

## Testing the Application

You can test the application with the following credentials:

- **Cedula**: 123456789
- **Password**: password123

For password reset functionality, the token will be displayed in the console since we're running locally without email capabilities.
