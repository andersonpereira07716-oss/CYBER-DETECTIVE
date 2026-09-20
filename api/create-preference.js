// api/create-preference.js
// Rota: POST /api/create-preference
// O app chama isso quando o usuário aperta "Abrir checkout".

import { MercadoPagoConfig, Preference } from "mercadopago";
import { kv } from "@vercel/kv";
import { randomUUID } from "crypto";

const client = new MercadoPagoConfig({ accessToken: process.env.MP_ACCESS_TOKEN });

export default async function handler(req, res) {
  if (req.method !== "POST") return res.status(405).end();

  try {
    const preference = new Preference(client);
    const externalReference = randomUUID();
    const siteUrl = `https://${req.headers.host}`;

    const result = await preference.create({
      body: {
        items: [
          {
            title: "Cyber-Detective PRO",
            quantity: 1,
            unit_price: Number(process.env.PRO_PRICE || 9.9),
            currency_id: "BRL",
          },
        ],
        external_reference: externalReference,
        back_urls: {
          success: `${siteUrl}/`,
          failure: `${siteUrl}/`,
          pending: `${siteUrl}/`,
        },
        auto_return: "approved",
        notification_url: `${siteUrl}/api/webhook`,
      },
    });

    await kv.set(`payment:${externalReference}`, { status: "pending", code: null });

    res.json({
      checkout_url: result.init_point,
      external_reference: externalReference,
    });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: "Falha ao criar cobrança" });
  }
}