# Overworld

`Overworld` is an archived Python script that was created to automate the old Overworld whitelist application flow.

The project was built to reduce repetitive manual work when preparing accounts for the Overworld whitelist campaign. Instead of opening the website, connecting a wallet, authorizing Twitter, completing a tweet task, and submitting the questionnaire by hand, the script attempted to perform those steps programmatically for a prepared account.

> Important: this project was used a long time ago and is no longer expected to work. It depends on old Overworld API endpoints, the previous whitelist website flow, Twitter OAuth behavior, hardcoded request formats, and external services that may have changed or disappeared since then.

## How It Works

The main logic is located in `Main.py`.

The script defines an `Overworld` class that performs the old whitelist flow in several steps:

1. Initializes a TLS client session with a random desktop Chrome user agent.
2. Configures HTTP and HTTPS proxy usage for the session.
3. Links an EVM wallet to the Overworld applicant profile.
4. Signs the applicant UUID with the wallet private key.
5. Connects a Twitter account through Twitter OAuth using an `auth_token` cookie.
6. Completes the tweet task through the Overworld API.
7. Submits answers to the Overworld questionnaire.

The execution flow at the bottom of `Main.py` runs these methods in order:

```python
print(overworld.LinkWallet())
time.sleep(4)
print(overworld.LinkTwitter())
time.sleep(4)
print(overworld.TweetTask())
time.sleep(4)
print(overworld.AnswerQuestions())
```

Each method prints or returns an HTTP status code so the operator could see whether that step completed successfully.

## Project Structure

```text
Overworld/
└── Main.py
```

The project is intentionally minimal and contains all logic in a single file.

## Main Components

### `LinkWallet`

Creates an applicant profile through the old Overworld API, receives an applicant `uuid`, signs that UUID with the provided EVM private key, and submits the signature back to the API.

### `LinkTwitter`

Uses the provided Twitter `auth_token` cookie to open Twitter, retrieve the `ct0` CSRF token, start the Overworld Twitter connection flow, approve the OAuth request, and follow the redirect back to Overworld.

### `TweetTask`

Calls the old Overworld tweet task endpoint for the current applicant UUID.

### `AnswerQuestions`

Submits a hardcoded questionnaire payload to the old Overworld questionnaire endpoint.

The questionnaire answers and email are currently written directly inside the method and were not loaded from a separate input file.

## Required Data

For the original historical run, the script required:

- Python 3.10 or a compatible version.
- An EVM wallet address.
- The private key for that wallet.
- A Twitter `auth_token` cookie for the account being linked.
- An HTTP proxy.

The constructor accepts these values in this order:

```python
Overworld(
    address,
    private_key,
    twitter_auth_token,
    proxy
)
```

The proxy is passed directly to `tls_client` and was expected to be in a format supported by the HTTP client, for example:

```text
login:password@ip:port
```

In the current `Main.py`, the values are placeholders or old sample data and should not be treated as active credentials.

## Dependencies

The project does not include a `requirements.txt` file. The dependencies were installed manually:

```bash
pip install tls-client ua-generator web3 eth-account
```

## Running

From the project root:

```bash
python Main.py
```

Before running historically, the account data in the `Overworld(...)` constructor had to be replaced with real values:

```python
overworld = Overworld(
    "wallet-address",
    "private-key",
    "twitter-auth-token",
    "proxy"
)
```

The questionnaire answers were also hardcoded in `AnswerQuestions`, so changing the submitted responses required editing `Main.py` directly.

## Why It No Longer Works

This repository should be treated as an archive of an old automation script, not as a working production tool. It is very likely broken now because:

- The old whitelist site `https://whitelist.overworld.games` may no longer expose the same flow.
- The Overworld API endpoint `https://owapi.ovrwrld.net` may have changed or been disabled.
- Twitter OAuth and internal API behavior have changed significantly over time.
- The script relies on Twitter cookies and CSRF handling that may no longer match the current platform.
- The questionnaire payload and task endpoints were campaign-specific.
- The old whitelist campaign is no longer relevant.
- Anti-bot protection, request validation, and session requirements may have changed.

The README documents what the script used to do and how it was structured, but it should not be considered a current launch guide for an active automation workflow.

## Security Notes

The script works with sensitive data: wallet private keys, Twitter authentication tokens, and proxies. These values must never be committed to a public repository or shared with third parties.

If the project is kept only for archival purposes, replace real credentials with placeholders and avoid storing active tokens or private keys in `Main.py`.
