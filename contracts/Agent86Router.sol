// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

// Import OpenZeppelin Security Standards
import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/utils/ReentrancyGuard.sol";
import "@openzeppelin/contracts/access/Ownable2Step.sol";

interface IPool {
    function supply(address asset, uint256 amount, address onBehalfOf, uint16 referralCode) external;
    function withdraw(address asset, uint256 amount, address to) external returns (uint256);
}

// Inherits ReentrancyGuard for security and Ownable2Step for safe ownership transfers
contract Agent86Router is ReentrancyGuard, Ownable2Step {
    using SafeERC20 for IERC20; 

    // Immutables save gas since these addresses never change
    IERC20 public immutable usdc;
    IERC20 public immutable aUsdc;
    IPool public immutable aavePool;

    // Fees set in Basis Points (100 = 1%)
    uint256 public constant ENTRY_FEE_BPS = 100;
    uint256 public constant EXIT_FEE_BPS = 100;

    // Events for off-chain indexing and frontend dashboards
    event Deposited(address indexed user, uint256 amount, uint256 fee);
    event Withdrawn(address indexed user, uint256 amount, uint256 fee);
    event FeesSwept(address indexed owner, uint256 amount);
    event EmergencyRecovered(address indexed token, address indexed to, uint256 amount);

    // Initialize Ownable with the deployer's address
    constructor() Ownable(msg.sender) {
        // Exact Checksummed Addresses required by Solidity 0.8.20
        usdc = IERC20(0xcebA9300f2b948710d2653dD7B07f33A8B32118C);
        aUsdc = IERC20(0xFF8309b9e99bfd2D4021bc71a362aBD93dBd4785);
        aavePool = IPool(0x3E59A31363E2ad014dcbc521c4a0d5757d9f3402);
        
        // Max approve the Aave Pool to spend USDC from this router contract
        usdc.approve(address(aavePool), type(uint256).max);
    }

    function depositToAave(uint256 amount) external nonReentrant {
        require(amount > 0, "Amount must be greater than 0");
        
        // 1. Pull USDC from user safely
        usdc.safeTransferFrom(msg.sender, address(this), amount);

        // 2. Calculate the 1% MiniYield routing fee
        uint256 fee = (amount * ENTRY_FEE_BPS) / 10000;
        uint256 amountAfterFee = amount - fee;

        // 3. Supply the remaining USDC to Aave on behalf of the user
        aavePool.supply(address(usdc), amountAfterFee, msg.sender, 0);

        // Emit event for tracking
        emit Deposited(msg.sender, amountAfterFee, fee);
    }

    function withdrawFromAave(uint256 amount) external nonReentrant {
        require(amount > 0, "Amount must be greater than 0");

        // 1. Pull aUSDC from user safely
        aUsdc.safeTransferFrom(msg.sender, address(this), amount);

        // 2. Withdraw FULL amount as USDC from Aave to THIS contract first
        aavePool.withdraw(address(usdc), amount, address(this));

        // 3. Calculate the 1% MiniYield routing fee in standard USDC
        uint256 fee = (amount * EXIT_FEE_BPS) / 10000;
        uint256 amountAfterFee = amount - fee;

        // 4. Send the remaining USDC directly to the user
        usdc.safeTransfer(msg.sender, amountAfterFee);

        // Emit event for tracking
        emit Withdrawn(msg.sender, amountAfterFee, fee);
    }

    // Admin function to sweep collected revenue fees
    function sweepFees() external onlyOwner {
        uint256 balance = usdc.balanceOf(address(this));
        require(balance > 0, "No fees to sweep");
        
        usdc.safeTransfer(owner(), balance);
        
        emit FeesSwept(owner(), balance);
    }

    // Emergency token recovery (e.g., someone accidentally sends random tokens here)
    function emergencyRecoverToken(address tokenAddress, uint256 tokenAmount) external onlyOwner {
        require(tokenAddress != address(usdc), "Cannot recover core USDC directly");
        require(tokenAddress != address(aUsdc), "Cannot recover aUSDC directly"); // Final safety lock
        
        IERC20(tokenAddress).safeTransfer(owner(), tokenAmount);
        
        emit EmergencyRecovered(tokenAddress, owner(), tokenAmount);
    }
}
