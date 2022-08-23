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

                                                                                                               HTTP requests (1026)
    ┏━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━┳━━━━━━━━━━┳━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
    ┃ Cty ┃ IP              ┃ Ago  ┃ Duration ┃ Resp ┃ Method ┃ Path                 ┃ Length  ┃ User agent                                                                                                                                  ┃
    ┡━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━╇━━━━━━━━━━╇━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
    │ US  │ 20.85.75.151    │      │ 0.66     │      │ GET    │ /api/pair-trade-data │         │ python-requests/2.27.1                                                                                                                      │
    │ US  │ 20.241.218.99   │      │ 0.64     │      │ GET    │ /api/candles         │         │ python-requests/2.27.1                                                                                                                      │
    │ US  │ 20.85.75.151    │ 0.83 │ 1.71     │ 200  │ GET    │ /api/pair-trade-data │ 304     │ python-requests/2.27.1                                                                                                                      │
    │ US  │ 20.241.218.99   │ 1.32 │ 0.76     │ 200  │ GET    │ /api/candles         │ 528,032 │ python-requests/2.27.1                                                                                                                      │
    │ US  │ 20.85.75.151    │ 2.71 │ 1.85     │ 200  │ GET    │ /api/pair-trade-data │ 300     │ python-requests/2.27.1                                                                                                                      │
    │ US  │ 20.241.218.99   │ 2.91 │ 0.81     │ 200  │ GET    │ /api/candles         │ 685,175 │ python-requests/2.27.1                                                                                                                      │
    │ US  │ 20.241.218.99   │ 4.34 │ 0.77     │ 200  │ GET    │ /api/candles         │ 363,670 │ python-requests/2.27.1                                                                                                                      │
    │ US  │ 20.85.75.151    │ 4.76 │ 0.05     │ 200  │ GET    │ /api/pair-details    │ 2,486   │ python-requests/2.27.1                                                                                                                      │
    │ SG  │ 139.180.132.162 │ 5.37 │ 0.73     │ 200  │ GET    │ /api/candles         │ 12,441  │                                                                                                                                             │
    │ US  │ 20.241.218.99   │ 5.65 │ 0.05     │ 200  │ GET    │ /api/candles         │ 208,675 │ python-requests/2.27.1                                                                                                                      │
    │ US  │ 20.241.218.99   │ 5.89 │ 1.96     │ 200  │ GET    │ /api/pair-trade-data │ 291     │ python-requests/2.27.1                                                                                                                      │
    │ US  │ 20.85.75.151    │ 7.53 │ 0.06     │ 200  │ GET    │ /api/pair-details    │ 2,486   │ python-requests/2.27.1                                                                                                                      │
    │ US  │ 66.249.66.51    │ 7.99 │ 0.85     │ 200  │ GET    │ /api/pair-details    │ 2,658   │ Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.79 Mobile Safari/537.36  │
    │     │                 │      │          │      │        │                      │         │ (compatible; Googlebot/2.1; +http://www.google.com/bot.html)                                                                                │
    │ US  │ 20.241.218.99   │ 8.03 │ 2.72     │ 200  │ GET    │ /api/pair-trade-data │ 287     │ python-requests/2.27.1                                                                                                                      │
    │ US  │ 20.85.75.151    │ 8.19 │ 0.81     │ 200  │ GET    │ /api/candles         │ 2,477   │ python-requests/2.27.1                                                                                                                      │
    └─────┴─────────────────┴──────┴──────────┴──────┴────────┴──────────────────────┴─────────┴─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
