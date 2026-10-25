// Cere parolele lui Daniel și Horia și pune în clipboard valoarea completă pentru ADMIN_USERS (Vercel).
// Parolele nu se afișează și nu se salvează nicăieri; în clipboard ajung doar hash-urile.
//   node tools/make-admin-users.js
const crypto = require("crypto");
const { spawnSync } = require("child_process");

const stdin = process.stdin;

function ask(label) {
  return new Promise((resolve) => {
    process.stdout.write(label);
    if (stdin.setRawMode) stdin.setRawMode(true);
    stdin.resume();
    stdin.setEncoding("utf8");
    let pw = "";
    const onData = (chunk) => {
      for (const ch of chunk) {
        if (ch === "\r" || ch === "\n" || ch === "\u0004") {
          stdin.removeListener("data", onData);
          if (stdin.setRawMode) stdin.setRawMode(false);
          stdin.pause();
          process.stdout.write("\n");
          return resolve(pw);
        } else if (ch === "\u0003") process.exit(1);
        else if (ch === "\u007f" || ch === "\b") pw = pw.slice(0, -1);
        else pw += ch;
      }
    };
    stdin.on("data", onData);
  });
}

function hash(pw) {
  const salt = crypto.randomBytes(16);
  return salt.toString("hex") + ":" + crypto.scryptSync(pw, salt, 64).toString("hex");
}

(async () => {
  const out = [];
  for (const [user, role, name] of [["daniel", "owner", "Daniel"], ["horia", "editor", "Horia"]]) {
    const a = await ask(`Parola pentru ${name} (min. 10 caractere, nu se vede): `);
    if (a.length < 10) { console.error("Prea scurtă. Ia-o de la capăt."); process.exit(1); }
    const b = await ask(`Repetă parola pentru ${name}: `);
    if (a !== b) { console.error("Parolele nu se potrivesc. Ia-o de la capăt."); process.exit(1); }
    out.push({ user, role, hash: hash(a) });
  }
  const value = JSON.stringify(out);
  const r = spawnSync("clip", { input: value, shell: true });
  if (r.status !== 0) { console.error("Nu am putut copia în clipboard."); process.exit(1); }
  console.log("Gata. Valoarea pentru ADMIN_USERS e în clipboard: lipește-o în Vercel cu Ctrl+V.");
})();
