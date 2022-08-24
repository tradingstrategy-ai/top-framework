Usage
=====

Help
----

Get help:

.. code-block:: shell

    web-top --help

.. code-block::

     Usage: web-top [OPTIONS] COMMAND [ARGS]...

     web-top is an interactive HTTP request monitor.
     For more information see https://github.com/tradingstrategy-ai/top-framework

    ╭─ Options ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
    │ --install-completion        [bash|zsh|fish|powershell|pwsh]  Install completion for the specified shell. [default: None]                                    │
    │ --show-completion           [bash|zsh|fish|powershell|pwsh]  Show completion for the specified shell, to copy it or customize the installation.             │
    │                                                              [default: None]                                                                                │
    │ --help                                                       Show this message and exit.                                                                    │
    ╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
    ╭─ Commands ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
    │ live             Interactive monitor for active and completed request of your web server.                                                                   │
    │ recent           Print out HTTP requests.                                                                                                                   │
    │ version          Print out application version.                                                                                                             │
    ╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

Live monitoring
---------------

.. code-block::

    web-to live

Open a live `top` like monitor that displays currently active HTTP requests
and recently completed HTTP responses.

Sorted by the longest request first.

You can set the tracker backend from command line option or `TOP_TRACKER_URL` environment variable.

.. code-block::

    ┏━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
    ┃ Cty ┃ IP                   ┃ Worker               ┃ Method   ┃ Path                      ┃ Duration  ┃ User agent                                                                                                                      ┃
    ┡━━━━━╇━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
    │ US  │ 20.241.218.99        │ <Worker 2159194>     │ GET      │ /api/pair-trade-data      │ 1.43      │ python-requests/2.27.1                                                                                                          │
    │ DE  │ 179.61.248.55        │ <Worker 2158801>     │ GET      │ /api/pairs                │ 0.49      │ Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2226.0 Safari/537.36                     │
    └─────┴──────────────────────┴──────────────────────┴──────────┴───────────────────────────┴───────────┴─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
                                                                                                         Completed HTTP responses (1024)
    ┏━━━━━┳━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
    ┃ Cty ┃ IP                  ┃ Ago       ┃ Duration  ┃ Resp ┃ Method   ┃ Path                    ┃ Length       ┃ User agent                                                                                                              ┃
    ┡━━━━━╇━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
    │ US  │ 20.85.75.151        │ 0.41      │ 1.73      │ 200  │ GET      │ /api/pair-trade-data    │ 298          │ python-requests/2.27.1                                                                                                  │
    │ US  │ 20.241.218.99       │ 1.57      │ 2.12      │ 200  │ GET      │ /api/pair-trade-data    │ 289          │ python-requests/2.27.1                                                                                                  │
    │ US  │ 20.85.75.151        │ 2.30      │ 0.05      │ 200  │ GET      │ /api/pair-details       │ 2,527        │ python-requests/2.27.1                                                                                                  │
    │ US  │ 192.241.112.60      │ 2.36      │ 0.25      │ 200  │ GET      │ /api/pairs              │ 228,587      │ Mozilla/5.0 (Windows NT 4.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36             │
    │ US  │ 20.241.218.99       │ 3.82      │ 1.82      │ 200  │ GET      │ /api/pair-trade-data    │ 287          │ python-requests/2.27.1                                                                                                  │
    │ US  │ 192.241.112.60      │ 4.16      │ 0.26      │ 200  │ GET      │ /api/pairs              │ 228,898      │ Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36                    │
    │ FR  │ 54.36.148.85        │ 4.76      │ 0.58      │ 200  │ GET      │ /api/candles            │ 25,994       │ Mozilla/5.0 (compatible; AhrefsBot/7.0; +http://ahrefs.com/robot/)                                                      │
    └─────┴─────────────────────┴───────────┴───────────┴──────┴──────────┴─────────────────────────┴──────────────┴─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

Options:

.. code-block:: shell

    web live --help

.. code-block::

    Usage: web-top live [OPTIONS]

     Interactive monitor for active and completed request of your web server.

    ╭─ Options ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
    │ *  --tracker-url              TEXT   Redis database for HTTP request tracking [env var: TOP_TRACKER_URL] [default: None] [required]                         │
    │    --refresh-rate             FLOAT  How many seconds have between refreshes [env var: TOP_REFRESH_RATE] [default: 2.0]                                     │
    │    --active-columns           TEXT   Comma separated list of columns to be displayed for active HTTP requests [env var: ACTIVE_COLUMNS]                     │
    │                                      [default: Cty, IP, Worker, Method, Path, Duration, User agent]                                                         │
    │    --completed-columns        TEXT   Comma separated list of columns to be displayed for completed HTTP requests [env var: COMPLETED_COLUMNS]               │
    │                                      [default: Cty, IP, Ago, Duration, Resp, Method, Path, Length, User agent]                                              │
    │    --help                            Show this message and exit.                                                                                            │
    ╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯


Recent requests
---------------

.. code-block:: shell

    web-to recent

Display the most recently completed HTTP requests in the terminal.

.. code-block::

    ┏━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━┳━━━━━━━━━━┳━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━┓
    ┃ Cty ┃ IP                      ┃ Ago  ┃ Duration ┃ Resp ┃ Method ┃ Path                    ┃ Length  ┃ User agent              ┃
    ┡━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━╇━━━━━━━━━━╇━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━┩
    │ US  │ 20.241.218.99           │      │ 0.90     │      │ GET    │ /api/candles            │         │ python-requests/2.27.1  │
    │ US  │ 20.85.75.151            │      │ 0.51     │      │ GET    │ /api/candles            │         │ python-requests/2.27.1  │
    │ US  │ 20.85.75.151            │ 0.96 │ 0.79     │ 200  │ GET    │ /api/candles            │ 127,156 │ python-requests/2.27.1  │
    │ AE  │ 2001:8f8:1d0f:2fcd:535… │ 1.56 │ 0.03     │ 200  │ GET    │ /api/top-momentum       │ 40,212  │ Mozilla/5.0 (iPhone;    │
    │     │                         │      │          │      │        │                         │         │ CPU iPhone OS 15_6 like │
    │     │                         │      │          │      │        │                         │         │ Mac OS X)               │
    │     │                         │      │          │      │        │                         │         │ AppleWebKit/605.1.15    │
    │     │                         │      │          │      │        │                         │         │ (KHTML, like Gecko)     │
    │     │                         │      │          │      │        │                         │         │ Version/15.6            │
    │     │                         │      │          │      │        │                         │         │ Mobile/15E148           │
    │     │                         │      │          │      │        │                         │         │ Safari/604.1            │
    │ US  │ 20.241.218.99           │ 1.59 │ 0.83     │ 200  │ GET    │ /api/candles            │ 453,586 │ python-requests/2.27.1  │
    │ AE  │ 2001:8f8:1d0f:2fcd:535… │ 1.63 │ 0.02     │ 200  │ GET    │ /api/impressive-numbers │ 152     │ Mozilla/5.0 (iPhone;    │
    │     │                         │      │          │      │        │                         │         │ CPU iPhone OS 15_6 like │
    │     │                         │      │          │      │        │                         │         │ Mac OS X)               │
    │     │                         │      │          │      │        │                         │         │ AppleWebKit/605.1.15    │
    │     │                         │      │          │      │        │                         │         │ (KHTML, like Gecko)     │
    │     │                         │      │          │      │        │                         │         │ Version/15.6            │
    │     │                         │      │          │      │        │                         │         │ Mobile/15E148           │
    │     │                         │      │          │      │        │                         │         │ Safari/604.1            │
    │ US  │ 20.85.75.151            │ 2.03 │ 0.04     │ 200  │ GET    │ /api/candles            │ 32,915  │ python-requests/2.27.1  │
    │ US  │ 20.241.218.99           │ 3.03 │ 0.70     │ 200  │ GET    │ /api/candles            │ 303,664 │ python-requests/2.27.1  │
    │ US  │ 20.85.75.151            │ 3.29 │ 1.84     │ 200  │ GET    │ /api/pair-trade-data    │ 288     │ python-requests/2.27.1  │
    │ US  │ 20.241.218.99           │ 4.10 │ 0.72     │ 200  │ GET    │ /api/candles            │ 99,651  │ python-requests/2.27.1  │
    │ HU  │ 81.182.158.125          │ 4.57 │ 0.04     │ 200  │ GET    │ /api/top-momentum       │ 575,510 │ python-requests/2.28.1  │
    │ US  │ 20.241.218.99           │ 5.06 │ 0.03     │ 200  │ GET    │ /api/candles            │ 21,311  │ python-requests/2.27.1  │
    │ US  │ 20.85.75.151            │ 5.32 │ 1.86     │ 200  │ GET    │ /api/pair-trade-data    │ 285     │ python-requests/2.27.1  │
    │ US  │ 20.241.218.99           │ 5.36 │ 1.81     │ 200  │ GET    │ /api/pair-trade-data    │ 302     │ python-requests/2.27.1  │
    │ US  │ 20.241.218.99           │ 7.33 │ 1.78     │ 200  │ GET    │ /api/pair-trade-data    │ 302     │ python-requests/2.27.1  │
    └─────┴─────────────────────────┴──────┴──────────┴──────┴────────┴─────────────────────────┴─────────┴─────────────────────────┘

Quit
----

Press `CTRL + C`