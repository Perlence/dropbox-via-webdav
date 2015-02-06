Dropbox via WebDAV
==================

*Access your Dropbox via WebDAV interface*


Installation
------------

-   Clone the repository:

    ```bash
    git clone https://github.com/Perlence/dropbox-via-webdav.git
    cd dropbox-via-webdav
    ```

-   Create and activate virtual environment:

    ```bash
    $ virtualenv env
    $ . env/bin/activate
    ```

-   Install requirements:

    ```bash
    $ pip install -r requirements.txt
    ```

-   Install the package:

    ```bash
    $ python setup.py install
    ```


Configuration
-------------

-   Create a Dropbox application with full access.

    -   Go to [App Console](https://www.dropbox.com/developers/apps/create).

    -   Select **Dropbox API app**.

    -   Select **Files and datastores**.

    -   Select **No — My app needs access to files already on Dropbox**.

    -   Select **All — file types My app needs access to a user's full Dropbox. Only supported via the Core API**.

    -   Provide an app name.

    -   Create **Create app**.

    -   Copy **App key** and **App secret**.

-   Create a copy of `default.json` and name it `config.json`.

-   Put **App key** and **App secret** to `CONSUMER_KEY` and `CONSUMER_SECRET` respectively.

-   Start `get-access-token` and follow the instructions.


Serving
-------

After `config.json` is filled with consumer key, consumer secret, and access tokens, start:

```bash
$ wsgidav
```

An HTTP server starts and listens to `http://localhost:8080` (configurable from `wsgidav.conf`).
