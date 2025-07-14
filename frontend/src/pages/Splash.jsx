import React from 'react';

export default function Splash() {
  return (
    <div className="splash-wrapper min-h-screen w-full flex items-center justify-center fade-in-out overflow-hidden">
      <img
        src="/logo.png"
        alt="PulseTracker Splash"
        className="w-[320px] rounded-xl shadow-md object-contain"
      />
    </div>
  );
}
