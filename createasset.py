import os
from dotenv import load_dotenv
from algosdk import account
from algosdk.future import transaction
from algosdk.v2client import algod
from algosdk import mnemonic
load_dotenv()

algod_address = "https://testnet-algorand.api.purestake.io/ps2"
algod_token = "rw0sHyrj9h5Fvro77Jpvu1uFHIyUWY8o5pTeSMWE"
headers = {
   "X-API-Key": algod_token,
}

# initialize an algodClient
algod_client = algod.AlgodClient(algod_token, algod_address, headers)

Mnemo = os.getenv('Mnemo')

private_key = mnemonic.to_private_key(Mnemo)



def wait_for_confirmation(client, txid):
    last_round = client.status().get("last-round")
    txinfo = client.pending_transaction_info(txid)
    while not (txinfo.get("confirmed-round") and txinfo.get("confirmed-round") > 0):
        print("Waiting for confirmation...")
        last_round += 1
        client.status_after_block(last_round)
        txinfo = client.pending_transaction_info(txid)
    print(
        "Transaction {} confirmed in round {}.".format(
            txid, txinfo.get("confirmed-round")
        )
    )
    return txinfo


def create_asset(client, private_key):
    # declare sender
    sender = account.address_from_private_key(private_key)

    params = client.suggested_params()

    txn = transaction.AssetConfigTxn(
        sender=sender,
        sp=params,
        total=1_000_000_000,
        default_frozen=False,
        unit_name="C3pio",
        asset_name="C3coin",
        manager=sender,
        reserve=sender,
        freeze=sender,
        clawback=sender,
        strict_empty_address_check=False,
        url=None, 
        decimals=0)

    # Sign with secret key of creator
    stxn = txn.sign(private_key)

    # Send the transaction to the network and retrieve the txid.
    
    txid = client.send_transaction(stxn)
    print("Signed transaction with txID: {}".format(txid))
    # Wait for the transaction to be confirmed
    confirmed_txn = wait_for_confirmation(client, txid)  
    print("TXID: ", txid)
    print("Result confirmed in round: {}".format(confirmed_txn['confirmed-round']))  

create_asset(algod_client, private_key)