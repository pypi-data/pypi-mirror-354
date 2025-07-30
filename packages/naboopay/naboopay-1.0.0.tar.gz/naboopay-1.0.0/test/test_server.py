# import os
from fastapi import FastAPI, HTTPException, Request

from naboopay import Webhook

app = FastAPI()

# NABOOPAY_WEBHOOK_SECRET = os.getenv("NABOOPAY_WEBHOOK_SECRET")
NABOOPAY_WEBHOOK_SECRET = "begueeeeeeee"

@app.post("/webhook")
async def handle_webhook(request: Request):
    payload = await request.json()
    signature = request.headers.get('X-Signature')
    naboopay_webhook = Webhook(webhook_secret_key=NABOOPAY_WEBHOOK_SECRET)
    payment = naboopay_webhook.verify(payload, signature)
    if payment is None:
        raise HTTPException(status_code=400, detail="Invalid signature")
    print(payment.order_id)
    print(payment.amount)
    print(payment.transaction_status)
    print(payment.created_at)
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )

