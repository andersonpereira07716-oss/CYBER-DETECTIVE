// api/check-payment.js
// Rota: GET /api/check-payment?ref=xxxx

import { kv } from "@vercel/kv";

export default async function handler(req, res) {
  if (req.method !== "GET") return res.status(405).end();

  const { ref } = req.query;
  if (!ref) return res.status(400).json({ status: "missing_ref" });

  const entry = await kv.get(`payment:${ref}`);
  if (!entry) return res.status(404).json({ status: "not_found" });

  res.json(entry);
}