const { readSession, json, SLOTS } = require("./_lib");

module.exports = async (req, res) => {
  const s = readSession(req);
  if (!s) return json(res, 401, { error: "Nu ești autentificat" });
  json(res, 200, { user: s.user, role: s.role, can: s.can, slots: s.can.includes("photos") ? SLOTS : [] });
};
