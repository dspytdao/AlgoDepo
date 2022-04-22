import { encodeUint64, getApplicationAddress, makeApplicationNoOpTxn, } from "algosdk";

import { algodClient, submitTransaction } from "./utils.js";
import { user } from "./config.js";

export const asa_deposit = async (appId, asset_id) => {
  
    // get transaction params
    const params = await algodClient.getTransactionParams().do();
  
    // deposit
    const enc = new TextEncoder();
    const depositAmount = 1000;
  
    let txn = makeApplicationNoOpTxn(
      user.addr,
      { ...params, flatFee: true, fee: 3000 }, // must pay for inner transaction
      appId,
      [enc.encode("asa_deposit"), encodeUint64(depositAmount)],
      undefined,
      undefined,
      [asset_id],//asset that we transfer
      undefined,
      undefined,
      getApplicationAddress(appId), // rekey to application address
    );
    let txId = await submitTransaction(txn, user.sk);
  
    console.log("Deposit transaction id: " + txId);
  }