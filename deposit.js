import { encodeUint64, getApplicationAddress, makeApplicationNoOpTxn, } from "algosdk";

import { algodClient, submitTransaction } from "./utils.js";
import { appId, user } from "./config.js";

async function main() {
  let txn
  let txId

  // get transaction params
  const params = await algodClient.getTransactionParams().do();

  // deposit
  const enc = new TextEncoder();
  const depositAmount = 2 * 1e5;

  txn = makeApplicationNoOpTxn(
    user.addr,
    { ...params, flatFee: true, fee: 2000 }, // must pay for inner transaction
    appId,
    [enc.encode("deposit"), encodeUint64(depositAmount)],
    undefined,
    undefined,
    undefined,
    undefined,
    undefined,
    getApplicationAddress(appId), // rekey to application address
  );
  txId = await submitTransaction(txn, user.sk);

  console.log("Deposit transaction id: " + txId);
}

main().catch(console.error);