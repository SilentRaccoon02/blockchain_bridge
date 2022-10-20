//SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

contract Demo {
    struct Payment {
        address from;
        uint256 to;
        uint256 amount;
        uint8 status;
    }

    Payment[] public payments;
    uint256 public payments_number = 0;

    function transfer(uint8 to) public payable {
        Payment memory temp = Payment(msg.sender, to, msg.value, 0);
        payments.push(temp);
        payments_number += 1;
    }
}
