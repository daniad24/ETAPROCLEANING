const { setCookie, json, mustPost } = require("./_lib");

module.exports = async (req, res) => {
  if (!mustPost(req, res)) return;
  setCookie(res, "", 0);
  json(res, 200, { ok: true });
};
