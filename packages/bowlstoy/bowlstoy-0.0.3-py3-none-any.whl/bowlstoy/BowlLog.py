import locale
import sys
import os
import re
import time

class Log():
    def __init__(self, out=None, encoding = None, bAddStamp = False):
        self.out = out or sys.stderr
        if not self.out:
            return
        
        enc = None
        prefEncoding = self.__preferredencoding()
        # `mode` might be `None` (Ref: https://github.com/yt-dlp/yt-dlp/issues/8816)
        if 'b' in (getattr(out, 'mode', None) or ''):
            enc = encoding or prefEncoding
        elif hasattr(out, 'buffer'):
            enc = encoding or getattr(out, 'encoding', None) or prefEncoding

        self.buffer = self.out
        if hasattr(out, "buffer"):
            self.buffer = out.buffer            

        self.encoding = enc
        self.bAddStamp = bAddStamp
        self.bSupportTerminalSequences = self.__supports_terminal_sequences(out)
    
    def __supports_terminal_sequences(self, stream):
        if os.name != 'nt':
            return False
        elif not os.getenv('TERM'):
            return False
        try:
            return stream.isatty()
        except BaseException:
            return False
        
    def __preferredencoding(self):
        """Get preferred encoding.

        Returns the best encoding scheme for the system, based on
        locale.getpreferredencoding() and some further tweaks.
        """
        try:
            pref = locale.getpreferredencoding()
            'TEST'.encode(pref)
        except Exception:
            pref = 'UTF-8'

        return pref
    
    def _GetTimeStamp(self):
        return time.strftime('[%Y.%m.%d-%H.%M.%S]', time.localtime(time.time()))
    
    def Debug(self, s):
        self._OutputString(s, "D")

    def Warning(self, s):
        self._OutputString(s, "W")

    def Error(self, s):
        self._OutputString(s, "E")


    def _OutputString(self, s, typeStr):
        assert isinstance(s, str)
        # `sys.stderr` might be `None` (Ref: https://github.com/pyinstaller/pyinstaller/pull/7217)
        if not self.out:
            return

        if self.bAddStamp:
            s = f"{self._GetTimeStamp()}[{typeStr}]{s}"
        
        s += "\n"
            
        if self.bSupportTerminalSequences:
            s = re.sub(r'([\r\n]+)', r' \1', s)

        self.buffer.write(s.encode(self.encoding, 'ignore') if self.encoding else s)
        self.out.flush()