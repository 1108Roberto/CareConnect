### Phase 1: Planning & Environment Setup (FINISHED)

1.  **Refine Requirements:** Although the diagram gives a good overview, flesh out the specific details: What exact fields are needed for clients, policies, and claims? What actions can users perform on each screen?
2.  **Choose Technology Stack:**
    - **Database:** MariaDB (as requested).
    - **Backend:** You'll need a server-side language to interact with the database and handle logic (e.g., PHP, Python with Flask/Django, Node.js with Express, Java with Spring).
    - **Frontend:** HTML, CSS (for styling), and JavaScript (for interactivity and communication with the backend).
3.  **Setup Development Environment:**
    - Install MariaDB Server.
    - Install a database management tool (optional but helpful, e.g., DBeaver, HeidiSQL, phpMyAdmin).

### Phase 2: MariaDB Development (FINISHED)

1.  **Design the Database Schema:** Based on the screens, identify the core data entities: Users, Clients, Policies, Claims.
    - **Users Table:** To handle login (`users`).
    - **Clients Table:** To store client information (`clients`).
    - **Policies Table:** To store policy details, linked to clients (`policies`).
    - **Claims Table:** To store claim details, linked to policies and clients (`claims`).
2.  **Define Table Structures:** Specify columns, data types, primary keys (PK), and foreign keys (FK) to link tables.

    - `clients` table:
      - `client_id` (INT, PK, AUTO_INCREMENT)
      - `name` (VARCHAR)
      - `national_id` (VARCHAR, UNIQUE) - Or appropriate ID type
      - `address` (TEXT)
      - `phone` (VARCHAR)
      - `email` (VARCHAR, UNIQUE)
      - `created_at` (TIMESTAMP)
      - `updated_at` (TIMESTAMP)
    - `policies` table:
      - `policy_id` (INT, PK, AUTO_INCREMENT)
      - `client_id` (INT, FK referencing `clients.client_id`)
      - `policy_number` (VARCHAR, UNIQUE)
      - `branch` (VARCHAR) - e.g., 'Auto', 'Home', 'Life'
      - `start_date` (DATE)
      - `end_date` (DATE)
      - `status` (VARCHAR) - e.g., 'Active', 'Expired', 'Cancelled'
      - `premium_amount` (DECIMAL)
      - `created_at` (TIMESTAMP)
      - `updated_at` (TIMESTAMP)
    - `claims` table:
      - `claim_id` (INT, PK, AUTO_INCREMENT)
      - `policy_id` (INT, FK referencing `policies.policy_id`)
      - `client_id` (INT, FK referencing `clients.client_id`) // Optional, can be derived via policy
      - `claim_number` (VARCHAR, UNIQUE)
      - `date_of_incident` (DATE)
      - `date_reported` (DATE)
      - `status` (VARCHAR) - e.g., 'Open', 'Processing', 'Closed', 'Rejected'
      - `description` (TEXT)
      - `created_at` (TIMESTAMP)
      - `updated_at` (TIMESTAMP)
    - `users` table (for login):
      - `user_id` (INT, PK, AUTO_INCREMENT)
      - `username` (VARCHAR, UNIQUE)
      - `password_hash` (VARCHAR) - **Never store plain passwords!**
      - `email` (VARCHAR, UNIQUE)
      - `full_name` (VARCHAR)
      - `created_at` (TIMESTAMP)

3.  **Create the Database and Tables in MariaDB:**

- Connect to your MariaDB server using a command-line client or GUI tool.
- Create the database:
  ```sql
  CREATE DATABASE your_app_db_name CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
  ```
- Select the database:
  ```sql
  USE your_app_db_name;
  ```
- Execute `CREATE TABLE` SQL statements for each table designed above. Example for `clients`:

  ```sql
  CREATE TABLE clients (
      client_id INT AUTO_INCREMENT PRIMARY KEY,
      name VARCHAR(255) NOT NULL,
      national_id VARCHAR(50) UNIQUE,
      address TEXT,
      phone VARCHAR(30),
      email VARCHAR(255) UNIQUE,
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
  ) ENGINE=InnoDB; -- Specify InnoDB engine for foreign key support

  -- Add other CREATE TABLE statements here for policies, claims, users
  -- Remember to include FOREIGN KEY constraints
  ALTER TABLE policies ADD CONSTRAINT fk_policies_client FOREIGN KEY (client_id) REFERENCES clients(client_id);
  ALTER TABLE claims ADD CONSTRAINT fk_claims_policy FOREIGN KEY (policy_id) REFERENCES policies(policy_id);
  -- Add other constraints as needed
  ```

4.  **Populate with Test Data (Optional):** Add some sample data to test your application later.

### Phase 3: Backend Development (FINISHED)

1.  **Set up Project Structure:** Organize your backend code (e.g., controllers/views, models, database connection logic).
2.  **Database Connection:** Write code to connect your backend application to the MariaDB database.
3.  **Create Core Logic/API Endpoints:**
    - **Authentication:** Implement login (verifying username/password hash) and logout functionality. Secure session management.
    - **Data Retrieval:** Create functions/endpoints to:
      - Fetch client details based on an ID or search criteria.
      - Fetch a list of policies for a specific client.
      - Fetch a list of claims for a specific client or policy.
      - Fetch details for a specific policy or claim.
    - **Data Modification (If needed):** Functions/endpoints to create or update records (ensure proper authorization).

### Phase 4: Frontend Development (HTML, CSS, JavaScript)

1.  **Create HTML Structure (`.html` files):** Based on the diagram, create the HTML for each screen. Let's focus on the "Client Screen":

    - **`client_dashboard.html` (Example):**

      ```html
      <!DOCTYPE html>
      <html lang="en">
        <head>
          <meta charset="UTF-8" />
          <meta
            name="viewport"
            content="width=device-width, initial-scale=1.0"
          />
          <title>Client Dashboard</title>
          <link rel="stylesheet" href="style.css" />
        </head>
        <body>
          <header>
            <img src="path/to/logo.png" alt="Company Logo" id="logo" />
            <div class="user-info">
              <span>Welcome, <span id="username">[Username]</span>!</span>
              <button id="logout-button">Logout</button>
            </div>
            <nav>
              <ul>
                <li><a href="#">Dashboard</a></li>
                <li><a href="#">Profile</a></li>
                <li><a href="#">Search</a></li>
              </ul>
            </nav>
          </header>

          <main>
            <h1>Client Information</h1>
            <section id="client-info-section">
              <h2>Client Details</h2>
              <div id="client-details">
                <p>
                  <strong>Name:</strong>
                  <span id="client-name">Loading...</span>
                </p>
                <p>
                  <strong>ID:</strong> <span id="client-id">Loading...</span>
                </p>
                <p>
                  <strong>Address:</strong>
                  <span id="client-address">Loading...</span>
                </p>
                <p>
                  <strong>Phone:</strong>
                  <span id="client-phone">Loading...</span>
                </p>
                <p>
                  <strong>Email:</strong>
                  <span id="client-email">Loading...</span>
                </p>
              </div>
            </section>

            <section id="policies-section">
              <h2>Policies / Branches</h2>
              <table id="policies-table">
                <thead>
                  <tr>
                    <th>Policy Number</th>
                    <th>Branch</th>
                    <th>Status</th>
                    <th>End Date</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td colspan="5">Loading policies...</td>
                  </tr>
                </tbody>
              </table>
            </section>

            <section id="claims-section">
              <h2>Claims / Incidents</h2>
              <table id="claims-table">
                <thead>
                  <tr>
                    <th>Claim Number</th>
                    <th>Policy Number</th>
                    <th>Date Reported</th>
                    <th>Status</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td colspan="5">Loading claims...</td>
                  </tr>
                </tbody>
              </table>
            </section>
          </main>

          <footer>
            <p>&copy; 2025 Your Company Name. All rights reserved.</p>
            <ul>
              <li><a href="#">Privacy Policy</a></li>
              <li><a href="#">Terms of Service</a></li>
              <li><a href="#">Contact Us</a></li>
            </ul>
          </footer>

          <script src="script.js"></script>
        </body>
      </html>
      ```

    - Create similar HTML structures for the Login screen, Policy Detail screen, Claim Detail screen, etc.

2.  **Style with CSS (`style.css`):**

    - Write CSS rules to style the header, navigation, main content sections, tables, forms, footer, etc., to match your desired look and feel. Use classes and IDs defined in your HTML.
    - Make it responsive using media queries so it looks good on different screen sizes.

3.  **Add Interactivity with JavaScript (`script.js`):**
    - **Fetch Data:** Use the `Workspace` API or `XMLHttpRequest` to call your backend API endpoints when the page loads (or based on user actions).
    - **Populate HTML:** Once data is received from the backend, use JavaScript to dynamically update the content of elements (e.g., fill in client details, populate table rows for policies and claims).
    - **Handle User Actions:** Add event listeners to buttons (Logout, View Details) and links. For example, clicking a "View Details" link in the policies table might fetch detailed policy data and either display it in a modal or navigate to the Policy Detail page.
    - **Handle Forms:** Manage form submissions (like the Login form).

### Phase 5: Integration & Testing

1.  **Connect Frontend & Backend:** Ensure the JavaScript `Workspace` calls correctly target your backend API endpoints and handle the responses (both success and errors).
2.  **Testing:**
    - **Unit Tests:** Test individual backend functions (database queries, logic).
    - **Integration Tests:** Test the interaction between frontend and backend (API calls).
    - **End-to-End Tests:** Simulate user flows (login, view client, view policy details, etc.).
    - **Cross-Browser Testing:** Test in different web browsers.

### Phase 6: Deployment

1.  **Choose Hosting:** Select a hosting provider that supports your chosen technology stack (backend language, MariaDB database).
2.  **Configure Server:** Set up the web server, database, and application environment on the hosting server.
3.  **Deploy Code:** Transfer your backend and frontend code to the server.
4.  **Domain Setup:** Point your domain name (if any) to the server.
