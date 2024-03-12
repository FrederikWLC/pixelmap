// SPDX-License-Identifier: GPL-3.0-or-later

pragma solidity ^0.8.0;

interface IPixelMapCoin {

	/// @notice A struct representing the RGB-color of a pixel.
    /// @param r The value of red (0-255)
    /// @param g The value of green (0-255)
    /// @param b The value of blue (0-255)
    struct Color {
        uint8 r;
        uint8 g; 
        uint8 b; 
    }

   /**
    * @dev Emitted when the `color` of a pixel is set with
    * a call to {setPixel}.
    */
	event Pixel(address indexed by, uint8 indexed x, uint8 indexed y, Color color);

   /**
    * @dev Paints a pixel at coordinate ('x','y') with ('r','g','b') color.
    *
    * Returns a boolean value indicating whether the operation succeeded.
    *
    * Emits a {Pixel} event.
    */
    function setPixel(uint8 x, uint8 y, uint8 r, uint8 g, uint8 b) external returns(bool);

}