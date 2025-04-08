this shit might not even run shoutout deepseek

read the [TODO](./TODO.md) file to see what's missing

#### Migration Commands (Run these once):

```bash
flask db init          # Initialize migrations
flask db migrate       # Create initial migration
flask db upgrade       # Apply to database
```

#### Key Notes:

- The password handling is intentionally insecure – we'll add proper hashing (like bcrypt) later
- All pages inherit from base.html for consistent navigation
- CSS uses simple grid layout for research projects
- Migration system is ready for future schema changes

#### Next Steps:

1. Run the migrations
2. Test the public pages by visiting:
   - `/` (Home, aka `index.html`)
   - `/about` (todo)
   - /research
3. Try registration/login flow
