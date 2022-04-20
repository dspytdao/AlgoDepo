import algosdk from "algosdk";

export const algodClient = new algosdk.Algodv2('', 'https://testnet-api.algonode.cloud/', 443);

export async function submitTransaction(txn, sk) {
    const signedTxn = txn.signTxn(sk);
    const { txId } = await algodClient.sendRawTransaction(signedTxn).do();
    await algosdk.waitForConfirmation(algodClient, txId, 1000);
    return txId;
}