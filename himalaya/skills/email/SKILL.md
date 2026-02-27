---
name: email
description: >-
  Manage email through the himalaya CLI: list, search, read, compose, reply,
  forward, and send messages; work with drafts, attachments, flags, and folders;
  multi-account support with MML template syntax for rich content and PGP.
  Use when user mentions email, inbox, or mail.
---

# Email Management with Himalaya

Himalaya is a CLI email client that supports IMAP, Maildir, Notmuch, SMTP, and Sendmail backends. All email operations go through the `himalaya` binary. Configuration lives at `~/.config/himalaya/config.toml`.

## Non-Interactive Usage (Required)

Several himalaya commands (`message write`, `message reply`, `message forward`, `message edit`) open `$EDITOR` and are **interactive**. Since Claude operates non-interactively, use the **template system** instead for composing email:

- `himalaya template write` -- generate a blank compose template (stdout)
- `himalaya template reply` -- generate a reply template (stdout)
- `himalaya template forward` -- generate a forward template (stdout)
- `himalaya template send` -- send a template (stdin)
- `himalaya template save` -- save a template to a folder as draft (stdin)

The workflow: generate a template, modify it, then pipe it to `template send` or `template save`.

## Always Use JSON Output

For all read operations, append `-o json` to get structured, parseable output:

```bash
himalaya envelope list -o json
himalaya message read <ID> -o json
himalaya folder list -o json
himalaya account list -o json
```

## Core Workflows

### Listing and Searching Emails

List recent envelopes (message previews with ID, flags, subject, sender, date):

```bash
himalaya envelope list # INBOX, default page
himalaya envelope list -f "Sent" # different folder
himalaya envelope list -s 20 # 20 per page
himalaya envelope list -p 2 -s 10 # page 2, 10 per page
```

Search with the query language (pass query terms as trailing arguments):

```bash
himalaya envelope list from john
himalaya envelope list subject "project update"
himalaya envelope list after 2025-01-15
himalaya envelope list before 2025-02-01
himalaya envelope list from alice and subject meeting
himalaya envelope list body "quarterly report" and after 2025-01-01
himalaya envelope list not flag seen # unread only
himalaya envelope list flag flagged # starred/flagged
```

Sort results:

```bash
himalaya envelope list order by date desc
himalaya envelope list order by subject asc
himalaya envelope list from john order by date desc
```

View envelopes as threads:

```bash
himalaya envelope thread # all threads in INBOX
himalaya envelope thread -i <ID> # thread containing specific message
himalaya envelope thread from alice # threads matching query
```

### Reading Messages

```bash
himalaya message read <ID> # read message, marks as seen
himalaya message read <ID> --preview # read without marking seen
himalaya message read <ID> --no-headers # body only
himalaya message read <ID> -H From -H Subject # specific headers only
himalaya message read <ID1> <ID2> # read multiple
himalaya message read <ID> -f "Sent" # from specific folder
```

Read an entire thread:

```bash
himalaya message thread <ID> # full thread for envelope
himalaya message thread <ID> --preview # without marking seen
```

### Composing and Sending Email

**Step 1**: Generate a template:

```bash
# New message
himalaya template write -H "To:recipient@example.com" -H "Subject:Hello"

# Reply
himalaya template reply <ID> # reply to sender
himalaya template reply <ID> --all # reply all

# Forward
himalaya template forward <ID>
```

> **Important: Replying to emails**
>
> When replying, you MUST use `himalaya template reply <ID>` to generate the template first. This command:
> - Adds `In-Reply-To` and `References` headers (required for email threading)
> - Includes the quoted original message
> - Pre-fills `To:`, `Cc:`, and `Subject:` correctly
>
> **Never compose a reply from scratch** — it will appear as a new conversation in the recipient's mail client.

**Complete reply workflow:**

```bash
# 1. Generate the reply template (outputs to stdout)
himalaya template reply 95 --account work

# 2. Capture output, shows something like:
# From: you@example.com
# To: sender@example.com
# In-Reply-To: <original-message-id@example.com>
# References: <original-message-id@example.com>
# Subject: Re: Original subject
#
# > Quoted original message here
# > Line 2 of original...

# 3. Compose your reply (keep headers, add body above the quoted text), then send:
himalaya template send --account work <<'EOF'
From: you@example.com
To: sender@example.com
In-Reply-To: <original-message-id@example.com>
References: <original-message-id@example.com>
Subject: Re: Original subject

Your reply text here.

> Quoted original message here
> Line 2 of original...
EOF
```

For HTML replies with signatures, wrap the body in MML multipart syntax (see "Multipart HTML with Signature" below) while preserving all headers from the generated template.

**Step 2**: Modify the template output as needed. A template looks like:

```
From: you@example.com
To: recipient@example.com
Subject: Hello

Body text here
```

**Step 3**: Send or save as draft using a heredoc:

```bash
# Send directly
himalaya template send <<'EOF'
From: you@example.com
To: recipient@example.com
Subject: Hello

Body text here.
EOF

# Save as draft
himalaya template save -f "Drafts" <<'EOF'
From: you@example.com
To: recipient@example.com
Subject: Hello

Draft body here.
EOF
```

A successful `template send` produces no output on stdout. Check stderr for errors.

For details on MML syntax (attachments, HTML parts, encryption), read **`references/mml-syntax.md`**.

### Multipart HTML with Signature

To send a professional email with both plain text and HTML (e.g., with an HTML signature), use `<#multipart type=alternative>`. The plain text comes first (before any `<#part>` tag), then the HTML part:

```bash
himalaya template send <<'EOF'
From: you@example.com
To: recipient@example.com
Subject: Meeting follow-up

<#multipart type=alternative>
Hi Bob,

Thanks for the meeting today. I'll send the notes by Friday.

Best,
Alice

--
Alice Smith
alice@example.com | example.com
<#part type=text/html>
<html><body style="font-family: -apple-system, Arial, sans-serif; font-size: 14px; color: #333;">
<p>Hi Bob,</p>
<p>Thanks for the meeting today. I'll send the notes by Friday.</p>
<p>Best,<br/>Alice</p>
<br/>
<!-- HTML signature goes here, inside the HTML part -->
<table cellpadding="0" cellspacing="0" style="font-size: 13px;">
  <tr>
    <td style="border-left: 2px solid #2563eb; padding-left: 12px;">
      <strong>Alice Smith</strong><br/>
      <a href="mailto:alice@example.com">alice@example.com</a> | example.com
    </td>
  </tr>
</table>
</body></html>
<#/part>
<#/multipart>
EOF
```

Key points:
- Plain text fallback uses `--` separator before the signature (name, email, URL)
- HTML signature lives **inside** the `<#part type=text/html>` block, after the body, separated by `<br/>`
- Do **not** wrap with `<#multipart type=related>` for inline images — see Known Limitations

### Sending from an Alias

Himalaya has no built-in alias feature. To send from an alias address, override the `From:` header. This works if the SMTP server allows sending from that address (most providers do for configured aliases).

When generating a template:

```bash
himalaya template write -H "From:alias@example.com" -H "To:recipient@example.com" -H "Subject:Hello"
```

Or set it directly in a heredoc:

```bash
himalaya template send <<'EOF'
From: alias@example.com
To: recipient@example.com
Subject: Hello

Body here.
EOF
```

For a persistent alias setup using separate accounts, see **`references/configuration.md`**.

### Working with Drafts

Save a draft:

```bash
himalaya template save -f "Drafts" <<'EOF'
From: you@example.com
To: recipient@example.com
Subject: WIP

Draft body here.
EOF
```

List drafts:

```bash
himalaya envelope list -f "Drafts"
```

Edit and send a draft (read it, modify, send, then delete the draft):

```bash
# 1. Read the draft content
himalaya message read <DRAFT_ID> -f "Drafts"
# 2. Modify as needed, then send via heredoc
himalaya template send <<'EOF'
<modified template content>
EOF
# 3. Remove the draft
himalaya message delete <DRAFT_ID> -f "Drafts"
```

### Attachments

Download all attachments from a message:

```bash
himalaya attachment download <ID> # downloads to configured dir
himalaya attachment download <ID> -f "Sent" # from specific folder
himalaya attachment download <ID1> <ID2> # from multiple messages
```

To send attachments, use MML syntax in the template body. See **`references/mml-syntax.md`**.

### Flags

Standard flags: `seen`, `answered`, `flagged`, `deleted`, `draft`. Custom flags are also supported.

```bash
himalaya flag add <ID> seen # mark as read
himalaya flag add <ID> flagged # star/flag
himalaya flag add <ID1> <ID2> seen # multiple messages
himalaya flag remove <ID> seen # mark as unread
himalaya flag set <ID> seen flagged # replace all flags
himalaya flag add <ID> seen -f "Sent" # in specific folder
```

### Folder Management

```bash
himalaya folder list # list all folders
himalaya folder add "Projects/Q1" # create folder
himalaya folder expunge "Trash" # permanently delete flagged-deleted
himalaya folder purge "Trash" -y # empty entire folder
himalaya folder delete "Old-Archive" -y # delete folder and contents
```

### Moving and Copying Messages

```bash
himalaya message move "Archive" <ID> # move to Archive
himalaya message move "Archive" <ID> -f "Sent" # from Sent to Archive
himalaya message copy "Backup" <ID> # copy to Backup
himalaya message move "Trash" <ID1> <ID2> # move multiple
```

### Deleting Messages

```bash
himalaya message delete <ID> # moves to Trash (or flags deleted)
himalaya message delete <ID1> <ID2> # delete multiple
himalaya message delete <ID> -f "Drafts" # delete from specific folder
```

Note: `message delete` does not permanently delete. It moves to Trash or adds the `deleted` flag. To permanently remove, use `folder expunge` after deleting.

### Exporting Messages

```bash
himalaya message export <ID> --full -d ./ # export as .eml file
himalaya message export <ID> -d ./exports/ # export MIME parts to directory
himalaya message export <ID> --full --open # export and open
```

### Multi-Account Usage

All commands accept `-a <ACCOUNT>` to target a specific account:

```bash
himalaya envelope list -a work
himalaya message read <ID> -a personal
himalaya template send -a work < message.txt
himalaya account list # show all configured accounts
himalaya account doctor # diagnose default account
himalaya account doctor work # diagnose specific account
```

**Important**: Always run `himalaya account list` first to discover available account names. Don't guess — account names are defined in `~/.config/himalaya/config.toml` and may not match the email address.

If there is only **one** account configured (common with providers like Zoho that support multiple aliases), skip `-a` entirely and just set the `From:` header in the template to the desired sender address. The SMTP server will send from that address if it's a configured alias.

## Envelope Query Language Reference

### Filter Operators

| Operator | Syntax | Example |
|----------|--------|---------|
| And | `<cond> and <cond>` | `from john and subject meeting` |
| Or | `<cond> or <cond>` | `from alice or from bob` |
| Not | `not <cond>` | `not flag seen` |

### Filter Conditions

| Condition | Syntax | Example |
|-----------|--------|---------|
| Date | `date <yyyy-mm-dd>` | `date 2025-01-15` |
| Before | `before <yyyy-mm-dd>` | `before 2025-02-01` |
| After | `after <yyyy-mm-dd>` | `after 2025-01-01` |
| From | `from <pattern>` | `from alice` |
| To | `to <pattern>` | `to team@company.com` |
| Subject | `subject <pattern>` | `subject "weekly sync"` |
| Body | `body <pattern>` | `body "action items"` |
| Flag | `flag <flag>` | `flag seen`, `flag flagged` |

### Sort Options

Append `order by` after any filter (or alone):

```
order by date desc # newest first
order by date asc # oldest first
order by from asc # alphabetical by sender
order by subject desc # reverse alphabetical by subject
order by date desc subject asc # multi-sort: date then subject
```

## Troubleshooting

If himalaya commands fail or return connection errors, diagnose with:

```bash
himalaya account doctor -o json
himalaya account doctor <ACCOUNT> --fix # attempt automatic repair
```

If himalaya is not installed, see the [himalaya repo](https://github.com/pimalaya/himalaya) for installation. For account configuration, see **`references/configuration.md`**.

## Known Limitations (himalaya 1.1.0)

- **Inline image attachments fail**: Using `<#multipart type=related>` with `<#part disposition=inline filename=... id=...>` to embed images via `cid:` references causes "cannot parse MML body" errors. Workaround: use `<img src="https://...">` with a hosted image URL in the HTML instead of `cid:` references. Alternatively, omit the image entirely — the surrounding HTML will still render correctly.
- **`id` attribute not supported**: The `id` attribute on `<#part>` (used to set Content-ID for `cid:` references) is not parsed by himalaya's MML parser. Do not use `cid:` image references; use remote URLs instead.
- **No `himalaya draft` command**: Draft management uses the template system: `himalaya template save -f "Drafts"` to save, `himalaya message read` / `himalaya message delete` to read/clean up drafts.

## Additional Resources

### Reference Files

For detailed information, consult:
- **`references/mml-syntax.md`** -- MML template syntax for attachments, HTML, multipart, PGP encryption/signing
- **`references/configuration.md`** -- himalaya TOML configuration, account setup, backend options, provider examples
