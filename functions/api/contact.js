import { EmailMessage } from "cloudflare:email";

const json = (data, status = 200) => new Response(JSON.stringify(data), {
  status,
  headers: {
    "content-type": "application/json; charset=utf-8",
    "cache-control": "no-store"
  }
});

const clean = (value, maxLength) => String(value || "")
  .replace(/[\u0000-\u0008\u000B\u000C\u000E-\u001F\u007F]/g, "")
  .trim()
  .slice(0, maxLength);

const escapeHeader = (value) => value.replace(/[\r\n]+/g, " ");

export async function onRequestPost({ request, env }) {
  try {
    const contentType = request.headers.get("content-type") || "";
    if (!contentType.includes("multipart/form-data") && !contentType.includes("application/x-www-form-urlencoded")) {
      return json({ error: "Unsupported form submission." }, 415);
    }

    const form = await request.formData();
    const honeypot = clean(form.get("company"), 200);
    if (honeypot) return json({ ok: true });

    const name = clean(form.get("name"), 120);
    const email = clean(form.get("email"), 254);
    const subject = clean(form.get("subject"), 120);
    const message = clean(form.get("message"), 5000);

    if (!name || !email || !subject || !message) {
      return json({ error: "Please complete every required field." }, 400);
    }

    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      return json({ error: "Please enter a valid email address." }, 400);
    }

    if (!env.SEND_EMAIL || !env.CONTACT_EMAIL || !env.CONTACT_FROM) {
      console.error("Contact form email bindings are not configured.");
      return json({ error: "The contact form is temporarily unavailable." }, 503);
    }

    const safeName = escapeHeader(name);
    const safeEmail = escapeHeader(email);
    const safeSubject = escapeHeader(subject);
    const boundary = `vectisverse-${crypto.randomUUID()}`;
    const raw = [
      `From: VectisVerse Website <${env.CONTACT_FROM}>`,
      `To: ${env.CONTACT_EMAIL}`,
      `Reply-To: ${safeName} <${safeEmail}>`,
      `Subject: Website enquiry: ${safeSubject}`,
      "MIME-Version: 1.0",
      `Content-Type: multipart/alternative; boundary=\"${boundary}\"`,
      "",
      `--${boundary}`,
      "Content-Type: text/plain; charset=UTF-8",
      "Content-Transfer-Encoding: 8bit",
      "",
      `Name: ${name}`,
      `Email: ${email}`,
      `Subject: ${subject}`,
      "",
      message,
      "",
      `--${boundary}--`
    ].join("\r\n");

    const emailMessage = new EmailMessage(env.CONTACT_FROM, env.CONTACT_EMAIL, raw);
    await env.SEND_EMAIL.send(emailMessage);

    return json({ ok: true });
  } catch (error) {
    console.error("Contact form error", error);
    return json({ error: "Message could not be sent. Please try again." }, 500);
  }
}

export function onRequestGet() {
  return json({ error: "Method not allowed." }, 405);
}
