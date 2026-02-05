import React, { useState } from 'react';
import { MessageCircle } from 'lucide-react';

interface ChatbotIconProps {
  onClick: () => void;
}

const ChatbotIcon: React.FC<ChatbotIconProps> = ({ onClick }) => {
  const [isHovered, setIsHovered] = useState(false);

  return (
    <div 
      className={`
        fixed bottom-6 right-6 z-50 
        w-14 h-14 rounded-full flex items-center justify-center
        bg-blue-600 text-white shadow-lg
        cursor-pointer transition-all duration-300
        ${isHovered ? 'bg-blue-700 scale-110' : 'bg-blue-600'}
        hover:shadow-xl
      `}
      onClick={onClick}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
      aria-label="Open chat"
      role="button"
      tabIndex={0}
      onKeyDown={(e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          onClick();
        }
      }}
    >
      <MessageCircle size={24} />
      <span className="sr-only">Open chat</span>
    </div>
  );
};

export default ChatbotIcon;