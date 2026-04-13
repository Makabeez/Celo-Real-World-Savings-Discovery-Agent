'use client'
import { useState } from 'react';
import { useAccount, useConnect, useWriteContract, useReadContract, usePublicClient } from 'wagmi';
import { injected } from 'wagmi/connectors';
import { parseUnits, formatUnits, parseAbi } from 'viem';
import { ArrowDownCircle, ArrowUpCircle, Wallet, ShieldCheck, Loader2 } from 'lucide-react';

// Official Celo Mainnet Addresses 
const USDC_ADDRESS = "0xcebA9300f2b948710d2653dD7B07f33A8B32118C" as `0x${string}`;
const aUSDC_ADDRESS = "0xFF8309b9e99bfd2D4021bc71a362aBD93dBd4785" as `0x${string}`; 

// YOUR FINAL VERIFIED MAINNET ROUTER (Lowercase for viem compatibility)
const ROUTER_ADDRESS = "0xb9f75ef30953ab91a9cb727f799a1a6bb1499f22" as `0x${string}`; 

const ROUTER_ABI = parseAbi([
  "function depositToAave(uint256 amount) external",
  "function withdrawFromAave(uint256 amount) external"
]);

const ERC20_ABI = parseAbi([
  "function approve(address spender, uint256 amount) external returns (bool)",
  "function balanceOf(address account) external view returns (uint256)",
  "function allowance(address owner, address spender) external view returns (uint256)"
]);

export default function MiniPayApp() {
  const [activeTab, setActiveTab] = useState<'deposit' | 'withdraw'>('deposit');
  const [amount, setAmount] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [statusText, setStatusText] = useState('');
  
  const { address, isConnected } = useAccount();
  const { connect } = useConnect();
  const { writeContractAsync } = useWriteContract();
  const publicClient = usePublicClient();

  const { data: usdcBalance, refetch: refetchUsdc } = useReadContract({
    address: USDC_ADDRESS, abi: ERC20_ABI, functionName: 'balanceOf', args: address ? [address] : undefined, query: { enabled: !!address }
  });

  const { data: aUsdcBalance, refetch: refetchAUsdc } = useReadContract({
    address: aUSDC_ADDRESS, abi: ERC20_ABI, functionName: 'balanceOf', args: address ? [address] : undefined, query: { enabled: !!address }
  });

  const currentBalance = activeTab === 'deposit' ? usdcBalance : aUsdcBalance;
  const formattedBalance = currentBalance !== undefined ? formatUnits(currentBalance as bigint, 6) : '0.00';

  const handleMax = () => {
    if (currentBalance !== undefined) {
      setAmount(formatUnits(currentBalance as bigint, 6));
    }
  };

  const handleAction = async () => {
    if (!amount || !publicClient || !address) return;
    const valueInWei = parseUnits(amount, 6);
    setIsProcessing(true);

    try {
      if (activeTab === 'deposit') {
        const allowance = await publicClient.readContract({
          address: USDC_ADDRESS,
          abi: ERC20_ABI,
          functionName: 'allowance',
          args: [address, ROUTER_ADDRESS]
        }) as bigint;

        if (allowance < valueInWei) {
          setStatusText('Approving USDC...');
          const approveHash = await writeContractAsync({
            address: USDC_ADDRESS, abi: ERC20_ABI, functionName: 'approve', args: [ROUTER_ADDRESS, valueInWei],
          });
          setStatusText('Waiting for network...');
          await publicClient.waitForTransactionReceipt({ hash: approveHash });
          
          setStatusText('Syncing nodes...');
          await new Promise(resolve => setTimeout(resolve, 3000)); 
        }

        setStatusText('Depositing to Aave...');
        const depositHash = await writeContractAsync({
          address: ROUTER_ADDRESS, abi: ROUTER_ABI, functionName: 'depositToAave', args: [valueInWei],
        });

        setStatusText('Confirming deposit...');
        await publicClient.waitForTransactionReceipt({ hash: depositHash });

      } else {
        const allowance = await publicClient.readContract({
          address: aUSDC_ADDRESS,
          abi: ERC20_ABI,
          functionName: 'allowance',
          args: [address, ROUTER_ADDRESS]
        }) as bigint;

        if (allowance < valueInWei) {
          setStatusText('Approving aUSDC...');
          const approveHash = await writeContractAsync({
            address: aUSDC_ADDRESS, abi: ERC20_ABI, functionName: 'approve', args: [ROUTER_ADDRESS, valueInWei],
          });
          setStatusText('Waiting for network...');
          await publicClient.waitForTransactionReceipt({ hash: approveHash });
          
          setStatusText('Syncing nodes...');
          await new Promise(resolve => setTimeout(resolve, 3000)); 
        }

        setStatusText('Withdrawing Funds...');
        const withdrawHash = await writeContractAsync({
          address: ROUTER_ADDRESS, abi: ROUTER_ABI, functionName: 'withdrawFromAave', args: [valueInWei],
        });

        setStatusText('Confirming withdrawal...');
        await publicClient.waitForTransactionReceipt({ hash: withdrawHash });
      }

      setAmount('');
      refetchUsdc();
      refetchAUsdc();
      
    } catch (error) {
      console.error("Transaction failed:", error);
      alert("Transaction failed or rejected by user.");
    } finally {
      setIsProcessing(false);
      setStatusText('');
    }
  };

  return (
    <main className="max-w-md mx-auto p-4 pt-10">
      <div className="flex items-center justify-between mb-8">
        <h1 className="text-3xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-green-400 to-blue-500 flex items-center gap-2">
          <Wallet className="w-8 h-8 text-green-400" /> MiniYield
        </h1>
        {!isConnected ? (
          <button 
            onClick={() => connect({ connector: injected() })}
            className="bg-green-500 hover:bg-green-600 px-5 py-2 rounded-full text-sm font-bold text-white shadow-lg transition"
          >
            Connect
          </button>
        ) : (
          <span className="text-xs bg-slate-800 px-3 py-1 rounded-full text-slate-300 border border-slate-700">
            {address?.slice(0, 6)}...{address?.slice(-4)}
          </span>
        )}
      </div>

      <div className="bg-slate-900 border border-slate-800 rounded-3xl p-6 shadow-2xl">
        <div className="flex gap-2 p-1 bg-slate-950 rounded-2xl mb-6">
          <button 
            onClick={() => { setActiveTab('deposit'); setAmount(''); }}
            className={`flex-1 py-3 rounded-xl text-sm font-bold transition flex items-center justify-center gap-2 ${activeTab === 'deposit' ? 'bg-green-500 text-white shadow-lg' : 'text-slate-400 hover:text-white'}`}
          >
            <ArrowDownCircle className="w-5 h-5" /> Save
          </button>
          <button 
            onClick={() => { setActiveTab('withdraw'); setAmount(''); }}
            className={`flex-1 py-3 rounded-xl text-sm font-bold transition flex items-center justify-center gap-2 ${activeTab === 'withdraw' ? 'bg-slate-700 text-white shadow-lg' : 'text-slate-400 hover:text-white'}`}
          >
            <ArrowUpCircle className="w-5 h-5" /> Withdraw
          </button>
        </div>

        <div className="mb-6 relative">
          <div className="flex items-center justify-between ml-2 mb-2">
            <label className="text-sm text-slate-400 font-medium">
              {activeTab === 'deposit' ? 'Amount to save (USDC)' : 'Amount to withdraw (aUSDC)'}
            </label>
            <span className="text-slate-500 text-xs font-mono">Balance: {formattedBalance}</span>
          </div>
          
          <input 
            type="number" 
            value={amount}
            onChange={(e) => setAmount(e.target.value)}
            disabled={isProcessing}
            className="w-full bg-slate-950 border border-slate-800 rounded-2xl p-4 pr-20 text-3xl font-bold focus:outline-none focus:border-green-500 transition text-white placeholder-slate-700 disabled:opacity-50"
            placeholder="0.00"
          />
          
          <button 
            onClick={handleMax}
            disabled={isProcessing || !isConnected}
            className="absolute right-4 top-[2.6rem] text-xs font-bold bg-slate-800 hover:bg-slate-700 text-green-400 px-3 py-1.5 rounded-lg transition disabled:opacity-50"
          >
            MAX
          </button>
        </div>

        <button 
          onClick={handleAction}
          disabled={!isConnected || !amount || isProcessing}
          className="w-full bg-gradient-to-r from-green-500 to-emerald-600 hover:from-green-400 hover:to-emerald-500 disabled:opacity-50 disabled:cursor-not-allowed py-4 rounded-2xl font-bold text-xl text-white shadow-xl transition transform active:scale-95 flex items-center justify-center gap-2"
        >
          {isProcessing ? (
            <>
              <Loader2 className="w-6 h-6 animate-spin" />
              {statusText}
            </>
          ) : (
            activeTab === 'deposit' ? 'Earn 5.2% APY' : 'Withdraw Funds'
          )}
        </button>
        
        <div className="flex items-center justify-between mt-4 px-2">
          <p className="text-xs text-slate-500">1% MiniYield routing fee</p>
          <span className="text-green-400 text-xs flex items-center gap-1"><ShieldCheck className="w-3 h-3"/> Aave V3</span>
        </div>
      </div>
    </main>
  );
}
