// Face hash-ul unei parole pentru ADMIN_USERS (Vercel). Rulezi local; parola nu se afișează și nu se salvează.
//   node tools/hash-password.js
const crypto = require("crypto");

process.stdout.write("Parola (nu se vede ce scrii): ");
const stdin = process.stdin;
if (stdin.setRawMode) stdin.setRawMode(true);
stdin.resume();
stdin.setEncoding("utf8");
let pw = "";
stdin.on("data", (chunk) => {
  for (const ch of chunk) {
    if (ch === "\r" || ch === "\n" || ch === "\u0004") {
      if (stdin.setRawMode) stdin.setRawMode(false);
      stdin.pause();
      process.stdout.write("\n");
      if (pw.length < 10) { console.error("Parola trebuie să aibă cel puțin 10 caractere."); process.exit(1); }
      const salt = crypto.randomBytes(16);
      console.log(salt.toString("hex") + ":" + crypto.scryptSync(pw, salt, 64).toString("hex"));
      process.exit(0);
    } else if (ch === "\u0003") process.exit(1);
    else if (ch === "\u007f" || ch === "\b") pw = pw.slice(0, -1);
    else pw += ch;
  }
});
