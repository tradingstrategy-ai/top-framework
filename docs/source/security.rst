Security
========

Like with all logging frameworks, Top framework may log sensitive
details like passwords and such, especially if passed in URLs.

Remember to keep this in mind when scoping out what are you going to track.

By default

- All HTTP GET parameters get tracked

- No HTTP POST payloads are tracked

- No environment variables from the task target are tracked