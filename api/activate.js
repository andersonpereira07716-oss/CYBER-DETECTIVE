// api/activate.js
// Rota: POST /api/activate  body: { code: "CYBER-XXXX-XXXX" }

import { kv } from "@vercel/kv";

export default async function handler(req, res) {
  if (req.method !== "POST") return res.status(405).end();

  const { code } = req.body || {};
  if (!code) return res.status(400).json({ valid: false, error: "Código não informado" });

  const entry = await kv.get(`code:${code}`);
  if (!entry) return res.json({ valid: false, error: "Código inválido" });
  if (entry.used) return res.json({ valid: false, error: "Código já foi usado" });

  entry.used = true;
  await kv.set(`code:${code}`, entry);

  res.json({ valid: true });
}