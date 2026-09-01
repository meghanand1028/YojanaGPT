import React, { useState, useEffect, useRef } from 'react';
import Sidebar from './Sidebar';
import InputDock from './InputDock';
import axios from 'axios';
import { Bot, User, Menu, RotateCcw, Volume2, VolumeX } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';

const API_BASE = (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') && window.location.port === '5173'
  ? 'http://127.0.0.1:10000' 
  : '';

function App() {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [history, setHistory] = useState([]);
  const [isTyping, setIsTyping] = useState(false);
  const [enableAudio, setEnableAudio] = useState(false);
  const viewportRef = useRef(null);

  useEffect(() => {
    axios.get(`${API_BASE}/history`, { withCredentials: true })
      .then(res => {
        if (res.data.success && res.data.history) {
          setHistory(res.data.history.slice(-10).reverse());
        }
      }).catch(err => console.log('No auth or error', err));
  }, []);

  useEffect(() => {
    if (viewportRef.current) {
      viewportRef.current.scrollTop = viewportRef.current.scrollHeight;
    }
  }, [messages, isTyping]);

  const startNewChat = () => setMessages([]);

  const submitQuery = async (queryText) => {
    if (!queryText.trim()) return;
    
    const userMsg = { content: queryText, sender: 'user', time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) };
    setMessages(prev => [...prev, userMsg]);
    setIsTyping(true);

    try {
      const res = await axios.post(`${API_BASE}/ask`, { message: queryText }, { headers: { 'Content-Type': 'application/json' }, withCredentials: true });
      setIsTyping(false);
      const botMsg = { 
        content: res.data.reply || 'Sorry, I could not process your query at this moment.', 
        sender: 'bot', 
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) 
      };
      setMessages(prev => [...prev, botMsg]);
      setHistory(prev => [{ user_message: queryText }, ...prev].slice(0, 10));
    } catch (err) {
      setIsTyping(false);
      setMessages(prev => [...prev, { content: 'Network error.', sender: 'bot', time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) }]);
    }
  };

  return (
    <div className="flex h-screen w-full bg-background text-foreground overflow-hidden font-sans">
      <Sidebar 
        sidebarOpen={sidebarOpen} 
        setSidebarOpen={setSidebarOpen} 
        startNewChat={startNewChat} 
        history={history} 
        submitQuery={submitQuery} 
      />

      <main className="flex-1 flex flex-col h-full relative">
        <header className="flex items-center justify-between px-6 py-4 border-b border-border bg-background z-20">
            <div className="flex items-center gap-4">
                <Button variant="ghost" size="icon" className="md:hidden" onClick={() => setSidebarOpen(true)}>
                  <Menu className="w-5 h-5" />
                </Button>
                <div className="flex items-center gap-3">
                    <div className="w-10 h-10 rounded-lg bg-primary text-primary-foreground flex items-center justify-center shadow-md">
                      <Bot size={22} />
                    </div>
                    <div>
                        <h3 className="font-semibold text-sm tracking-tight">YojanaGPT</h3>
                        <p className="text-xs text-muted-foreground flex items-center gap-1">
                          <span className="w-2 h-2 rounded-full bg-green-500"></span> Ready
                        </p>
                    </div>
                </div>
            </div>

            <div className="flex items-center gap-2">
                <Button variant={enableAudio ? "secondary" : "ghost"} size="icon" onClick={() => setEnableAudio(!enableAudio)}>
                  {enableAudio ? <Volume2 className="w-4 h-4" /> : <VolumeX className="w-4 h-4 text-muted-foreground" />}
                </Button>
                <Button variant="ghost" size="icon" onClick={startNewChat}>
                  <RotateCcw className="w-4 h-4 text-muted-foreground" />
                </Button>
            </div>
        </header>

        <div className="flex-1 overflow-y-auto p-4 md:p-8 flex flex-col gap-6" ref={viewportRef}>
          {messages.length === 0 ? (
            <div className="flex flex-col items-center justify-center h-full max-w-2xl mx-auto text-center space-y-8">
                <div className="w-20 h-20 bg-primary text-primary-foreground rounded-2xl flex items-center justify-center shadow-lg">
                  <Bot size={40} />
                </div>
                <div className="space-y-2">
                  <h2 className="text-3xl font-bold tracking-tight">How can I help you today?</h2>
                  <p className="text-muted-foreground">Search across Indian government schemes and eligibility criteria.</p>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 w-full mt-8">
                    {['PM-Kisan Yojana benefits?', 'Ayushman Bharat application?', 'PM Awas Yojana subsidies?', 'Student scholarships available?'].map((q, i) => (
                      <Card key={i} onClick={() => submitQuery(q)} className="p-4 cursor-pointer hover:border-primary transition-colors hover:bg-muted/50">
                        <p className="text-sm font-medium">{q}</p>
                      </Card>
                    ))}
                </div>
            </div>
          ) : (
            messages.map((msg, i) => (
              <div key={i} className={`flex gap-4 max-w-[85%] ${msg.sender === 'user' ? 'ml-auto flex-row-reverse' : ''}`}>
                  <div className={`w-8 h-8 flex-shrink-0 rounded-md flex items-center justify-center ${msg.sender === 'user' ? 'bg-secondary text-secondary-foreground' : 'bg-primary text-primary-foreground'}`}>
                      {msg.sender === 'user' ? <User size={16} /> : <Bot size={16} />}
                  </div>
                  <div className={`flex flex-col gap-1 ${msg.sender === 'user' ? 'items-end' : 'items-start'}`}>
                      <div className={`px-4 py-3 text-sm leading-relaxed rounded-2xl ${msg.sender === 'user' ? 'bg-primary text-primary-foreground rounded-tr-sm' : 'bg-muted text-foreground border border-border rounded-tl-sm'}`}>
                          {msg.content}
                      </div>
                      <span className="text-[10px] text-muted-foreground font-medium px-1">{msg.time}</span>
                  </div>
              </div>
            ))
          )}

          {isTyping && (
             <div className="flex gap-4 max-w-[85%]">
                 <div className="w-8 h-8 rounded-md bg-primary text-primary-foreground flex items-center justify-center"><Bot size={16}/></div>
                 <div className="bg-muted border border-border rounded-2xl rounded-tl-sm px-4 py-4 flex items-center gap-1.5">
                     <div className="w-1.5 h-1.5 bg-foreground/50 rounded-full animate-bounce" style={{animationDelay: '0ms'}}></div>
                     <div className="w-1.5 h-1.5 bg-foreground/50 rounded-full animate-bounce" style={{animationDelay: '150ms'}}></div>
                     <div className="w-1.5 h-1.5 bg-foreground/50 rounded-full animate-bounce" style={{animationDelay: '300ms'}}></div>
                 </div>
             </div>
          )}
        </div>

        <InputDock submitQuery={submitQuery} />
      </main>
    </div>
  );
}

export default App;
