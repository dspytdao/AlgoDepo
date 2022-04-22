import { mnemonicToSecretKey } from "algosdk";

import dotenv from "dotenv";
dotenv.config();

export const user = mnemonicToSecretKey(process.env.Mnemo);
export const asset_Id = 84891710;