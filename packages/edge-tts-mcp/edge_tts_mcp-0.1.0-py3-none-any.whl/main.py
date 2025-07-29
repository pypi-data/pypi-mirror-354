from mcp.server.fastmcp import FastMCP
import os
from datetime import datetime
from typing import List, Dict, Optional
import edge_tts
import asyncio
import nest_asyncio
from mcp.server.fastmcp import FastMCP

nest_asyncio.apply()

_voice_manager: Optional[edge_tts.VoicesManager] = None
_voice_manager_lock = asyncio.Lock()

server = FastMCP("TTS Server")

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

async def _get_voice_manager() -> edge_tts.VoicesManager:
    """Get voice manager instance, thread-safe"""
    global _voice_manager
    if _voice_manager is None:
        async with _voice_manager_lock:
            if _voice_manager is None:  # Double-checked locking
                _voice_manager = await edge_tts.VoicesManager.create()
    return _voice_manager

@server.tool(name="list_voice", description="Get available voice list")
def list_voice() -> List[Dict[str, str]]:
    """
    Get available voice list
    
    Returns:
        Available voice list, each voice contains ShortName, Gender, Locale and other information, ShortName value is used to select appropriate voice parameter
    """
    try:
        voice_manager = asyncio.run(_get_voice_manager())
        return voice_manager.voices
    except Exception as e:
        raise ValueError(f"Failed to get voice list: {str(e)}")

@server.tool(name="tts", description="Convert text to speech and return audio file path")
def tts(text: str, voice: str, srt_enable: bool = False) -> Dict[str, str]:
    """
    Convert text to speech and return audio file and subtitle file paths. Before calling this method, you must first call list_voice to get the available voice list, and select the appropriate voice parameter based on the input text parameter.
    
    Args:
        text: Text to be converted to speech (required)
        voice: Voice name, can be obtained through list_voice, ShortName value (required)
        srt_enable: Whether to generate subtitle file, default is False
    
    Returns:
        Dictionary containing audio file and subtitle file paths
    """
    # Input validation
    if not text or not text.strip():
        raise ValueError("Text content cannot be empty")
    if not voice or not voice.strip():
        raise ValueError("Voice name cannot be empty")
    
    try:
        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"tts_{timestamp}"
        
        # Set output file paths
        mp3_path = os.path.join(OUTPUT_DIR, f"{filename}.mp3")
        srt_path = os.path.join(OUTPUT_DIR, f"{filename}.srt")
        
        # Generate speech using synchronous method
        communicate = edge_tts.Communicate(text, voice)
        
        # If subtitle file generation is needed, initialize SubMaker
        submaker = None
        if srt_enable:
            submaker = edge_tts.SubMaker()
        
        # Generate audio file
        try:
            with open(mp3_path, "wb") as file:
                for chunk in communicate.stream_sync():
                    if chunk["type"] == "audio":
                        file.write(chunk["data"])
                    elif chunk["type"] == "WordBoundary" and submaker:
                        submaker.feed(chunk)
        except Exception as e:
            # If generation fails, clean up possibly created files
            if os.path.exists(mp3_path):
                os.remove(mp3_path)
            raise e
        
        # If subtitle file generation is needed
        if srt_enable and submaker:
            try:
                with open(srt_path, "w", encoding="utf-8") as srt_file:
                    srt_file.write(submaker.get_srt())
            except Exception as e:
                # If subtitle generation fails, clean up audio file
                if os.path.exists(mp3_path):
                    os.remove(mp3_path)
                raise e
        
        result = {"audio_path": mp3_path}
        if srt_enable:
            result["subtitle_path"] = srt_path
            
        return result
    except Exception as e:
        raise ValueError(f"TTS conversion failed: {str(e)}")

# Run server through stdio
if __name__ == "__main__":
    server.run()