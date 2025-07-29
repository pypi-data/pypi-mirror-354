# mashup

> generate a chaotic character sequence so cursed even regex will flinch.

**mashup** is a terminal-friendly, argument-powered, clipboard-integrated nonsense generator for passwords, tokens, and bad decisions.

---
## Features

- Mix character sets: `--lower`, `--upper`, `--digits`, `--symbols`, etc.
- Combine flags like `-ludsp`
- Use custom charsets like `--custom 'abc123!?🐍'`
- Automatically copies to clipboard (unless you hate joy)
---

## Installation
```
pip install mashup
```
---
## Usage
`mashup [flags] [length]`

### Flags:
  `-l`  `--lower`        –  Use lowercase letters (a–z)
  
  `-u`  `--upper`        –  Use uppercase letters (A–Z)
  
  `-d`  `--digits`       –  Use digits (0–9)
  
  `-x`  `--hexdigits`    –  Use hexadecimal digits (0–9, A–F)
  
  `-s`  `--symbols`      –  Use safe symbols (!@#$%^&*()-_=+[]{})
  
  `-p`  `--punctuation`  –  Use full ASCII punctuation (~, \, etc.)
  
  `-c`  `--custom <str>` –  Use your own charset (like 'abc123!?🔥🦄')
  
  `-n`  `--do-not-copy`  –  Don't copy the result to clipboard
