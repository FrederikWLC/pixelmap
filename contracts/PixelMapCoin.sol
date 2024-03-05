// SPDX-License-Identifier: GPL-3.0-or-later
pragma solidity ^0.8.0;

import "node_modules/@openzeppelin/contracts/token/ERC20/extensions/ERC20Burnable.sol";
import "node_modules/@openzeppelin/contracts/token/ERC20/ERC20.sol";
import {IPixelMapCoin} from "./IPixelMapCoin.sol";

contract PixelMapCoin is ERC20, ERC20Burnable, IPixelMapCoin {

    /// @notice Mapping taking an integer (x) pointing to another mapping taking an integer (y) pointing to a Color struct.
    mapping(uint8 => mapping(uint8 => Color)) private mapCoordinates;

    constructor() ERC20("Pixel Map Coin", "PMC") {
        _mint(_msgSender(), 100_000_000_000 * 10**18 );
    }

    function setPixel(uint8 x, uint8 y, uint8 r, uint8 g, uint8 b) external returns(bool) {
        require(balanceOf(_msgSender())>=1,"Balance must be greater than 1 to paint a pixel.");
        mapCoordinates[x][y] = Color(r,g,b);
        _burn(_msgSender(),1);
        return true;
    }



}