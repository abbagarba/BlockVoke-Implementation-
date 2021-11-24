// SPDX-License-Identifier: GPL-3.0
pragma solidity >=0.7.0 <0.9.0;
contract revoke{
    address payable CA;
    address payable Owner;
    bool revoked;
    uint deposit;
    
    modifier isOwner(){
        require(msg.sender == Owner, "Caller is not Owner");
        _;
    }
    
    modifier isCA(){
        require(msg.sender == CA, "Caller is not CA");
        _;
    }
    
    constructor(address payable NewOwner){
        CA=payable(msg.sender);
        Owner=NewOwner;
        deposit=0;
        revoked=false;
    }
    
    function RevokeByCA()public payable isCA {
        revoked=true;
        PaybackCA();
    }
    
    function PaybackCA()internal {
         selfdestruct(CA);
    }

    function RevokeByOwner()public payable isOwner {
        revoked=true;
        PaybackOwner();
    }
    
    function PaybackOwner()internal {
         selfdestruct(Owner);
    }
    function getstatus() external view returns (bool){
        return revoked;
    }
}

    fallback(){
      if(msg.value>0&&msg.sender==CA)
         RevokeByCA();
      else if(msg.value>0&&msg.sender==Owner)
        RevokeByOwner();
    }
    receive(){
      if(msg.value>0&&msg.sender==CA)
         RevokeByCA();
      else if(msg.value>0&&msg.sender==Owner)
        RevokeByOwner();
    }
