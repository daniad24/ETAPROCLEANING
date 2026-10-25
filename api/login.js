const { users, checkPassword, makeToken, setCookie, json, mustPost, TTL } = require("./_lib");

module.exports = async (req, res) => {
  if (!mustPost(req, res)) return;
  const { user, password } = req.body || {};
  const found = users().find((u) => u.user === String(user || "").toLowerCase().trim());
  // aceeași muncă și același răspuns indiferent dacă utilizatorul există, ca să nu se poată ghici numele
  const ok = checkPassword(password, found ? found.hash : "00:00");
  if (!found || !ok) {
    await new Promise((r) => setTimeout(r, 800));
    return json(res, 401, { error: "Utilizator sau parolă greșită" });
  }
  setCookie(res, makeToken(found), TTL);
  json(res, 200, { ok: true });
};
