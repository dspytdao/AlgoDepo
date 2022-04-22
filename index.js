import { deposit } from "./deposit.js";
import { asa_deposit } from "./asa_deposit.js";
import { deploy } from "./deploy.js";
import { asset_Id } from "./config.js";

const main = async () =>{
    var appId = await deploy()

    await deposit(appId);
    
    asa_deposit(appId, asset_Id);
};

main()