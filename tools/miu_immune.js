// miu_immune.js — Sistema Inmune MIU v1.0
// Inspired by Cerberus (Adirdabush1/cerberus) + Claude-Red (SnailSploit)
// DOI: 10.5281/zenodo.20547558

const SIGNALS = {
  POLICY: ['ignore previous', 'disregard', 'override instructions', 'forget context', 'new role', 'act as', 'pretend you are'],
  INJECTION: ['system prompt', 'jailbreak', 'DAN mode', 'developer mode', 'ignore all rules', 'bypass filter'],
  BEHAVIORAL: ['repeat 100 times', 'infinite loop', 'send all secrets', 'exfiltrate', 'rm -rf'],
  CONTENT: ['<script>', 'javascript:', 'data:text/html', 'eval(', 'document.cookie']
};

function scoreEvent(event) {
  const text = JSON.stringify(event).toLowerCase();
  let score = 0;
  const triggered = [];

  for (const [signal, patterns] of Object.entries(SIGNALS)) {
    for (const p of patterns) {
      if (text.includes(p.toLowerCase())) {
        score += signal === 'INJECTION' ? 35 : signal === 'POLICY' ? 30 : signal === 'BEHAVIORAL' ? 25 : 15;
        triggered.push({ signal, pattern: p });
      }
    }
  }

  score = Math.min(100, score);
  const action = score >= 70 ? 'BLOCK' : score >= 40 ? 'AUDIT' : 'ALLOW';
  return { score, action, triggered, safe: action === 'ALLOW' };
}

module.exports = { scoreEvent, SIGNALS };
