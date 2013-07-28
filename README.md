Google+ API Playpen
===================

Mucking around and experimenting with Google+ APIs and OAuth.

There are two apps in the plus folder:

* *web_app.py*: a web app that uses the user OAuth authentication to interact with Google+ APIs. This has been shamelessly hacked together from the sample quick-start app at [Google's online API docs](https://developers.google.com/+/quickstart/python)

* *console_app.py*: a command-line app that uses an API key to hit the APIs; no user-specific functionality here

Settings Files
--------------

The standard Google API client secrets file should be in the root folder and called ```client_secrets.json```:

```json
{ "web":
  { "client_id": "YOUR_CLIENT_ID",
    "client_secret": "YOUR_CLIENT_SECRET",
    "redirect_uris": [ "postmessage"],
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://accounts.google.com/o/oauth2/token"
  }
}
```

Both apps also need a ```settings.json``` file to provide either Flask secret key or the Google API key:

```json
{ "flask":
  { "secret_key": "YOUR SECRET KEY" },
  "google":
  { "api_key": "APP API KEY" }
}
```