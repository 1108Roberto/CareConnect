#!/bin/shell

# Stop and remove containers with volumes.
docker-compose down -v

# Rebuild fresh containers.
docker-compose up -d

echo "This might take a while. Do not cancel this operation."

# Recreate tables with updated schema.
# We wait 20 seconds just to make sure Docker has time to start everything.
sleep 20

python -c " 
from app import app
from app.models import db
with app.app_context():
    db.create_all()
"
