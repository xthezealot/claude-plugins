# Himalaya Configuration Reference

Himalaya uses a TOML configuration file at `~/.config/himalaya/config.toml`. Run `himalaya` with no config to launch the interactive setup wizard, or create the file manually.

Multiple config files can be merged using `-c path1.toml -c path2.toml` (useful for separating public config from private credentials).

## Minimal Configuration

```toml
[accounts.default]
default = true
email = "user@example.com"
display-name = "User Name"

folder.aliases.inbox = "INBOX"
folder.aliases.sent = "Sent"
folder.aliases.drafts = "Drafts"
folder.aliases.trash = "Trash"

backend.type = "imap"
backend.host = "imap.example.com"
backend.port = 993
backend.encryption = "tls"
backend.auth.type = "password"
backend.auth.command = "cat ~/.email-password"

message.send.backend.type = "smtp"
message.send.backend.host = "smtp.example.com"
message.send.backend.port = 465
message.send.backend.encryption = "tls"
message.send.backend.auth.type = "password"
message.send.backend.command = "cat ~/.email-password"
```

## Global Settings

These apply as defaults across all accounts:

```toml
# Default display name
display-name = "Full Name"

# Signature (inline string or file path)
signature = "Best regards,\nAlice"
# OR
signature = "/home/alice/.signature"

# Signature delimiter (default: "-- \n")
signature-delim = "-- \n"

# Downloads directory for attachments
downloads-dir = "/home/alice/Downloads"
```

## Account Settings

Each account is a TOML table under `[accounts.<name>]`:

```toml
[accounts.personal]
default = true
email = "alice@gmail.com"
display-name = "Alice Smith"
signature = "Cheers,\nAlice"
downloads-dir = "/home/alice/mail-downloads"

[accounts.work]
email = "alice@company.com"
display-name = "Alice Smith"
signature = "/home/alice/.work-signature"
```

## Folder Aliases

Map logical folder names to actual mailbox names (varies by provider):

```toml
[accounts.default.folder.aliases]
inbox = "INBOX"
sent = "Sent"          # Gmail: "[Gmail]/Sent Mail"
drafts = "Drafts"      # Gmail: "[Gmail]/Drafts"
trash = "Trash"         # Gmail: "[Gmail]/Trash"
# Custom aliases
archive = "Archive"
```

## Folder Display

```toml
[accounts.default.folder.list]
page-size = 10

[accounts.default.folder.list.table]
preset = "default"
```

## Envelope Display

```toml
[accounts.default.envelope.list]
page-size = 20
datetime-fmt = "%Y-%m-%d %H:%M"      # strftime format
datetime-local-tz = true               # convert to local timezone

[accounts.default.envelope.list.table]
preset = "default"
```

## Message Settings

### Reading

```toml
[accounts.default.message.read]
headers = ["From", "To", "Cc", "Subject", "Date"]
format = "auto"    # "auto", "flowed", or "fixed"
```

### Writing

```toml
[accounts.default.message.write]
headers = ["From", "To", "Cc", "Bcc", "Subject"]
```

### Sending

```toml
[accounts.default.message.send]
save-copy = true                       # save to Sent folder
# pre-hook = "markdown-to-html"        # optional pre-send processing
```

### Deleting

```toml
[accounts.default.message.delete]
style = "folder"     # "folder" (move to trash) or "flag" (add deleted flag)
```

## Template Settings

### Signature Placement

```toml
[accounts.default.template]
# For new messages
[accounts.default.template.new]
signature-style = "inlined"    # "hidden", "attached", or "inlined"

# For replies
[accounts.default.template.reply]
posting-style = "top"          # "top", "bottom", or "interleaved"
signature-style = "inlined"

# For forwards
[accounts.default.template.forward]
posting-style = "top"
signature-style = "hidden"
```

## Backend Configuration

### IMAP

```toml
[accounts.default.backend]
type = "imap"
host = "imap.example.com"
port = 993
encryption = "tls"           # "tls", "start-tls", or "none"

# Password auth (command outputs password to stdout)
[accounts.default.backend.auth]
type = "password"
command = "pass email/imap"

# OR OAuth2
[accounts.default.backend.auth]
type = "oauth2"
client-id = "your-client-id"
auth-url = "https://accounts.google.com/o/oauth2/v2/auth"
token-url = "https://oauth2.googleapis.com/token"
pkce = true
scopes = ["https://mail.google.com/"]
```

### Maildir

```toml
[accounts.default.backend]
type = "maildir"
root-dir = "/home/alice/Maildir"
```

### Notmuch

```toml
[accounts.default.backend]
type = "notmuch"
db-path = "/home/alice/.mail"
```

### SMTP (Sending)

```toml
[accounts.default.message.send.backend]
type = "smtp"
host = "smtp.example.com"
port = 465
encryption = "tls"

[accounts.default.message.send.backend.auth]
type = "password"
command = "pass email/smtp"
```

### Sendmail (Sending)

```toml
[accounts.default.message.send.backend]
type = "sendmail"
command = "/usr/sbin/sendmail"
```

## Password Storage on macOS

The Homebrew build of himalaya does not include `+keyring`, so the TOML `keyring = "..."` auth option is unavailable. Use the macOS Keychain via the `security` command instead.

### Storing a password

```bash
# Add (first time)
security add-generic-password -s himalaya-imap -a user@example.com -w

# Update (if entry already exists)
security add-generic-password -U -s himalaya-imap -a user@example.com -w
```

Both forms prompt for the password interactively. Use a distinct `-s` service name per backend (e.g., `himalaya-imap`, `himalaya-smtp`).

### Using it in himalaya config

Point `auth.command` at `security find-generic-password -w`:

```toml
# IMAP
[accounts.default.backend.auth]
type = "password"
command = "security find-generic-password -s himalaya-imap -a user@example.com -w"

# SMTP
[accounts.default.message.send.backend.auth]
type = "password"
command = "security find-generic-password -s himalaya-smtp -a user@example.com -w"
```

## PGP / Encryption

### GPG Shell Commands

```toml
[accounts.default.pgp]
type = "commands"
encrypt-cmd = "gpg --encrypt --armor --recipient <recipient>"
decrypt-cmd = "gpg --decrypt"
sign-cmd = "gpg --sign --armor"
verify-cmd = "gpg --verify"
```

### GPG Bindings

```toml
[accounts.default.pgp]
type = "gpg"
```

### Native Rust PGP

```toml
[accounts.default.pgp]
type = "native"
secret-key.path = "/home/alice/.pgp/secret.key"
secret-key.passphrase.command = "pass pgp/passphrase"
wkd = true                          # Web Key Discovery
key-servers = ["hkps://keys.openpgp.org"]
```

## Provider-Specific Examples

### Gmail (App Password)

```toml
[accounts.gmail]
default = true
email = "user@gmail.com"
display-name = "User Name"

folder.aliases.inbox = "INBOX"
folder.aliases.sent = "[Gmail]/Sent Mail"
folder.aliases.drafts = "[Gmail]/Drafts"
folder.aliases.trash = "[Gmail]/Trash"

backend.type = "imap"
backend.host = "imap.gmail.com"
backend.port = 993
backend.encryption = "tls"
backend.auth.type = "password"
backend.auth.command = "pass google/app-password"

message.send.backend.type = "smtp"
message.send.backend.host = "smtp.gmail.com"
message.send.backend.port = 465
message.send.backend.encryption = "tls"
message.send.backend.auth.type = "password"
message.send.backend.auth.command = "pass google/app-password"
```

### Gmail (OAuth2)

```toml
[accounts.gmail]
default = true
email = "user@gmail.com"

backend.type = "imap"
backend.host = "imap.gmail.com"
backend.port = 993
backend.encryption = "tls"
backend.auth.type = "oauth2"
backend.auth.client-id = "your-client-id.apps.googleusercontent.com"
backend.auth.client-secret.keyring = "himalaya-gmail-client-secret"
backend.auth.auth-url = "https://accounts.google.com/o/oauth2/v2/auth"
backend.auth.token-url = "https://oauth2.googleapis.com/token"
backend.auth.pkce = true
backend.auth.scopes = ["https://mail.google.com/"]

message.send.backend.type = "smtp"
message.send.backend.host = "smtp.gmail.com"
message.send.backend.port = 465
message.send.backend.encryption = "tls"
message.send.backend.auth.type = "oauth2"
message.send.backend.auth.client-id = "your-client-id.apps.googleusercontent.com"
message.send.backend.auth.client-secret.keyring = "himalaya-gmail-client-secret"
message.send.backend.auth.auth-url = "https://accounts.google.com/o/oauth2/v2/auth"
message.send.backend.auth.token-url = "https://oauth2.googleapis.com/token"
message.send.backend.auth.pkce = true
message.send.backend.auth.scopes = ["https://mail.google.com/"]
```

### Outlook / Office 365

```toml
[accounts.outlook]
email = "user@outlook.com"

backend.type = "imap"
backend.host = "outlook.office365.com"
backend.port = 993
backend.encryption = "tls"
backend.auth.type = "oauth2"
backend.auth.client-id = "your-azure-client-id"
backend.auth.auth-url = "https://login.microsoftonline.com/common/oauth2/v2.0/authorize"
backend.auth.token-url = "https://login.microsoftonline.com/common/oauth2/v2.0/token"
backend.auth.pkce = true
backend.auth.scopes = ["https://outlook.office365.com/.default"]

message.send.backend.type = "smtp"
message.send.backend.host = "smtp.office365.com"
message.send.backend.port = 587
message.send.backend.encryption = "start-tls"
message.send.backend.auth.type = "oauth2"
message.send.backend.auth.client-id = "your-azure-client-id"
message.send.backend.auth.auth-url = "https://login.microsoftonline.com/common/oauth2/v2.0/authorize"
message.send.backend.auth.token-url = "https://login.microsoftonline.com/common/oauth2/v2.0/token"
message.send.backend.auth.pkce = true
message.send.backend.auth.scopes = ["https://outlook.office365.com/.default"]
```

### ProtonMail (via Bridge)

```toml
[accounts.proton]
email = "user@protonmail.com"

backend.type = "imap"
backend.host = "127.0.0.1"
backend.port = 1143
backend.encryption = "start-tls"
backend.auth.type = "password"
backend.auth.command = "pass proton/bridge-password"

message.send.backend.type = "smtp"
message.send.backend.host = "127.0.0.1"
message.send.backend.port = 1025
message.send.backend.encryption = "start-tls"
message.send.backend.auth.type = "password"
message.send.backend.auth.command = "pass proton/bridge-password"
```

### iCloud Mail

```toml
[accounts.icloud]
email = "user@icloud.com"

backend.type = "imap"
backend.host = "imap.mail.me.com"
backend.port = 993
backend.encryption = "tls"
backend.auth.type = "password"
backend.auth.command = "pass icloud/app-password"

message.send.backend.type = "smtp"
message.send.backend.host = "smtp.mail.me.com"
message.send.backend.port = 587
message.send.backend.encryption = "start-tls"
message.send.backend.auth.type = "password"
message.send.backend.auth.command = "pass icloud/app-password"
```

## Email Aliases

Himalaya has no built-in alias feature. To send from an alias persistently, configure a separate account that shares the same backend credentials but uses a different `email` field:

```toml
# Primary account
[accounts.personal]
default = true
email = "alice@example.com"
display-name = "Alice Smith"

backend.type = "imap"
backend.host = "imap.example.com"
backend.port = 993
backend.encryption = "tls"
backend.auth.type = "password"
backend.auth.command = "security find-generic-password -s himalaya-imap -a alice@example.com -w"

message.send.backend.type = "smtp"
message.send.backend.host = "smtp.example.com"
message.send.backend.port = 465
message.send.backend.encryption = "tls"
message.send.backend.auth.type = "password"
message.send.backend.auth.command = "security find-generic-password -s himalaya-smtp -a alice@example.com -w"

# Alias account — same server/credentials, different From address
[accounts.alias]
email = "team@example.com"
display-name = "Alice Smith (Team)"

backend.type = "imap"
backend.host = "imap.example.com"
backend.port = 993
backend.encryption = "tls"
backend.auth.type = "password"
backend.auth.command = "security find-generic-password -s himalaya-imap -a alice@example.com -w"

message.send.backend.type = "smtp"
message.send.backend.host = "smtp.example.com"
message.send.backend.port = 465
message.send.backend.encryption = "tls"
message.send.backend.auth.type = "password"
message.send.backend.auth.command = "security find-generic-password -s himalaya-smtp -a alice@example.com -w"
```

Send from the alias with `-a`:

```bash
himalaya template send -a alias <<'EOF'
From: team@example.com
To: recipient@example.com
Subject: Hello from the team

Body here.
EOF
```

For one-off alias usage without a separate account, override the `From:` header directly in the template. The SMTP server must allow sending from that address.

## Diagnostics

Check account health:

```bash
himalaya account doctor              # diagnose default account
himalaya account doctor work         # diagnose named account
himalaya account doctor work --fix   # attempt automatic fixes (e.g., keyring repair)
```

## Environment Variables

| Variable | Purpose |
|----------|---------|
| `HIMALAYA_CONFIG` | Override default config file path |
| `EDITOR` | Editor for interactive message commands |
| `RUST_LOG` | Log level (debug, trace) |
| `RUST_BACKTRACE` | Enable backtraces (1) |
