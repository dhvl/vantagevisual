# Hosting the Inquiry Form Backend

To make your inquiry form live, you need to host the backend logic (`send_inquiry.py`) on a server or serverless platform.

## Option 1: Vercel (Recommended for Static Sites)
Since you are using GitHub, Vercel is the easiest option.
1.  Create an `api/` directory in your root.
2.  Move `send_inquiry.py` into `api/send-inquiry.py`.
3.  Modify it to be a Vercel Serverless Function (using the `Handler` pattern).
4.  Set your `RESEND_API_KEY` and `CONTACT_EMAIL` in Vercel Environment Variables.

## Option 2: Supabase Edge Functions
If you prefer Supabase:
1.  Use the Supabase CLI to create a new function: `supabase functions new send-inquiry`.
2.  Copy the logic from `send_inquiry.py` into the TypeScript function (Deno).
3.  Deploy: `supabase functions deploy send-inquiry`.
4.  Update the `fetch()` URL in your HTML to point to your Supabase function URL.

## Option 3: Local Testing
To test the form locally:
1.  Install dependencies: `pip install flask flask-cors resend python-dotenv`.
2.  Run the handler: `python execution/app.py`.
3.  In your HTML, update the fetch URL to `http://localhost:5000/api/send-inquiry`.
4.  Open `vantage-visual-website.html` in your browser and submit.

## Resend Note
By default, Resend uses `onboarding@resend.dev`. To send from your own domain (e.g., `info@vantagevisual.co.uk`), you must verify your domain in the Resend Dashboard.
