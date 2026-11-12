# fullstack_developer_capstone

Repository: xrwvm-fullstack_developer_capstone

Best Cars is a dealership and review portal built with React, Django, an
Express/MongoDB dealership service, and a Flask/VADER sentiment service.
SQLite stores Django users, sessions, car makes and models.

## Run
Use `docker compose up --build` from the repository root. The web application
is available at http://localhost:8000. Run `python manage.py createsuperuser`
inside the web container to create your own admin account. No credentials
are committed. Course sample dealership and review data are seeded once;
restarting services does not erase reviews.

## Verification
`cd server && python manage.py test` tests authentication, validation,
dealer filtering, upstream errors, and review ownership. GitHub Actions also
compiles the React client and checks the Node service syntax.

## Attribution
Based on the Apache-2.0 IBM Skills Network starter project. Implementation,
tests and documentation were prepared with AI assistance and must be
reviewed by the learner. Staff profiles and contact details are fictional
demonstration data. Deployment evidence is collected from actual runs.
