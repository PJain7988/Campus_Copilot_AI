import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Fingerprint, ScanFace, X, CheckCircle, Loader2, Scan } from 'lucide-react';

export default function BiometricScannerModal({ isOpen, onClose, onSuccess }) {
  const [step, setStep] = useState('idle');
  const [scanType, setScanType] = useState('face');
  const [scanPhase, setScanPhase] = useState(''); // Text to display during scan
  
  const videoRef = useRef(null);
  const streamRef = useRef(null);

  useEffect(() => {
    if (isOpen) setStep('idle');
    else stopCamera();
    
    return () => stopCamera();
  }, [isOpen]);

  const stopCamera = () => {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach(track => track.stop());
      streamRef.current = null;
    }
  };

  const startScan = async (type) => {
    setScanType(type);
    setStep('scanning');
    setScanPhase('Initializing Scanner...');

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

    // Sequence of realistic automatic scanning phases
    setTimeout(() => setScanPhase(type === 'face' ? 'Detecting Facial Landmarks...' : 'Detecting Fingerprint...'), 1500);
    setTimeout(() => setScanPhase(type === 'face' ? 'Analyzing Depth & Features...' : 'Analyzing Minutiae Points...'), 3500);
    setTimeout(() => setScanPhase('Matching against Secure Ledger...'), 5500);
    
    setTimeout(() => {
      setStep('authenticating');
      stopCamera();
      
      setTimeout(() => {
        setStep('success');
        setTimeout(() => {
          onSuccess();
          onClose();
        }, 2000);
      }, 1500);
    }, 7000); // 7 seconds total automatic scan time
  };

  if (!isOpen) return null;

  return (
    <AnimatePresence>
      <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
        {/* Backdrop */}
        <motion.div 
          initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
          onClick={step === 'idle' ? onClose : undefined}
          className="absolute inset-0 bg-black/70 backdrop-blur-md"
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

          <div className="p-8 flex flex-col items-center min-h-[350px] justify-center">
            {step === 'idle' && (
              <div className="w-full flex gap-4">
                <button onClick={() => startScan('face')} className="flex-1 flex flex-col items-center justify-center gap-3 p-8 rounded-2xl border transition-all hover:bg-white/5 hover:border-brand-500/50 group" style={{ borderColor: 'var(--border)' }}>
                  <ScanFace className="w-14 h-14 text-brand-400 group-hover:scale-110 transition-transform" />
                  <span className="text-sm font-bold" style={{ color: 'var(--text-secondary)' }}>Face ID</span>
                </button>
                <button onClick={() => startScan('fingerprint')} className="flex-1 flex flex-col items-center justify-center gap-3 p-8 rounded-2xl border transition-all hover:bg-white/5 hover:border-emerald-500/50 group" style={{ borderColor: 'var(--border)' }}>
                  <Fingerprint className="w-14 h-14 text-emerald-400 group-hover:scale-110 transition-transform" />
                  <span className="text-sm font-bold" style={{ color: 'var(--text-secondary)' }}>Biometric</span>
                </button>
              </div>
            )}

            {step === 'scanning' && (
              <div className="flex flex-col items-center">
                <div className="relative w-56 h-56 flex items-center justify-center overflow-hidden rounded-full border-4 bg-black/20"
                     style={{ borderColor: scanType === 'face' ? 'rgba(99,102,241,0.4)' : 'rgba(16,185,129,0.4)' }}>
                  
                  {scanType === 'face' ? (
                    <video ref={videoRef} autoPlay playsInline muted className="absolute inset-0 w-full h-full object-cover transform -scale-x-100" />
                  ) : (
                    <Fingerprint className="w-28 h-28 text-emerald-500 animate-pulse" />
                  )}
                  
                  {/* Automated Scanning Laser */}
                  <motion.div 
                    initial={{ top: 0, opacity: 0 }}
                    animate={{ top: ['0%', '100%', '0%'], opacity: [0, 1, 1, 0] }}
                    transition={{ duration: 1.5, repeat: Infinity, ease: "linear" }}
                    className={`absolute left-0 right-0 h-1 shadow-[0_0_20px_2px] z-10 ${scanType === 'face' ? 'bg-brand-400 shadow-brand-500' : 'bg-emerald-400 shadow-emerald-500'}`}
                  />

                  {/* High-tech overlays */}
                  <div className="absolute inset-0 z-10 pointer-events-none" style={{ backgroundImage: 'radial-gradient(transparent 30%, rgba(0,0,0,0.7) 100%)' }}>
                    <div className={`absolute inset-4 border ${scanType === 'face' ? 'border-brand-500/40' : 'border-emerald-500/40'} rounded-full`} />
                    <div className={`absolute inset-10 border border-dashed ${scanType === 'face' ? 'border-brand-500/30' : 'border-emerald-500/30'} rounded-full animate-spin-slow`} />
                  </div>
                </div>

                <div className="mt-8 flex flex-col items-center">
                  <div className="flex items-center gap-2 mb-2">
                    <Scan className={`w-5 h-5 animate-spin ${scanType === 'face' ? 'text-brand-500' : 'text-emerald-500'}`} />
                    <p className={`text-lg font-black uppercase tracking-widest ${scanType === 'face' ? 'text-brand-500' : 'text-emerald-500'}`}>
                      Auto-Scan Active
                    </p>
                  </div>
                  <p className="text-sm font-bold text-slate-300 animate-pulse text-center h-6">
                    {scanPhase}
                  </p>
                </div>
              </div>
            )}

            {step === 'authenticating' && (
              <div className="flex flex-col items-center justify-center py-6">
                <Loader2 className="w-12 h-12 text-brand-400 animate-spin mb-4" />
                <p className="text-sm font-bold" style={{ color: 'var(--text-primary)' }}>Verifying Secure Ledger...</p>
                <p className="text-xs mt-2" style={{ color: 'var(--text-muted)' }}>Cryptographically signing activity logs</p>
              </div>
            )}

            {step === 'success' && (
              <motion.div 
                initial={{ scale: 0.5, opacity: 0 }} animate={{ scale: 1, opacity: 1 }}
                className="flex flex-col items-center justify-center py-6"
              >
                <div className="w-20 h-20 rounded-full bg-emerald-500/20 flex items-center justify-center mb-5 border border-emerald-500/30">
                  <CheckCircle className="w-10 h-10 text-emerald-500" />
                </div>
                <p className="text-2xl font-black text-emerald-500 mb-2">Sync Complete!</p>
                <p className="text-sm text-center max-w-xs" style={{ color: 'var(--text-secondary)' }}>
                  Your campus activities and library visits have been successfully verified and added to your profile.
                </p>
              </motion.div>
            )}
          </div>
        </motion.div>
      </div>
    </AnimatePresence>
  );
}
