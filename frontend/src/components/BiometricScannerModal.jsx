import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Fingerprint, ScanFace, X, CheckCircle, Loader2 } from 'lucide-react';

export default function BiometricScannerModal({ isOpen, onClose, onSuccess }) {
  const [step, setStep] = useState('idle');
  const [scanType, setScanType] = useState('face');
  const [holdProgress, setHoldProgress] = useState(0);
  const holdIntervalRef = React.useRef(null);
  const videoRef = React.useRef(null);
  const streamRef = React.useRef(null);

  useEffect(() => {
    if (isOpen) setStep('idle');
    else stopCamera();
    
    return () => {
      stopCamera();
      clearInterval(holdIntervalRef.current);
    };
  }, [isOpen]);

  const stopCamera = () => {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach(track => track.stop());
      streamRef.current = null;
    }
  };

  const completeScan = () => {
    setStep('authenticating');
    stopCamera();
    setTimeout(() => {
      setStep('success');
      setTimeout(() => {
        onSuccess();
        onClose();
      }, 1500);
    }, 1500);
  };

  const startHold = () => {
    if (scanType !== 'fingerprint') return;
    setHoldProgress(0);
    holdIntervalRef.current = setInterval(() => {
      setHoldProgress(p => {
        if (p >= 100) {
          clearInterval(holdIntervalRef.current);
          completeScan();
          return 100;
        }
        return p + 2.5;
      });
    }, 50);
  };

  const endHold = () => {
    if (scanType !== 'fingerprint' || holdProgress >= 100) return;
    clearInterval(holdIntervalRef.current);
    setHoldProgress(0);
  };

  const startScan = async (type) => {
    setScanType(type);
    setStep('scanning');
    setHoldProgress(0);

    if (type === 'face') {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        streamRef.current = stream;
        setTimeout(() => {
          if (videoRef.current) videoRef.current.srcObject = stream;
        }, 100);
      } catch (err) {
        console.error("Camera access denied or unavailable", err);
      }
    }
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
              <div className="flex flex-col items-center">
                <div 
                  className={`relative w-48 h-48 sm:w-56 sm:h-56 flex items-center justify-center overflow-hidden rounded-full border-4 ${scanType === 'fingerprint' ? 'cursor-pointer' : ''} select-none touch-none`}
                  style={{ 
                    borderColor: scanType === 'face' ? 'rgba(99,102,241,0.3)' : `rgba(16,185,129,${Math.max(0.3, holdProgress/100)})`, 
                    background: 'rgba(0,0,0,0.2)' 
                  }}
                  onMouseDown={startHold}
                  onMouseUp={endHold}
                  onMouseLeave={endHold}
                  onTouchStart={startHold}
                  onTouchEnd={endHold}
                >
                  {scanType === 'face' ? (
                    <video ref={videoRef} autoPlay playsInline muted className="absolute inset-0 w-full h-full object-cover transform -scale-x-100" />
                  ) : (
                    <Fingerprint className="w-24 h-24" style={{ color: `rgba(16,185,129,${Math.max(0.5, holdProgress/100)})`, transform: `scale(${1 + holdProgress/400})` }} />
                  )}
                  
                  {/* Face Target Overlay */}
                  {scanType === 'face' && (
                    <div className="absolute inset-0 z-10 pointer-events-none" style={{ backgroundImage: 'radial-gradient(transparent 40%, rgba(0,0,0,0.6) 100%)' }}>
                      <div className="absolute inset-4 border border-brand-500/30 rounded-full" />
                      <motion.div initial={{ top: 0, opacity: 0 }} animate={{ top: ['0%', '100%', '0%'], opacity: [0, 1, 1, 0] }} transition={{ duration: 2, repeat: Infinity, ease: "linear" }} className="absolute left-0 right-0 h-1 bg-brand-400 shadow-[0_0_15px_rgba(99,102,241,1)] z-10" />
                    </div>
                  )}

                  {/* Fingerprint Progress Overlay */}
                  {scanType === 'fingerprint' && (
                    <div className="absolute bottom-0 left-0 right-0 bg-emerald-500/20 transition-all duration-75" style={{ height: `${holdProgress}%` }} />
                  )}
                </div>

                <div className="mt-8">
                  {scanType === 'face' ? (
                     <button onClick={completeScan} className="btn-primary px-8 py-3 rounded-full text-sm font-bold shadow-lg shadow-brand-500/30 flex items-center gap-2 hover:scale-105 transition-transform">
                       <ScanFace className="w-5 h-5" /> Capture & Verify
                     </button>
                  ) : (
                     <p className="text-sm font-bold text-emerald-500 animate-pulse bg-emerald-500/10 px-6 py-2 rounded-full border border-emerald-500/20 select-none">
                       {holdProgress > 0 ? `${Math.floor(holdProgress)}% Scanning...` : 'Press & Hold to Scan'}
                     </p>
                  )}
                </div>
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
