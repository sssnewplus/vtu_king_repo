from .apis import OpayAPI
import time
from .models import User


# financial services
# api call func to create wallet
def create_wallet(user_id, name, phone_number, email):
    try:
        payload = {
            "userId": user_id,
            "name": name,
            "phoneNumber": phone_number,
            "email": email,
        }
        response = OpayAPI.post("/wallet/create", payload)
        if response["status"] == "success":
            return {"success": True, "wallet_id": response["data"]["walletId"]}
        return {"success": False, "message": response["message"]}
    except Exception as e:
        return {"success": False, "message": str(e)}

# api call func to create wallet with retries of 5
def create_wallet_with_retries(user):
    attempts = 0
    while attempts < 4:
        response = create_wallet(user.id, user.name, user.phone_number, user.email)
        if response["success"]:
            return response
        else:
            attempts += 1
            time.sleep(2 ** attempts)
            ''' -> attempt 1: Wait 2 seconds, attempt 2: Wait 4 seconds, attempt 3: Wait 8 seconds and so on '''

# api call func to transfer to other wallet
def transfer_to_wallet(sender_wallet_id, reciever_wallet_id, amount):
    try:
        payload = {"sender_wallet_id": sender_wallet_id,
                   "recipient_wallet_id": reciever_wallet_id,
                   "amount": amount}
        response = OpayAPI.post("/wallet/transfer", payload)
        if response["status"] == "success":
            return {"success": True, "balance": response["data"]["balance"]}
        return {"success": False, "message": response["message"]}
    except Exception as e:
        return {"success": False, "message": str(e)}

# api call func to transfer selling price amount to granny wallet
def transfer_to_granny(sender_wallet_id, amount):
    granny_user = User.query.filter_by(username='sssnew').first()
    recipient_wallet_id = granny_user.wallet_id
    try:
        payload = { "sender_wallet_id": sender_wallet_id,
                   "recipient_wallet_id" : recipient_wallet_id,
                   "amount": amount}
        response = OpayAPI.post("/wallet/transfer", payload)
        if response["status"] == "success":
            return {"success": True, "transaction_id": response["data"]["transactionId"]}
        return {"success": False, "message": response["message"]}
    except Exception as e:
        return {"success": False, "message": str(e)}

# api call func to buy airtime
def buy_airtime(phone_number, network, amount):
    granny_user = User.query.filter_by(username='sssnew').first()
    wallet_id = granny_user.api_wallet_id
    try:
        payload = {
            "walletId": wallet_id,
            "phoneNumber": phone_number,
            "network": network,
            "amount": amount,
        }
        response = OpayAPI.post("/airtime/buy", payload)
        if response["status"] == "success":
            return {"success": True, "transaction_id": response["data"]["transactionId"]}
        return {"success": False, "message": response["message"]}
    except Exception as e:
        return {"success": False, "message": str(e)}
