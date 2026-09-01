import React from 'react';
import { Plus, MessageSquare, X, Landmark } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Link } from 'react-router-dom';

function Sidebar({ sidebarOpen, setSidebarOpen, startNewChat, history, submitQuery }) {
  return (
    <aside className={`fixed inset-y-0 left-0 z-50 w-72 bg-card border-r border-border flex flex-col transition-transform duration-300 md:relative md:translate-x-0 ${sidebarOpen ? 'translate-x-0' : '-translate-x-full'}`}>
        <div className="flex items-center justify-between p-6 border-b border-border">
            <div className="flex items-center gap-3">
                <div className="w-8 h-8 bg-primary text-primary-foreground rounded-md flex items-center justify-center">
                    <Landmark size={18} />
                </div>
                <span className="font-bold tracking-tight">YojanaGPT</span>
            </div>
            <Button variant="ghost" size="icon" className="md:hidden" onClick={() => setSidebarOpen(false)}>
                <X size={18} />
            </Button>
        </div>

        <div className="p-4">
            <Button className="w-full justify-start gap-2 bg-primary text-primary-foreground hover:bg-primary/90" onClick={startNewChat}>
                <Plus size={16} /> New Chat
            </Button>
        </div>

        <div className="flex-1 overflow-y-auto p-4 pt-0 space-y-2">
            <h4 className="text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-4 px-2">History</h4>
            {history.length === 0 && <p className="text-xs text-muted-foreground px-2">No recent searches</p>}
            {history.map((item, idx) => (
                <button 
                  key={idx} 
                  className="w-full flex items-center gap-3 px-3 py-2 text-sm text-muted-foreground hover:bg-muted hover:text-foreground rounded-md transition-colors text-left"
                  onClick={() => submitQuery(item.user_message)}
                >
                    <MessageSquare size={14} className="flex-shrink-0" />
                    <span className="truncate">{item.user_message}</span>
                </button>
            ))}
        </div>

        <div className="p-4 border-t border-border mt-auto">
            <div className="flex items-center justify-between bg-muted/50 p-3 rounded-lg">
                <div className="flex items-center gap-3">
                    <div className="w-8 h-8 rounded-full bg-secondary text-secondary-foreground flex items-center justify-center text-xs font-bold">
                        U
                    </div>
                    <span className="text-sm font-medium">Guest User</span>
                </div>
                <Link to="/login" className="text-xs text-primary font-medium hover:underline">Sign In</Link>
            </div>
        </div>
    </aside>
  );
}

export default Sidebar;
