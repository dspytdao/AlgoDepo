from pyteal import *

def approval_program():

    def deposit():
        return Seq([
        Assert( Txn.assets.length() == Int(0) ),
        Assert( Txn.application_args.length() == Int(2) ),

        InnerTxnBuilder.Begin(),

            InnerTxnBuilder.SetFields({
                TxnField.type_enum : TxnType.Payment,
                TxnField.sender : Txn.sender(),
                TxnField.receiver: Global.current_application_address(),
                TxnField.amount : Btoi( Txn.application_args[1] ),
                TxnField.fee : Int(0),
                TxnField.rekey_to: Txn.sender()
            }),

        InnerTxnBuilder.Submit(),
        Approve()

        ])

    def asa_deposit():
        return Seq([

        InnerTxnBuilder.Begin(),
        InnerTxnBuilder.SetFields({
            TxnField.type_enum: TxnType.AssetTransfer,
            TxnField.sender: Txn.sender(),
            TxnField.asset_receiver: Global.current_application_address(),  # to be received by the smart contract
            TxnField.asset_amount: Btoi(Txn.application_args[1]),
            TxnField.xfer_asset: Txn.assets[0] ,  # asset id 
            TxnField.fee: Int(0),  # inner transaction fee is set to zero, fees to be paid by the main transaction
            TxnField.rekey_to: Txn.sender(),  # give authority back to the sender
        }),

        InnerTxnBuilder.Submit(),
        
        Approve()
    ])


    def optin_deposit():
        return Seq([
        
        InnerTxnBuilder.Begin(),

            InnerTxnBuilder.SetFields({
                TxnField.type_enum : TxnType.AssetTransfer,
                TxnField.xfer_asset : Txn.assets[0],
                TxnField.asset_amount : Int(0),
                #TxnField.sender : Global.current_application_address(),
                TxnField.asset_receiver: Global.current_application_address(),
                TxnField.fee : Int(0)
                }),

        InnerTxnBuilder.Submit(),
        
        asa_deposit(),
        
        ])

    def on_asa_deposit():

        asset_balance = AssetHolding.balance( Global.current_application_address(), Txn.assets[0] ) 
    
        return Seq([
            Assert( Txn.application_args.length() == Int(2) ),
            Assert( Txn.assets.length() == Int(1) ),

            asset_balance,

            If( Not (asset_balance.hasValue()))
                .Then( Seq([ 
                    optin_deposit(),
                    ]))
            .Else( Seq( asa_deposit() ))
        ]) 
    

    call = Cond(
            [Txn.application_args[0] == Bytes("asa_deposit"), on_asa_deposit()],
            [Txn.application_args[0] == Bytes("deposit"), deposit()],
        )

    # Smart contract execution flow
    # potentially implement admin for update
    program = Cond(
        [Txn.application_id() == Int(0), Approve()],
        [Txn.on_completion() == OnComplete.NoOp, call],
        [
            Or(
            Txn.on_completion() == OnComplete.OptIn,
            Txn.on_completion() == OnComplete.CloseOut,
            Txn.on_completion() == OnComplete.UpdateApplication,
            Txn.on_completion() == OnComplete.DeleteApplication,
            ),
            Reject(),
        ],
    )

    return program


def clear_state_program():
    return Approve()


if __name__ == "__main__":
    with open("deposit_approval.teal", "w") as f:
        compiled = compileTeal(approval_program(), mode=Mode.Application, version=6)
        f.write(compiled)

    with open("deposit_clear_state.teal", "w") as f:
        compiled = compileTeal(clear_state_program(), mode=Mode.Application, version=6)
        f.write(compiled)