# DSH CTF fast loop

An optional DeepSeek Harness bundle for this CTF workspace. It adds a compact Pwn workflow prompt and rejects unbounded local probe/replay calls before they start.

The plugin activates only when the session working directory contains `.dsh/skills/ctf-solve/SKILL.md`. It recognizes directly invoked Python and shell scripts in `pwsh` calls, including relative names such as `python probe2.py`:

- `solve*`, `exploit*`, and `test_local*`: 30 seconds
- Other Python or shell scripts: 45 seconds

The `pwsh` call must pass `timeoutMs` explicitly and stay within its limit. A missing or excessive value is rejected before the script starts; an accepted value is passed to the shell executor as its process timeout. Inline interpreter commands are not matched. Explicit remote commands are excluded. If a run times out, simplify or split it instead of repeating the same case without new evidence.

## Install

From the CyberScience workspace, install the bundle into the active DSH profile:

```powershell
dsh plugin --profile desktop add ./.dsh/plugins/dsh-ctf-fast-loop
```

The profile update is persistent. Remove it with:

```powershell
dsh plugin --profile desktop remove dsh-ctf-fast-loop
```

