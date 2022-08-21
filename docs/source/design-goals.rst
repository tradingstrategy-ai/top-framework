Design goals
============

- **Simplicity**: Less lines of code is better. This is why Redis and Textualize where chosen as the foundational building blocks.

- **Extensibility**: If you have a special use case you should be easily include your logic.

Out of scope
------------

- **Not secure**: All processes are assumed to be trusted, to keep it simple. Assume everything runs in a trusted environment you control.

- **Not scalable**: We do not assume we can handle millions of requests or tasks. Instead, we focus keeping things simple so you can easily extend without needing to understand high level of software reliability engineering.
