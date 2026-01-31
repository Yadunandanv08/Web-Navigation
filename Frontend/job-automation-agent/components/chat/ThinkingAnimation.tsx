import React from 'react';

export function ThinkingAnimation() {
  return (
    <div className="flex items-center gap-2 py-4">
      <div className="flex items-center gap-1">
        <div className="w-2 h-2 bg-primary rounded-full dot-bounce" style={{ animationDelay: '0ms' }} />
        <div className="w-2 h-2 bg-primary rounded-full dot-bounce" style={{ animationDelay: '150ms' }} />
        <div className="w-2 h-2 bg-primary rounded-full dot-bounce" style={{ animationDelay: '300ms' }} />
      </div>
      <span className="text-sm text-foreground/60 ml-2">Agent thinking...</span>
    </div>
  );
}
