To see what's missing, read the [TODO](./TODO.md) file.

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

Finally, run Flask:

```bash
flask run
```

Open your local host and test the following **working** paths:

- http://localhost:5000/register
- http://localhost:5000/login
