from .apis import OpayAPI
import time
import uuid
import os
from dotenv import load_dotenv


# func to generate ref id -> uuid
def generate_ref_id() -> str:
    ref_id = str(uuid.uuid4())
    return ref_id

# func to generate request serial number -> time stamp in millisecond
def generate_request_serial_number() -> str:
    request_serial_number = f"req_{int(time.time() * 1000 )}"
    return request_serial_number

# load env variables
load_dotenv()
opay_merchant_id = os.getenv("OPAY_MERCHANT_ID")
opay_collection_id = os.getenv("OPAY_COLLECTION_ID")

# financial services
# api call func to create wallet
def create_wallet(name, phone_number, email) -> dict:
    try:
        data = {
              "opayMerchantId": opay_merchant_id, # the merchant id
              "name": name, # user username
              "email": email, # user email
              "phone": phone_number, # user phone number
              "sendPassWordFlag":"N", # never sends email
              "refId": generate_ref_id(), # transaction ref id
              "accountType":"User", # assets belong to user not merchant ( but can be swept )
            }
        response = OpayAPI.post("api/v2/third/depositcode/generateStaticDepositCode", data)
        if response["code"] == "00000":
            return {"success": True, "wallet_id": response["data"]["depositCode"]}
        return {"success": False, "message": response["message"]}
    except Exception as e:
        return {"success": False, "message": f'error occurred: {str(e)}'}


# api func to create wallet with retries of 5
def create_wallet_with_retries(user) -> dict:
    attempts = 0
    while attempts < 4:
        response = create_wallet(user.name, user.phone_number, user.email)
        if response["success"]:
            return response
        else:
            attempts += 1
            time.sleep(2 ** attempts)
            ''' -> attempt 1: Wait 2 seconds, attempt 2: Wait 4 seconds, attempt 3: Wait 8 seconds and so on '''


# api call func to get transaction list
def fetch_api_wallet_transactions(user, start_time=None, end_time=None) -> dict:
    try:
        all_transactions = []
        page_no = 1
        while True:
            data = {
                "opayMerchantId": opay_merchant_id,
                "depositCodes": [user.api_wallet_account_number],
                "pageNo": page_no,
                "pageSize": 499,
            }
            if start_time:
                data["startTime"] = start_time
            if end_time:
                data["endTime"] = end_time
            response = OpayAPI.post("api/v2/third/depositcode/queryStaticDepositCodeTransList", data)
            if response["code"] == "00000":
                transactions = response["data"]
                all_transactions.extend(transactions)
                if len(transactions) < 499: # Check if there are more pages
                    break
                page_no += 1
            else:
                return {"success": False, "message": response["message"]}
        return {"success": True, "transactions": all_transactions}
    except Exception as e:
        return {"success": False, "message": f"error occurred: {str(e)}"}


# api call func to query wallet balance
def query_wallet_balance(user) -> dict:
    try:
        data = {
              "opayMerchantId": opay_merchant_id, # the merchant id
              "depositCode": user.api_wallet_account_number # the user deposit code
            }
        response = OpayAPI.post("api/v2/third/depositcode/queryWalletBalance", data)
        if response["code"] == "00000":
            return {"success": True, "wallet_balance": response["data"]["amount"]}
        return {"success": False, "message": response["message"]}
    except Exception as e:
        return {"success": False, "message": f'error occurred: {str(e)}'}


# api call func to deduct from user wallet to merchant wallet
def sweep_digital_wallet(user, amount, message) -> dict:
    try:
        data = {
            "amount": amount, # the amount
            "depositCode": user.api_wallet_account_number, # the user deposit code
            "opayMerchantId": opay_merchant_id, # merchant id
            "collectionMerchantId": opay_collection_id, # granny account ( master account )
            "requestSerialNo": generate_request_serial_number(), # request S/No.
            "description": f"{message}" # message of the transaction
        }
        response = OpayAPI.post("api/v2/third/depositcode/transferToMerchant", data)
        if response["status"] == "success":
            return {"success": True, "transaction_id": response["data"]["transactionId"]}
        return {"success": False, "message": response["message"]}
    except Exception as e:
        return {"success": False, "message": str(e)}



# api call func to transfer to other wallet
# def transfer_to_wallet(sender_wallet_id, reciever_wallet_id, amount):
#     try:
#         payload = {"sender_wallet_id": sender_wallet_id,
#                    "recipient_wallet_id": reciever_wallet_id,
#                    "amount": amount}
#         response = OpayAPI.post("/wallet/transfer", payload)
#         if response["status"] == "success":
#             return {"success": True, "balance": response["data"]["balance"]}
#         return {"success": False, "message": response["message"]}
#     except Exception as e:
#         return {"success": False, "message": str(e)}


# api call func to buy airtime
# def buy_airtime(phone_number, network, amount):
#     granny_user = User.query.filter_by(username='sssnew').first()
#     wallet_id = granny_user.api_wallet_id
#     try:
#         payload = {
#             "walletId": wallet_id,
#             "phoneNumber": phone_number,
#             "network": network,
#             "amount": amount,
#         }
#         response = OpayAPI.post("/airtime/buy", payload)
#         if response["status"] == "success":
#             return {"success": True, "transaction_id": response["data"]["transactionId"]}
#         return {"success": False, "message": response["message"]}
#     except Exception as e:
#         return {"success": False, "message": str(e)}
#
#
# # api call func to buy airtime
# def buy_data(phone_number, network, amount):
#     granny_user = User.query.filter_by(username='sssnew').first()
#     wallet_id = granny_user.api_wallet_id
#     try:
#         payload = {
#             "walletId": wallet_id,
#             "phoneNumber": phone_number,
#             "network": network,
#             "amount": amount,
#         }
#         response = OpayAPI.post("/data/buy", payload)
#         if response["status"] == "success":
#             return {"success": True, "transaction_id": response["data"]["transactionId"]}
#         return {"success": False, "message": response["message"]}
#     except Exception as e:
#         return {"success": False, "message": str(e)}
