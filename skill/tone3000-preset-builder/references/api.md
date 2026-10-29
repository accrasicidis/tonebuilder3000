# TONE3000 API and login

TONE3000 has an official REST API and OAuth 2.0 service at `https://www.tone3000.com/api/v1`. Full docs: [tone3000.com/api](https://www.tone3000.com/api).

## Authentication

Every call needs a Bearer token:

```text
Authorization: Bearer <token>
```

There are two ways to get one.

### 1. OAuth 2.0 with PKCE (recommended)

Use this for interactive work.

- Authorize: `GET https://www.tone3000.com/api/v1/oauth/authorize`
- Token: `POST https://www.tone3000.com/api/v1/oauth/token`

Steps:

1. Make a PKCE `code_verifier` (a random URL safe string). Derive `code_challenge` as `base64url(sha256(code_verifier))`.
2. Make a random `state` to guard against CSRF.
3. Send the user to:

   ```text
   https://www.tone3000.com/api/v1/oauth/authorize?client_id=<YOUR_PUBLISHABLE_KEY>&redirect_uri=<REDIRECT_URI>&response_type=code&code_challenge=<CHALLENGE>&code_challenge_method=S256&state=<STATE>
   ```

4. Handle the redirect at `redirect_uri` (`GET /callback?code=...&state=...`) and check `state`.
5. Swap the code for tokens:

   ```http
   POST /api/v1/oauth/token
   Content-Type: application/x-www-form-urlencoded

   grant_type=authorization_code&code=<code>&code_verifier=<verifier>&redirect_uri=<uri>&client_id=<client_id>
   ```

   The response looks like this:

   ```json
   {
     "access_token": "...",
     "refresh_token": "...",
     "expires_in": 3600,
     "token_type": "bearer"
   }
   ```

6. When the access token expires, refresh it:

   ```http
   POST /api/v1/oauth/token
   Content-Type: application/x-www-form-urlencoded

   grant_type=refresh_token&refresh_token=<refresh_token>&client_id=<client_id>
   ```

The script does all of this for you:

```bash
python scripts/t3k.py login
```

It starts a local callback server at `http://localhost:8080/callback`, opens your browser, finishes the exchange and saves the tokens in your OS config folder. Tokens refresh on their own. Add `http://localhost:8080/callback` as a redirect URI in your TONE3000 settings first.

Token file locations:

- Windows: `%APPDATA%\TONE3000\auth.json`
- Linux: `~/.config/TONE3000/auth.json`
- macOS: `~/Library/Application Support/TONE3000/auth.json`

### 2. Secret key (headless or automation)

Create a key under [Settings, API Keys](https://www.tone3000.com/settings). Pass the secret key (`t3k_cs_...`) or an access token in an environment variable:

```bash
export T3K_SECRET_KEY=t3k_cs_...     # macOS and Linux
set T3K_SECRET_KEY=t3k_cs_...        # Windows
```

Keep keys out of command history, chat and repo files.

---

## Endpoints the builder uses

### Current user

`GET /api/v1/user` returns the logged in user (`id`, `username`, `display_name`, `avatar_url`, `is_verified`).

### Search tones

`GET /api/v1/tones/search`

Query parameters:

- `query`: the search term, for example `jcm800`
- `gears`: gear filter. One of `amp`, `amp-cab`, `pedal`, `cab`, `outboard`, `space`, `experimental`. Join several with an underscore, for example `amp_amp-cab`.
- `page`: page number, starting at 1
- `page_size`: results per page (max 25)
- `sort`: `trending`, `best-match`, `newest`, `oldest` or `downloads-all-time`
- `architecture`: `1`, `2` or `custom`. The builder uses `2` (modern NAM A2 models).
- `format`: `nam` or `ir`

Returns `PaginatedResponse<Tone[]>`:

```json
{
  "data": [
    {
      "id": 87735,
      "title": "Marshall Jcm800 + V30 1960",
      "gear": "amp-cab",
      "format": "nam",
      "downloads_count": 23771,
      "favorites_count": 346,
      "user": {
        "id": 123,
        "username": "flaviospanker",
        "display_name": "Flavio",
        "avatar_url": "..."
      },
      "makes": [{"id": 1, "name": "Marshall JCM800"}],
      "tags": [{"id": 2, "name": "british crunch"}]
    }
  ],
  "page": 1,
  "page_size": 10,
  "total": 45,
  "total_pages": 5
}
```

### Get a tone

`GET /api/v1/tones/{id}?architecture=2` returns the full tone, including the creator (`user`), `makes`, `tags`, `gear`, `format` and `description`.

### List models for a tone

`GET /api/v1/models?tone_id={id}&page_size=100&architecture=2` returns `PaginatedResponse<Model[]>`:

```json
{
  "data": [
    {
      "id": 741409,
      "tone_id": 87735,
      "name": "Jcm800",
      "model_url": "https://www.tone3000.com/api/v1/models/741409/download/...",
      "size": "standard",
      "architecture_version": "2"
    }
  ]
}
```

---

## What the plugin needs for each block

A `.t3kpreset` holds a JUCE ValueTree with one `ChainBlock` node per gear item. Each block carries a `toneJson` string that describes the tone.

- It must have a `models[]` array with `id`, `name` and `model_url` from the official API.
- `activeModelId` on the `ChainBlock` must match one of the model IDs in `models[]`.
- When TONE3000 loads the preset, `ProcessorHistory.cpp::queueActiveModelLoad` downloads `model_url`. It uses the user's active TONE3000 session to authenticate.
