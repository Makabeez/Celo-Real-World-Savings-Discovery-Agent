import React from 'react';

interface AgentData {
  status: string;
  celo_price: number;
  active_strategy: string;
  reasoning: string;
  balance_celo: number;
  balance_usdc: number;
  visa_status: string;
  tx_count: number;
  timestamp: string;
}

export const ReasoningCard = ({ data }: { data: AgentData }) => {
  const targetTx = 10000;
  const isCitizen = data.tx_count >= targetTx;
  const isWorkVisa = data.tx_count >= 1000;
  
  let badgeColor = "bg-yellow-900/50 text-yellow-400 border-yellow-500";
  let dotColor = "bg-yellow-500";
  
  if (isCitizen) {
    badgeColor = "bg-yellow-500/20 text-yellow-300 border-yellow-400 shadow-[0_0_15px_rgba(234,179,8,0.5)]";
    dotColor = "bg-yellow-400";
  } else if (isWorkVisa) {
    badgeColor = "bg-purple-900/50 text-purple-400 border-purple-500 shadow-[0_0_10px_rgba(168,85,247,0.5)]";
    dotColor = "bg-purple-500";
  }

  const progressPercent = Math.min((data.tx_count / targetTx) * 100, 100);

  return (
    <div className="bg-slate-900 border border-slate-800 p-6 rounded-xl shadow-2xl max-w-md w-full transition-all duration-500">
      
      <div className="flex justify-between items-start mb-6 border-b border-slate-800 pb-4">
        <div>
          <div className="flex items-center space-x-2 mb-2">
            <div className={`h-3 w-3 rounded-full animate-pulse ${dotColor}`} />
            <h3 className="text-slate-100 font-semibold tracking-wide uppercase text-xs">Live Status</h3>
          </div>
          <div className={`inline-block px-2 py-1 text-[10px] uppercase font-bold tracking-wider rounded border ${badgeColor}`}>
            {data.visa_status}
          </div>
        </div>
        <div className="text-right">
          <span className="text-xs text-slate-500 block">Live $CELO</span>
          <span className="text-yellow-500 font-mono font-bold text-lg">${data.celo_price.toFixed(3)}</span>
        </div>
      </div>

      {!isCitizen ? (
        <div className="mb-6">
          <div className="flex justify-between text-xs mb-1">
            <span className="text-slate-400 uppercase tracking-wider font-bold">Citizenship Progress</span>
            <span className="text-purple-400 font-mono font-bold">{data.tx_count} / {targetTx} TXs</span>
          </div>
          <div className="w-full bg-slate-800 rounded-full h-2.5 border border-slate-700 overflow-hidden">
            <div 
              className="bg-purple-500 h-2.5 rounded-full transition-all duration-1000 ease-in-out relative" 
              style={{ width: `${progressPercent}%` }}
            >
              <div className="absolute inset-0 bg-white/20 animate-pulse"></div>
            </div>
          </div>
        </div>
      ) : (
        <div className="mb-6 p-3 bg-yellow-900/20 border border-yellow-500/30 rounded-lg text-center animate-fade-in">
          <span className="text-yellow-400 text-xs uppercase tracking-widest font-bold block mb-1">👑 Celo Citizenship Unlocked</span>
          <span className="text-slate-300 text-sm">Agent deployed to 14M+ MiniPay users.</span>
        </div>
      )}

      <div className="mb-4 bg-slate-800/50 p-3 rounded-lg border border-slate-700">
        <span className="text-xs text-blue-400 uppercase tracking-wider font-bold block mb-1">Active Strategy</span>
        <span className="text-slate-200 text-sm font-medium">{data.active_strategy}</span>
      </div>

      <p className="text-slate-300 text-sm italic mb-6">
        "{data.reasoning}"
      </p>

      <div className="space-y-3">
        <div className="flex justify-between text-xs text-slate-500 border-b border-slate-800 pb-2">
          <span>CELO Wallet Balance</span>
          <span className="text-slate-200 font-mono">{data.balance_celo.toFixed(2)}</span>
        </div>
        <div className="flex justify-between text-xs text-slate-500 border-b border-slate-800 pb-2">
          <span>USDC Yield Vault</span>
          <span className="text-green-400 font-mono">${data.balance_usdc.toFixed(2)}</span>
        </div>
        <div className="flex justify-between text-xs text-slate-500">
          <span>Last Network Sync</span>
          <span className="text-slate-200 font-mono">{data.timestamp}</span>
        </div>
      </div>

      <button className={`w-full mt-6 py-3 font-bold rounded-lg transition-all text-sm uppercase tracking-wide ${isCitizen ? 'bg-yellow-500 hover:bg-yellow-600 text-slate-900' : 'bg-purple-600 hover:bg-purple-700 text-white'}`}>
        Verify on CeloScan
      </button>
    </div>
  );
};
