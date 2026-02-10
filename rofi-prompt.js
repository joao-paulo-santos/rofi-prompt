#!/usr/bin/env node
const { spawn, spawnSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const ROFI_RETV = process.env.ROFI_RETV || '0';
const ROFI_INFO = process.env.ROFI_INFO || '';
const INPUT = process.argv.slice(2).join(' ').trim();

const stdoutWrite = (s) => { try { fs.writeSync(1, s); } catch (_) {} };

const AGENTS = {
  opencode: {
    command: 'opencode run',
    label: 'OpenCode'
  },
  claude: {
    command: 'claude -p',
    label: 'Claude Code'
  }
};

const DEFAULT_AGENT = process.env.PROMPT_AGENT || 'opencode';

if (!AGENTS[DEFAULT_AGENT]) {
  console.error(`Unknown agent: ${DEFAULT_AGENT}. Available agents: ${Object.keys(AGENTS).join(', ')}`);
  process.exit(1);
}

const agent = AGENTS[DEFAULT_AGENT];

function printRow(label, info) {
  stdoutWrite(label + '\x00info\x1f' + info + '\n');
}

// when rofi asks for list
if (ROFI_RETV === '0') {
  printRow(`Run ${agent.label} prompt`, 'RUN');
  process.exit(0);
}

if (ROFI_RETV === '1') {
  process.exit(0);
}

if (ROFI_RETV === '2') {
  if (!INPUT) process.exit(0);
  
  const SCRIPT_DIR = path.dirname(__filename);
  const OUTFILE = '/tmp/rofi_prompt_result.txt';
  const SCRIPT_FILE = '/tmp/rofi_prompt_runner.sh';
  const RESULT_SCRIPT = path.join(SCRIPT_DIR, 'show_prompt_result.py');
  
  const runnerScript = `#!/bin/sh
${agent.command} '${INPUT.replace(/'/g, "'\\''")}' > '${OUTFILE}' 2>&1 || echo "ERROR: failed" >> '${OUTFILE}'
python3 '${RESULT_SCRIPT}' '${OUTFILE}' 2>/dev/null &
`;
  
  try {
    fs.writeFileSync(SCRIPT_FILE, runnerScript, 'utf8');
    fs.chmodSync(SCRIPT_FILE, 0o755);
    const p = spawn(SCRIPT_FILE, [], { detached: true, stdio: 'ignore' });
    p.unref();
  } catch (e) { /* ignore */ }
  
  process.exit(0);
}
