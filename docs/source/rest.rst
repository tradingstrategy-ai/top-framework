.. _rest:

REST API endpoint tracking backend
==================================

REST API endpoint tracking backend
returns the active HTTP requests and completed HTTP responses
from your web server directly.

Your web server must implement the API.

`The reference implementation is available for Node.js as web-top-node package <https://www.npmjs.com/package/@trading-strategy-ai/web-top-node>`_.

Usage
-----

Start `web-top` and pass API key and tracking API endpoint URL:

.. code-block:: shell

    # The API key that you gave for your web server integration
    export TOP_WEB_API_KEY=...

    # Start web-top by using REST API
    # to get the active tasks
    web-top live --tracker-url="http://localhost:3000/tracker"
