// Funcții comune pentru /api (login, sesiune, drepturi, scriere în GitHub). Fără dependențe.
const crypto = require("crypto");
const SLOTS = require("./_slots.json");

const COOKIE = "eta_admin";
const TTL = 12 * 3600; // sesiunea ține 12 ore

// Ce poate face fiecare rol. Daniel = owner (tot), Horia = editor (poze + prețuri).
const ROLES = {
  owner: ["photos", "prices", "content", "users"],
  editor: ["photos", "prices"],
};

function users() {
  try { return JSON.parse(process.env.ADMIN_USERS || "[]"); } catch { return []; }
}

function secret() {
  const s = process.env.SESSION_SECRET || "";
  if (s.length < 32) throw new Error("SESSION_SECRET lipsește sau e prea scurt (min. 32 caractere)");
  return s;
}

const b64u = (b) => Buffer.from(b).toString("base64url");
const sign = (data) => crypto.createHmac("sha256", secret()).update(data).digest("base64url");

function safeEq(a, b) {
  const x = Buffer.from(String(a)), y = Buffer.from(String(b));
  return x.length === y.length && crypto.timingSafeEqual(x, y);
}

// hash în formatul "salt:hash" (hex), produs de tools/hash-password.js
function checkPassword(password, stored) {
  const [salt, hash] = String(stored || "").split(":");
  if (!salt || !hash) return false;
  const test = crypto.scryptSync(String(password), Buffer.from(salt, "hex"), 64).toString("hex");
  return safeEq(test, hash);
}

function makeToken(user) {
  const payload = b64u(JSON.stringify({ u: user.user, e: Math.floor(Date.now() / 1000) + TTL }));
  return `${payload}.${sign(payload)}`;
}

function readSession(req) {
  const m = /(?:^|;\s*)eta_admin=([^;]+)/.exec(req.headers.cookie || "");
  if (!m) return null;
  const [payload, sig] = m[1].split(".");
  if (!payload || !sig || !safeEq(sig, sign(payload))) return null;
  let data;
  try { data = JSON.parse(Buffer.from(payload, "base64url").toString()); } catch { return null; }
  if (!data.e || data.e < Date.now() / 1000) return null;
  // rolul se ia mereu din configurarea curentă: dacă contul e scos sau schimbat, se aplică imediat
  const user = users().find((u) => u.user === data.u);
  if (!user || !ROLES[user.role]) return null;
  return { user: user.user, role: user.role, can: ROLES[user.role] };
}

function setCookie(res, value, maxAge) {
  res.setHeader("Set-Cookie", `${COOKIE}=${value}; Path=/; HttpOnly; Secure; SameSite=Strict; Max-Age=${maxAge}`);
}

function json(res, status, body) {
  res.statusCode = status;
  res.setHeader("Content-Type", "application/json; charset=utf-8");
  res.setHeader("Cache-Control", "no-store");
  res.end(JSON.stringify(body));
}

// cerere de modificare: doar POST, doar JSON (un alt site nu poate trimite așa fără permisiunea browserului)
function mustPost(req, res) {
  if (req.method !== "POST") { json(res, 405, { error: "Metodă nepermisă" }); return false; }
  if (!String(req.headers["content-type"] || "").includes("application/json")) { json(res, 415, { error: "Cerere invalidă" }); return false; }
  return true;
}

function requireCan(req, res, perm) {
  const s = readSession(req);
  if (!s) { json(res, 401, { error: "Nu ești autentificat" }); return null; }
  if (!s.can.includes(perm)) { json(res, 403, { error: "Nu ai dreptul la această acțiune" }); return null; }
  return s;
}

const REPO = () => process.env.GITHUB_REPO || "daniad24/ETAPROCLEANING";
const BRANCH = () => process.env.GITHUB_BRANCH || "main";

async function gh(path, opts = {}) {
  if (!process.env.GITHUB_TOKEN) throw new Error("GITHUB_TOKEN lipsește");
  return fetch(`https://api.github.com/repos/${REPO()}/${path}`, {
    ...opts,
    headers: {
      Authorization: `Bearer ${process.env.GITHUB_TOKEN}`,
      Accept: "application/vnd.github+json",
      "X-GitHub-Api-Version": "2022-11-28",
      "User-Agent": "etapro-admin",
      ...(opts.headers || {}),
    },
  });
}

// Scrie un fișier în repo (commit nou pe branch). Autorul commit-ului e proprietarul tokenului (contul tău GitHub).
async function putFile(repoPath, contentBuffer, message) {
  const url = `contents/${repoPath.split("/").map(encodeURIComponent).join("/")}`;
  let sha;
  const cur = await gh(`${url}?ref=${encodeURIComponent(BRANCH())}`);
  if (cur.ok) sha = (await cur.json()).sha;
  else if (cur.status !== 404) throw new Error(`GitHub a răspuns ${cur.status}`);
  const r = await gh(url, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message, content: contentBuffer.toString("base64"), branch: BRANCH(), ...(sha ? { sha } : {}) }),
  });
  if (!r.ok) throw new Error(`GitHub a refuzat scrierea (${r.status})`);
}

module.exports = { SLOTS, ROLES, users, checkPassword, makeToken, readSession, setCookie, json, mustPost, requireCan, putFile, TTL };
