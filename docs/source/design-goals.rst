Design goals
============

Top framework aims to provide you a useful custom monitoring tool with very little effort.

The framework aims for:

- **Simplicity**: Less lines of code is better. This is why Redis and Textualize where chosen as the foundational building blocks.

- **Extensibility**: If you have a special use case you should be easily include your logic.

Out of scope
------------

- **Not scalable**: We do not assume we can handle millions of requests or tasks. Instead, we focus keeping things simple so you can easily extend without needing to understand high level of software reliability engineering. The optimal spot is services doing max 40-50 requests/tasks per second with a flow that a human eye can follow.

- **Not secure**: All processes are assumed to be trusted. Assume everything runs in a trusted environment you control. By not having authentication and authorization or permissions and only offering this tool for sysadmins we can keep the code structure simple.
