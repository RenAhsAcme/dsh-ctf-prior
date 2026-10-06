# DSH CTF fast loop

An optional DeepSeek Harness bundle for this CTF workspace. It adds bounded experiment guidance across CTF categories and rejects Python, Node, PowerShell, shell, and common network-command calls without an explicit short timeout.

The plugin activates only when the session working directory contains `.dsh/skills/ctf-solve/SKILL.md`. It recognizes Python, Node, PowerShell, Bash, and shell scripts in `pwsh` calls, including relative paths and inline interpreter commands. It also limits common direct network commands and .NET HTTP client invocations:

- `solve*`, `exploit*`, and `test_local*`: 30 seconds
- Other scripts and network probes: 20 seconds

The `pwsh` call must pass `timeoutMs` explicitly and stay within its limit. A missing or excessive value is rejected before execution. These limits bound the foreground wait; a long-running command may be moved to a background job rather than terminated. Collect or stop that job before starting another remote experiment. The prompt also asks the solver to use one in-flight remote job, small sequential probes, and a request budget tied to a stated hypothesis. Those network-count and concurrency limits are guidance, not hard enforcement by this plugin.

An aborted call, missing output, or truncated output is `PARTIAL/UNKNOWN`, not proof that no request or side effect occurred. Establish the process and request status before retrying.

The prompt also requires an exact endpoint, operation, account or file, and request count before state-changing probes. Approval for one account or submission does not extend to per-candidate account creation or repeated submissions; this is guidance, not a runtime request counter.

The default probe budget is at most 12 distinct HTTP requests per batch. The plugin does not count requests or active jobs; this budget, per-request timeouts, retry limits, and concurrency guidance depend on the model following the injected prompt.

Treat transport errors and sentinel statuses such as `-1` as inconclusive. Define a positive hit predicate before a probe; require the expected HTTP status and a response signature that distinguishes the target behavior from a WAF, fallback page, or ordinary error. A response body merely differing from one deny string is not a hit, and a `403` alone does not prove that a route or directory exists; compare status, length, body signature, and relevant headers with known baselines.

For containers with an expiry, record the remaining lease before deliberate waits and leave time for a final verification and result handoff.

## Install

From the CyberScience workspace, install the bundle into the active DSH profile:

```powershell
dsh plugin --profile desktop add ./.dsh/plugins/dsh-ctf-fast-loop
```

The profile update is persistent. Remove it with:

```powershell
dsh plugin --profile desktop remove dsh-ctf-fast-loop
```

