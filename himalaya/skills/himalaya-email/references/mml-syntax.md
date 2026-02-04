# MML (MIME Meta Language) Syntax Reference

MML is the template body language used by himalaya for composing rich emails. It is based on the Emacs MML specification and ported to Rust by the Pimalaya project. MML allows adding multiple parts, attachments, inline images, and PGP encryption/signing within a template body.

MML tags use an XML-like syntax with `<#tag>` opening and `<#/tag>` closing.

## Plain Text (Default)

Any text in the template body that is not wrapped in MML tags is treated as a plain text part:

```
From: alice@example.com
To: bob@example.com
Subject: Simple message

This is a plain text email body.
No MML tags needed for simple text.
```

## HTML Parts

Wrap HTML content in a `<#part>` tag with `type=text/html`:

```
From: alice@example.com
To: bob@example.com
Subject: HTML email

<#part type=text/html>
<h1>Hello</h1>
<p>This is an <strong>HTML</strong> email.</p>
<#/part>
```

## Multipart Messages

Use `<#multipart>` to combine plain text and HTML alternatives:

```
From: alice@example.com
To: bob@example.com
Subject: Multipart message

This is the plain text version.

<#multipart type=alternative>
<#part type=text/html>
<h1>Hello</h1>
<p>This is the HTML version.</p>
<#/part>
<#/multipart>
```

The `type=alternative` attribute tells mail clients to pick the best version to display.

## File Attachments

Attach a file using the `filename` attribute on `<#part>`:

```
From: alice@example.com
To: bob@example.com
Subject: Report attached

Please find the report attached.

<#part filename=/path/to/report.pdf><#/part>
```

### Custom Attachment Name

Override the displayed filename with the `name` attribute:

```
<#part filename=/path/to/report-v3-final-FINAL.pdf name=report.pdf><#/part>
```

### Multiple Attachments

Add multiple `<#part>` tags:

```
From: alice@example.com
To: bob@example.com
Subject: Documents

Here are the requested documents.

<#part filename=/path/to/report.pdf><#/part>
<#part filename=/path/to/spreadsheet.xlsx><#/part>
<#part filename=/path/to/presentation.pptx><#/part>
```

### Attachment with Description

Add a description for the attachment:

```
<#part filename=/path/to/image.png description="Project screenshot"><#/part>
```

## Inline Images

Use `disposition=inline` to embed an image in the email body:

```
From: alice@example.com
To: bob@example.com
Subject: Screenshot

Here is the screenshot:

<#part disposition=inline filename=/path/to/screenshot.png><#/part>
```

> **Limitation (himalaya 1.1.0):** The `id` attribute on `<#part>` is not supported by himalaya's MML parser — using it causes "cannot parse MML body" errors. This means `cid:` image references (`<img src="cid:...">`) cannot work. For images in HTML emails (e.g., signature logos), use a remote URL instead: `<img src="https://example.com/logo.png">`. Simple inline disposition (above) works for attaching images as standalone parts.

## PGP Encryption

Encrypt the message body using PGP/MIME:

```
From: alice@example.com
To: bob@example.com
Subject: Confidential

<#part encrypt=pgpmime>
This content will be encrypted.
<#/part>
```

Requires PGP to be configured in himalaya's config (GPG bindings, shell commands, or native implementation).

## PGP Signing

Sign the message body using PGP/MIME:

```
From: alice@example.com
To: bob@example.com
Subject: Signed message

<#part sign=pgpmime>
This content will be digitally signed.
<#/part>
```

## Combined Encrypt and Sign

Encrypt and sign can be combined in nested parts or separate sections:

```
From: alice@example.com
To: bob@example.com
Subject: Encrypted and signed

<#part sign=pgpmime>
<#part encrypt=pgpmime>
This content is both encrypted and signed.
<#/part>
<#/part>
```

## Complete Example: Rich Email with Attachment

```
From: alice@example.com
To: bob@example.com
Cc: team@example.com
Subject: Q1 Report

Hi Bob,

Please find the Q1 report attached. Here's a summary:

- Revenue up 15%
- New customers: 230
- Churn rate: 2.1%

Let me know if you have questions.

Best,
Alice

<#part filename=/home/alice/reports/q1-2025.pdf name=Q1-Report.pdf><#/part>
```

## Complete Example: HTML Email with Inline Image

> **Note:** This pattern may fail with "cannot parse MML body" in himalaya 1.1.0. See the Inline Images section above for details. If it fails, remove the `<#part disposition=inline>` and the `<img src="cid:...">` reference.

```
From: alice@example.com
To: bob@example.com
Subject: Design preview

<#multipart type=alternative>
<#part type=text/html>
<h2>Design Preview</h2>
<p>Here's the latest mockup:</p>
<img src="cid:mockup">
<#/part>
<#/multipart>

<#part disposition=inline filename=/home/alice/designs/mockup.png><#/part>
```

## MML Tag Reference

| Tag | Attributes | Purpose |
|-----|-----------|---------|
| `<#part>...<#/part>` | `type`, `filename`, `name`, `disposition`, `description`, `encrypt`, `sign` | Define a MIME part |
| `<#multipart>...<#/multipart>` | `type` (alternative, mixed, related) | Group multiple parts |

### Part Attributes

| Attribute | Values | Purpose |
|-----------|--------|---------|
| `type` | MIME type (e.g., `text/html`, `text/plain`) | Content type of the part |
| `filename` | File path | Attach a file from disk |
| `name` | String | Override displayed filename |
| `disposition` | `inline`, `attachment` | How the part is presented (default: attachment) |
| `id` | String | Content-ID for `cid:` references in HTML (unreliable in 1.1.0) |
| `description` | String | Description metadata for the part |
| `encrypt` | `pgpmime` | Encrypt the part content |
| `sign` | `pgpmime` | Sign the part content |

### Multipart Types

| Type | Purpose |
|------|---------|
| `alternative` | Multiple representations of the same content (e.g., plain + HTML) |
| `mixed` | Independent parts (e.g., text + attachments) |
| `related` | Parts that reference each other (e.g., HTML + inline images) |

## Sending a Template with MML via Pipe

Construct the full template (headers + MML body) and pipe it to `template send`:

```bash
himalaya template send <<'EOF'
From: alice@example.com
To: bob@example.com
Subject: Report

Please see the Q1 report attached.

<#part filename=/home/alice/reports/q1.pdf><#/part>
EOF
```

Or save as a draft instead:

```bash
himalaya template save -f "Drafts" <<'EOF'
From: alice@example.com
To: bob@example.com
Subject: Report

Please see the Q1 report attached.

<#part filename=/home/alice/reports/q1.pdf><#/part>
EOF
```

The template system compiles MML to proper MIME before sending, so the recipient sees standard email with attachments.
