// api/webhook.js
// Rota: POST /api/webhook
// O Mercado Pago chama isso sozinho quando o pagamento muda de status.

import { MercadoPagoConfig, Payment } from "mercadopago";
import { kv } from "@vercel/kv";
import { randomBytes } from "crypto";

const client = new MercadoPagoConfig({ accessToken: process.env.MP_ACCESS_TOKEN });

function generateCode() {
  const part = () => randomBytes(2).toString("hex").toUpperCase();
  return `CYBER-${part()}-${part()}`;
}

export default async function handler(req, res) {
  try {
    const paymentId = req.query["data.id"] || req.body?.data?.id;
    if (!paymentId) return res.status(200).end();

    const payment = new Payment(client);
    const info = await payment.get({ id: paymentId });

    if (info.status === "approved") {
      const externalReference = info.external_reference;
      const entry = await kv.get(`payment:${externalReference}`);

      if (entry && !entry.code) {
        const code = generateCode();
        await kv.set(`payment:${externalReference}`, { status: "approved", code });
        await kv.set(`code:${code}`, { used: false, externalReference });
        console.log(`Pagamento aprovado. Código gerado: ${code}`);
      }
    }

    res.status(200).end();
  } catch (err) {
    console.error(err);
    res.status(200).end();
  }
}