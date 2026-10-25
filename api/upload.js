const { requireCan, json, mustPost, putFile, SLOTS } = require("./_lib");

const MAX_BYTES = 3 * 1024 * 1024; // limita Vercel pentru cerere e ~4,5 MB; panoul micșorează pozele înainte

const isJpeg = (b) => b[0] === 0xff && b[1] === 0xd8 && b[2] === 0xff;
const isPng = (b) => b.length > 8 && b.readUInt32BE(0) === 0x89504e47;

module.exports = async (req, res) => {
  if (!mustPost(req, res)) return;
  const s = requireCan(req, res, "photos");
  if (!s) return;
  const { file, data } = req.body || {};
  const slot = SLOTS.find((x) => x.file === file); // doar pozele din listă pot fi schimbate
  if (!slot || typeof data !== "string") return json(res, 400, { error: "Poză necunoscută" });
  const buf = Buffer.from(data, "base64");
  if (!buf.length || buf.length > MAX_BYTES) return json(res, 413, { error: "Poza e prea mare (max. 3 MB)" });
  const png = file.endsWith(".png");
  if (png ? !isPng(buf) : !isJpeg(buf)) return json(res, 400, { error: `Fișierul trebuie să fie ${png ? "PNG" : "JPG"}` });
  try {
    await putFile(`site/assets/img/${file}`, buf, `Poză schimbată din admin: ${slot.group}, ${slot.label} (${s.user})`);
  } catch (e) {
    return json(res, 502, { error: "Nu am putut salva poza. Încearcă din nou." });
  }
  json(res, 200, { ok: true });
};
