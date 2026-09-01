import React, { useState } from 'react';
import { Mic, SendHorizontal } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';

function InputDock({ submitQuery }) {
  const [input, setInput] = useState('');
  const [isRecording, setIsRecording] = useState(false);
  const [recognition, setRecognition] = useState(null);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (input.trim()) {
      submitQuery(input);
      setInput('');
    }
  };

  const toggleVoiceInput = () => {
    if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) return;
    if (isRecording && recognition) {
        recognition.stop();
        return;
    }
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const newRec = new SpeechRecognition();
    newRec.continuous = false;
    newRec.lang = 'en-IN';
    newRec.onstart = () => setIsRecording(true);
    newRec.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        setInput(transcript);
        submitQuery(transcript);
    };
    newRec.onerror = () => setIsRecording(false);
    newRec.onend = () => setIsRecording(false);
    newRec.start();
    setRecognition(newRec);
  };

  return (
    <div className="p-4 max-w-4xl mx-auto w-full">
        <form onSubmit={handleSubmit} className="relative flex items-center bg-card border border-border shadow-sm rounded-full px-2 py-2">
            <Button 
              type="button"
              variant="ghost" 
              size="icon" 
              className={`rounded-full flex-shrink-0 ${isRecording ? 'text-destructive bg-destructive/10 animate-pulse' : 'text-muted-foreground'}`}
              onClick={toggleVoiceInput}
            >
                <Mic size={18} />
            </Button>
            <Input 
              className="flex-1 border-0 focus-visible:ring-0 bg-transparent text-foreground placeholder:text-muted-foreground text-sm px-4 h-10 shadow-none"
              placeholder="Ask anything about government schemes..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
            />
            <Button type="submit" size="icon" className="rounded-full bg-primary text-primary-foreground flex-shrink-0 w-10 h-10 hover:bg-primary/90">
                <SendHorizontal size={18} />
            </Button>
        </form>
        <p className="text-center text-[10px] text-muted-foreground mt-3 font-medium uppercase tracking-wider">
            YojanaGPT uses AI. Verify critical information.
        </p>
    </div>
  );
}

export default InputDock;
