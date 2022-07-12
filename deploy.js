import {
  makeApplicationCreateTxnFromObject,
  OnApplicationComplete,
  waitForConfirmation,
} from "algosdk";
import fs from "fs";

import { algodClient } from "./utils.js";
import { user } from "./config.js";

export const deploy = async () => {
  const suggestedParams = await algodClient.getTransactionParams().do();

  const app = fs.readFileSync(
    new URL("../AlgoDepo/contracts/deposit_approval.teal", import.meta.url),
    "utf8"
  );
  const compileApp = await algodClient.compile(app).do();

  const clearState = fs.readFileSync(
    new URL("../AlgoDepo/contracts/deposit_clear_state.teal", import.meta.url),
    "utf8"
  );
  const compiledClearProg = await algodClient.compile(clearState).do();

  const tx = makeApplicationCreateTxnFromObject({
    suggestedParams,
    from: user.addr,
    approvalProgram: new Uint8Array(Buffer.from(compileApp.result, "base64")),
    clearProgram: new Uint8Array(
      Buffer.from(compiledClearProg.result, "base64")
    ),
    numGlobalByteSlices: 0,
    numGlobalInts: 0,
    numLocalByteSlices: 0,
    numLocalInts: 0,
    onComplete: OnApplicationComplete.NoOpOC,
  });

  let txSigned = tx.signTxn(user.sk);
  const { txId } = await algodClient.sendRawTransaction(txSigned).do();
  const transactionResponse = await waitForConfirmation(algodClient, txId, 5);
  const appId = transactionResponse["application-index"];

  console.log("Created app-id: ", appId);

  return appId;
};
