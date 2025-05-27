#!/usr/bin/env python3
"""
Screen recorder module for the Pygame Arcade Launcher.
Allows recording gameplay sessions to video files.
Uses pygame's built-in capabilities to avoid external dependencies.
"""
import pygame
import os
import time
import datetime
import threading
import queue

class GameRecorder:
    """Records gameplay to a series of screenshots."""
    
    def __init__(self, output_dir=None):
        """Initialize the recorder."""
        # Set up output directory
        if output_dir is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            self.output_dir = os.path.join(base_dir, 'recordings')
        else:
            self.output_dir = output_dir
            
        # Create output directory if it doesn't exist
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            
        # Initialize recording state
        self.recording = False
        self.paused = False
        self.frame_queue = queue.Queue()
        self.writer_thread = None
        self.fps = 30
        self.last_frame_time = 0
        self.frame_interval = 1.0 / self.fps
        self.frame_count = 0
        self.session_dir = None
        
    def start_recording(self, width, height):
        """Start recording gameplay."""
        if self.recording:
            return
            
        # Generate output directory with timestamp
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        self.session_dir = os.path.join(self.output_dir, f"gameplay_{timestamp}")
        
        if not os.path.exists(self.session_dir):
            os.makedirs(self.session_dir)
        
        # Start writer thread
        self.recording = True
        self.paused = False
        self.frame_count = 0
        self.writer_thread = threading.Thread(target=self._process_frames)
        self.writer_thread.daemon = True
        self.writer_thread.start()
        
        print(f"Recording started: {self.session_dir}")
        return self.session_dir
        
    def stop_recording(self):
        """Stop recording gameplay."""
        if not self.recording:
            return
            
        # Stop recording
        self.recording = False
        
        # Wait for writer thread to finish
        if self.writer_thread:
            self.writer_thread.join()
            
        print(f"Recording stopped. {self.frame_count} frames saved to {self.session_dir}")
        
        # Create a simple HTML viewer for the frames
        self._create_html_viewer()
        
    def toggle_pause(self):
        """Pause or resume recording."""
        if not self.recording:
            return
            
        self.paused = not self.paused
        print(f"Recording {'paused' if self.paused else 'resumed'}")
        
    def capture_frame(self, surface):
        """Capture a frame from the pygame surface."""
        if not self.recording or self.paused:
            return
            
        # Check if it's time to capture a new frame
        current_time = time.time()
        if current_time - self.last_frame_time < self.frame_interval:
            return
            
        self.last_frame_time = current_time
        
        # Add frame to queue
        self.frame_queue.put(surface.copy())
        
    def _process_frames(self):
        """Process frames in the background."""
        while self.recording or not self.frame_queue.empty():
            try:
                # Get frame from queue with timeout
                frame = self.frame_queue.get(timeout=1.0)
                
                # Save frame as PNG
                frame_filename = os.path.join(self.session_dir, f"frame_{self.frame_count:06d}.png")
                pygame.image.save(frame, frame_filename)
                
                # Increment frame counter
                self.frame_count += 1
                
                # Mark task as done
                self.frame_queue.task_done()
                
            except queue.Empty:
                # No frames in queue, continue waiting
                continue
                
        print("Frame processing complete")
    
    def _create_html_viewer(self):
        """Create a simple HTML viewer for the recorded frames."""
        if not self.session_dir or self.frame_count == 0:
            return
            
        html_path = os.path.join(self.session_dir, "viewer.html")
        
        with open(html_path, 'w') as f:
            f.write(f"""<!DOCTYPE html>
<html>
<head>
    <title>Gameplay Recording Viewer</title>
    <style>
        body {{ font-family: Arial, sans-serif; text-align: center; background-color: #222; color: white; }}
        .controls {{ margin: 20px; }}
        button {{ padding: 10px; margin: 5px; background-color: #444; color: white; border: none; cursor: pointer; }}
        button:hover {{ background-color: #666; }}
        #frame {{ max-width: 100%; border: 2px solid #444; }}
        .slider-container {{ width: 80%; margin: 20px auto; }}
        #frameSlider {{ width: 100%; }}
    </style>
</head>
<body>
    <h1>Gameplay Recording Viewer</h1>
    <div class="controls">
        <button id="playButton">Play</button>
        <button id="pauseButton">Pause</button>
        <span id="frameCounter">Frame: 0 / {self.frame_count}</span>
    </div>
    <div class="slider-container">
        <input type="range" min="0" max="{self.frame_count - 1}" value="0" id="frameSlider">
    </div>
    <div>
        <img id="frame" src="frame_000000.png" alt="Frame">
    </div>

    <script>
        const totalFrames = {self.frame_count};
        let currentFrame = 0;
        let isPlaying = false;
        let playInterval;
        const fps = {self.fps};
        
        const frameImg = document.getElementById('frame');
        const frameCounter = document.getElementById('frameCounter');
        const frameSlider = document.getElementById('frameSlider');
        
        function updateFrame() {{
            const frameNum = currentFrame.toString().padStart(6, '0');
            frameImg.src = `frame_${{frameNum}}.png`;
            frameCounter.textContent = `Frame: ${{currentFrame}} / ${{totalFrames - 1}}`;
            frameSlider.value = currentFrame;
        }}
        
        function nextFrame() {{
            currentFrame = (currentFrame + 1) % totalFrames;
            updateFrame();
        }}
        
        document.getElementById('playButton').addEventListener('click', () => {{
            if (!isPlaying) {{
                isPlaying = true;
                playInterval = setInterval(nextFrame, 1000 / fps);
            }}
        }});
        
        document.getElementById('pauseButton').addEventListener('click', () => {{
            isPlaying = false;
            clearInterval(playInterval);
        }});
        
        frameSlider.addEventListener('input', () => {{
            currentFrame = parseInt(frameSlider.value);
            updateFrame();
            if (isPlaying) {{
                isPlaying = false;
                clearInterval(playInterval);
            }}
        }});
        
        updateFrame();
    </script>
</body>
</html>
""")
        
        print(f"HTML viewer created: {html_path}")
