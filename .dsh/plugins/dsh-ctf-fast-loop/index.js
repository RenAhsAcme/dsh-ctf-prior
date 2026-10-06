import { existsSync } from 'node:fs'
import { join } from 'node:path'

export const name = 'dsh-ctf-fast-loop'
export const inject = ['systemPrompt', 'tools']

const FULL_RUN_MS = 30_000
const PROBE_MS = 45_000

const FAST_LOOP_GUIDANCE = [
  'For local CTF Pwn work, combine ELF mitigations, symbols, relevant disassembly, and useful strings into one reconnaissance pass.',
  'Keep one reusable probe harness. State the hypothesis and the observation that would distinguish it before each experiment; vary one factor at a time.',
  'Every local Python or shell script call through pwsh must set timeoutMs explicitly: 30 seconds for solve/exploit/test_local scripts and 45 seconds for other scripts. A missing or larger timeout is rejected before execution.',
  'Report case identifiers and a clear success signal; stop at the first passing payload. Do not create a new dbgN script for each small variation or repeat the same case without a changed hypothesis.',
  'Promote the exact locally passing payload into the solver before testing fallbacks. A timeout or guard rejection is inconclusive; simplify or split the run before trying again.',
  'After one local end-to-end success, run only the final concise confirmation before any authorized remote check.',
].join(' ')

function isCtfWorkspace(agent) {
  const cwd = agent?.session?.header?.cwd
  return typeof cwd === 'string'
    && existsSync(join(cwd, '.dsh', 'skills', 'ctf-solve', 'SKILL.md'))
}

function unquote(token) {
  return token.replace(/^["'`]/, '').replace(/["'`]$/, '')
}

function scriptInvocations(command) {
  const tokens = command.match(/"[^"]*"|'[^']*'|`[^`]*`|[^\s;&|]+/g) ?? []
  const scripts = []

  for (let i = 0; i < tokens.length; i += 1) {
    const executable = unquote(tokens[i]).replaceAll('\\', '/').toLowerCase().split('/').at(-1)
    if (!/^(?:python(?:\d+(?:\.\d+)*)?|py|bash|sh)(?:\.exe)?$/.test(executable)) continue

    for (let j = i + 1; j < tokens.length && j <= i + 5; j += 1) {
      const argument = unquote(tokens[j]).replaceAll('\\', '/').toLowerCase()
      if (argument === '-c' || argument === '-m') break
      if (argument === '-x' || argument === '-w') {
        j += 1
        continue
      }
      if (argument.startsWith('-')) continue
      if (/\.(?:py|sh)$/.test(argument)) scripts.push(argument.split('/').at(-1))
      break
    }
  }

  return scripts
}

function localCtfRun(exec) {
  if (exec.name !== 'pwsh' || !isCtfWorkspace(exec.agent)) return undefined

  const command = exec.arguments?.command
  if (typeof command !== 'string') return undefined

  const normalized = command.replaceAll('\\', '/').toLowerCase()
  if (/--remote\b|(?:^|[;&|]\s*)(?:ssh|nc|ncat|netcat|curl|wget)\b/.test(normalized)) return undefined

  const scripts = scriptInvocations(command)
  if (scripts.length === 0) return undefined

  const fullRun = scripts.some((script) => /^(?:solve|exploit|test_local)(?:[-_.][a-z0-9_.-]+)?\.(?:py|sh)$/.test(script))
  return fullRun
    ? { timeoutMs: FULL_RUN_MS, label: 'full local exploit replay' }
    : { timeoutMs: PROBE_MS, label: 'local script run' }
}

function timeoutDenial(run, supplied) {
  const requested = Number.isFinite(supplied) ? `${supplied}ms` : 'no explicit timeout'
  return {
    kind: 'deny',
    reason: `CTF fast-loop guard: this ${run.label} was not run because it requested ${requested}. Set timeoutMs to at most ${run.timeoutMs}ms. If it times out, simplify or split the experiment; do not rerun the same payload without new evidence.`,
  }
}

export function apply(ctx) {
  ctx.systemPrompt.section({
    name: 'ctf:pwn-fast-loop',
    order: 150,
    text: ({ agent }) => isCtfWorkspace(agent) ? FAST_LOOP_GUIDANCE : '',
  })

  ctx.on('tools/pre-execute', (exec, next) => {
    const run = localCtfRun(exec)
    if (!run) return next()

    const supplied = exec.arguments?.timeoutMs
    if (!Number.isFinite(supplied) || supplied <= 0 || supplied > run.timeoutMs) {
      return timeoutDenial(run, supplied)
    }

    return next()
  })
}
