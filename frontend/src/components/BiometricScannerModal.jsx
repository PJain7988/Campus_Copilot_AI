import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Fingerprint, ScanFace, X, CheckCircle, Loader2 } from 'lucide-react';

export default function BiometricScannerModal({ isOpen, onClose, onSuccess }) {
  const [step, setStep] = useState('idle'); // idle, scanning, authenticating, success
  const [scanType, setScanType] = useState('face'); // face or fingerprint

  useEffect(() => {
    if (isOpen) setStep('idle');
  }, [isOpen]);

  const startScan = (type) => {
    setScanType(type);
    setStep('scanning');

    setTimeout(() => {
      setStep('authenticating');
      setTimeout(() => {
        setStep('success');
        setTimeout(() => {
          onSuccess();
          onClose();
        }, 1500);
      }, 1500);
    }, 2000);
  };

  if (!isOpen) return null;

  return (
    <AnimatePresence>
      <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
        {/* Backdrop */}
        <motion.div 
          initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
          onClick={step === 'idle' ? onClose : undefined}
          className="absolute inset-0 bg-black/60 backdrop-blur-sm"
        />

        {/* Modal */}
        <motion.div 
          initial={{ opacity: 0, scale: 0.95, y: 20 }}
          animate={{ opacity: 1, scale: 1, y: 0 }}
          exit={{ opacity: 0, scale: 0.95, y: 20 }}
          className="relative w-full max-w-md rounded-3xl overflow-hidden shadow-2xl border"
          style={{ background: 'var(--bg-card)', borderColor: 'var(--border)' }}
        >
          {/* Header */}
          <div className="p-6 pb-0 flex items-center justify-between">
            <div>
              <h3 className="text-xl font-bold" style={{ color: 'var(--text-primary)' }}>Secure Sync</h3>
              <p className="text-xs mt-1 uppercase tracking-wider font-bold" style={{ color: 'var(--text-muted)' }}>Smart Campus Gateway</p>
            </div>
            {step === 'idle' && (
              <button onClick={onClose} className="p-2 rounded-full hover:bg-white/5 transition-colors">
                <X className="w-5 h-5 text-slate-400" />
              </button>
            )}
          </div>

          <div className="p-8 flex flex-col items-center">
            {step === 'idle' && (
              <div className="w-full flex gap-4">
                <button onClick={() => startScan('face')} className="flex-1 flex flex-col items-center justify-center gap-3 p-6 rounded-2xl border transition-all hover:bg-white/5 hover:border-brand-500/50" style={{ borderColor: 'var(--border)' }}>
                  <ScanFace className="w-12 h-12 text-brand-400" />
                  <span className="text-sm font-bold" style={{ color: 'var(--text-secondary)' }}>Face ID</span>
                </button>
                <button onClick={() => startScan('fingerprint')} className="flex-1 flex flex-col items-center justify-center gap-3 p-6 rounded-2xl border transition-all hover:bg-white/5 hover:border-emerald-500/50" style={{ borderColor: 'var(--border)' }}>
                  <Fingerprint className="w-12 h-12 text-emerald-400" />
                  <span className="text-sm font-bold" style={{ color: 'var(--text-secondary)' }}>Biometric</span>
                </button>
              </div>
            )}

            {step === 'scanning' && (
              <div className="relative w-32 h-32 flex items-center justify-center">
                {/* Scanner frame */}
                <div className="absolute inset-0 rounded-2xl border-2 border-brand-500/30" />
                {/* The icon */}
                {scanType === 'face' ? <ScanFace className="w-16 h-16 text-brand-500" /> : <Fingerprint className="w-16 h-16 text-emerald-500" />}
                {/* The scanning laser */}
                <motion.div 
                  initial={{ top: 0, opacity: 0 }}
                  animate={{ top: ['0%', '100%', '0%'], opacity: [0, 1, 1, 0] }}
                  transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
                  className="absolute left-0 right-0 h-1 bg-brand-400 shadow-[0_0_15px_rgba(99,102,241,0.8)]"
                />
                <p className="absolute -bottom-8 text-sm font-bold animate-pulse" style={{ color: 'var(--text-primary)' }}>Scanning...</p>
              </div>
            )}

            {step === 'authenticating' && (
              <div className="flex flex-col items-center justify-center py-6">
                <Loader2 className="w-12 h-12 text-brand-400 animate-spin mb-4" />
                <p className="text-sm font-bold" style={{ color: 'var(--text-primary)' }}>Authenticating with Ledger...</p>
                <p className="text-xs mt-2" style={{ color: 'var(--text-muted)' }}>Retrieving campus activity logs</p>
              </div>
            )}

            {step === 'success' && (
              <motion.div 
                initial={{ scale: 0.5, opacity: 0 }} animate={{ scale: 1, opacity: 1 }}
                className="flex flex-col items-center justify-center py-6"
              >
                <div className="w-16 h-16 rounded-full bg-emerald-500/20 flex items-center justify-center mb-4 border border-emerald-500/30">
                  <CheckCircle className="w-8 h-8 text-emerald-500" />
                </div>
                <p className="text-lg font-black text-emerald-500">Sync Complete!</p>
                <p className="text-xs mt-1" style={{ color: 'var(--text-muted)' }}>Activities have been securely logged.</p>
              </motion.div>
            )}
          </div>
        </motion.div>
      </div>
    </AnimatePresence>
  );
}
