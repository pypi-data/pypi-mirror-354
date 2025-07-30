#!/usr/bin/env python3
import sys, time, signal, subprocess, urllib.request, json, logging, os, threading, psutil, traceback
from importlib import metadata
from packaging.version import parse as parse_version
from datetime import datetime, timedelta

# Configuration
CHECK_INTERVAL = 60*60         # Check for updates every hour
HEALTH_CHECK_INTERVAL = 30     # Check process health every 30 seconds
RESTART_DELAY = 5              # Wait 5 seconds before restarting after crash
MAX_RESTART_ATTEMPTS = 5       # Maximum restart attempts within window
RESTART_WINDOW = 300           # 5 minute window for restart attempts
PYPI_JSON_URL = "https://pypi.org/pypi/lightscope/json"
LOG_FILE = os.path.expanduser("~/lightscope_monitor.log")

# Setup comprehensive logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class RestartTracker:
    """Track restart attempts to prevent restart loops"""
    def __init__(self):
        self.attempts = []
        self.max_attempts = MAX_RESTART_ATTEMPTS
        self.window = timedelta(seconds=RESTART_WINDOW)
    
    def can_restart(self):
        """Check if we can safely restart (not too many recent attempts)"""
        now = datetime.now()
        # Remove old attempts outside the window
        self.attempts = [t for t in self.attempts if now - t < self.window]
        
        if len(self.attempts) >= self.max_attempts:
            logger.error(f"Too many restart attempts ({len(self.attempts)}) within {RESTART_WINDOW}s window. Refusing to restart.")
            return False
        return True
    
    def record_restart(self):
        """Record a restart attempt"""
        self.attempts.append(datetime.now())
        logger.info(f"Restart attempt recorded. Total attempts in window: {len(self.attempts)}/{self.max_attempts}")

def get_installed_version():
    """Get the currently installed LightScope version"""
    try:
        version = metadata.version("lightscope")
        logger.debug(f"Installed version: {version}")
        return version
    except metadata.PackageNotFoundError:
        logger.warning("LightScope not found in installed packages")
        return None
    except Exception as e:
        logger.error(f"Error getting installed version: {e}")
        return None

def get_latest_version():
    """Get the latest version from PyPI with retry logic"""
    max_retries = 3
    for attempt in range(max_retries):
        try:
            logger.debug(f"Checking PyPI for latest version (attempt {attempt + 1}/{max_retries})")
            with urllib.request.urlopen(PYPI_JSON_URL, timeout=30) as r:
                data = json.load(r)
                version = data["info"]["version"]
                logger.debug(f"Latest version on PyPI: {version}")
                return version
        except urllib.request.URLError as e:
            logger.warning(f"Network error checking PyPI (attempt {attempt + 1}): {e}")
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON response from PyPI: {e}")
        except Exception as e:
            logger.error(f"Unexpected error checking PyPI: {e}")
        
        if attempt < max_retries - 1:
            time.sleep(5 * (attempt + 1))  # Exponential backoff
    
    logger.error(f"Failed to get latest version after {max_retries} attempts")
    return None

def install_or_upgrade():
    """Install or upgrade LightScope with comprehensive error handling"""
    max_retries = 3
    for attempt in range(max_retries):
        try:
            logger.info(f"Installing/upgrading LightScope (attempt {attempt + 1}/{max_retries})")
            cmd = [sys.executable, "-m", "pip", "install", "--upgrade", "lightscope"]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            if result.returncode == 0:
                logger.info("LightScope installation/upgrade successful")
                logger.debug(f"Pip output: {result.stdout}")
                return True
            else:
                logger.error(f"Pip failed with return code {result.returncode}")
                logger.error(f"Pip stderr: {result.stderr}")
                
        except subprocess.TimeoutExpired:
            logger.error(f"Installation timeout (attempt {attempt + 1})")
        except Exception as e:
            logger.error(f"Installation error (attempt {attempt + 1}): {e}")
        
        if attempt < max_retries - 1:
            time.sleep(10 * (attempt + 1))  # Exponential backoff
    
    logger.error(f"Failed to install/upgrade after {max_retries} attempts")
    return False

def spawn_app():
    """Spawn the LightScope application with enhanced monitoring"""
    try:
        logger.info("Starting LightScope application")
        # Run with environment variables for better debugging
        env = os.environ.copy()
        env['PYTHONUNBUFFERED'] = '1'  # Force unbuffered output
        
        proc = subprocess.Popen(
            [sys.executable, "-m", "lightscope"],
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1  # Line buffered
        )
        
        logger.info(f"LightScope started with PID: {proc.pid}")
        return proc
        
    except Exception as e:
        logger.error(f"Failed to start LightScope: {e}")
        return None

def is_process_healthy(proc):
    """Check if the process is still running and healthy"""
    if proc is None:
        return False
    
    try:
        # Check if process is still running
        if proc.poll() is not None:
            logger.warning(f"Process {proc.pid} has terminated with code {proc.returncode}")
            return False
        
        # Check if we can get process info (process exists and accessible)
        psutil_proc = psutil.Process(proc.pid)
        if not psutil_proc.is_running():
            logger.warning(f"Process {proc.pid} is not running according to psutil")
            return False
            
        # Check CPU usage (if 0% for too long, might be frozen)
        cpu_percent = psutil_proc.cpu_percent()
        logger.debug(f"Process {proc.pid} CPU usage: {cpu_percent}%")
        
        return True
        
    except psutil.NoSuchProcess:
        logger.warning(f"Process {proc.pid} no longer exists")
        return False
    except psutil.AccessDenied:
        logger.warning(f"Access denied checking process {proc.pid}")
        return True  # Assume healthy if we can't check
    except Exception as e:
        logger.error(f"Error checking process health: {e}")
        return True  # Assume healthy if we can't check

def graceful_shutdown(proc, timeout=30):
    """Gracefully shutdown the process with comprehensive cleanup"""
    if proc is None:
        return
    
    try:
        pid = proc.pid
        logger.info(f"Shutting down process {pid} gracefully")
        
        # Try SIGTERM first
        proc.send_signal(signal.SIGTERM)
        
        try:
            proc.wait(timeout=timeout)
            logger.info(f"Process {pid} terminated gracefully")
        except subprocess.TimeoutExpired:
            logger.warning(f"Process {pid} didn't respond to SIGTERM, using SIGKILL")
            proc.kill()
            proc.wait(timeout=10)
            logger.info(f"Process {pid} killed forcefully")
            
    except ProcessLookupError:
        logger.info("Process already terminated")
    except Exception as e:
        logger.error(f"Error during shutdown: {e}")
        try:
            proc.kill()
            proc.wait()
        except:
            pass

def output_reader(proc):
    """Read and log output from the subprocess"""
    try:
        for line in proc.stdout:
            line = line.strip()
            if line:
                # Log LightScope output to our log file
                logger.info(f"[LightScope] {line}")
    except Exception as e:
        logger.error(f"Error reading process output: {e}")

def main():
    """Main monitoring loop with bulletproof error handling"""
    logger.info("=" * 60)
    logger.info("LightScope Monitor Starting")
    logger.info(f"Log file: {LOG_FILE}")
    logger.info("=" * 60)
    
    restart_tracker = RestartTracker()
    
    # Initial installation check
    v0 = get_installed_version()
    if not v0:
        logger.info("LightScope not installed, installing now...")
        if not install_or_upgrade():
            logger.error("Initial installation failed")
            sys.exit(1)
        
        v0 = get_installed_version()
        if not v0:
            logger.error("Installation appeared to succeed but version still not detected")
            sys.exit(1)
    
    logger.info(f"Starting monitoring with LightScope version {v0}")
    
    proc = None
    last_update_check = 0
    last_health_check = 0
    output_thread = None
    
    try:
        while True:
            current_time = time.time()
            
            # Health check
            if current_time - last_health_check >= HEALTH_CHECK_INTERVAL:
                if not is_process_healthy(proc):
                    logger.warning("Process health check failed")
                    
                    # Clean up old process
                    if proc:
                        graceful_shutdown(proc)
                        if output_thread and output_thread.is_alive():
                            output_thread.join(timeout=5)
                    
                    # Restart if allowed
                    if restart_tracker.can_restart():
                        restart_tracker.record_restart()
                        logger.info(f"Restarting LightScope after crash (delay: {RESTART_DELAY}s)")
                        time.sleep(RESTART_DELAY)
                        
                        proc = spawn_app()
                        if proc:
                            # Start output reader thread
                            output_thread = threading.Thread(target=output_reader, args=(proc,), daemon=True)
                            output_thread.start()
                        else:
                            logger.error("Failed to restart LightScope")
                    else:
                        logger.critical("Too many restart attempts, giving up")
                        break
                
                last_health_check = current_time
            
            # Update check
            if current_time - last_update_check >= CHECK_INTERVAL:
                logger.info("Checking for updates...")
                latest = get_latest_version()
                
                if latest and v0 and parse_version(latest) > parse_version(v0):
                    logger.info(f"Update available: {v0} -> {latest}")
                    
                    # Shutdown current process
                    if proc:
                        graceful_shutdown(proc)
                        if output_thread and output_thread.is_alive():
                            output_thread.join(timeout=10)
                    
                    # Update
                    if install_or_upgrade():
                        new_version = get_installed_version()
                        if new_version:
                            v0 = new_version
                            logger.info(f"Updated to version {v0}")
                        
                        # Restart with new version
                        proc = spawn_app()
                        if proc:
                            output_thread = threading.Thread(target=output_reader, args=(proc,), daemon=True)
                            output_thread.start()
                    else:
                        logger.error("Update failed, restarting with current version")
                        proc = spawn_app()
                        if proc:
                            output_thread = threading.Thread(target=output_reader, args=(proc,), daemon=True)
                            output_thread.start()
                else:
                    logger.debug(f"No update needed (current: {v0}, latest: {latest})")
                
                last_update_check = current_time
            
            # Start process if it's not running
            if not proc:
                if restart_tracker.can_restart():
                    restart_tracker.record_restart()
                    proc = spawn_app()
                    if proc:
                        output_thread = threading.Thread(target=output_reader, args=(proc,), daemon=True)
                        output_thread.start()
            
            time.sleep(1)
            
    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt, shutting down...")
    except Exception as e:
        logger.error(f"Unexpected error in main loop: {e}")
        logger.error(traceback.format_exc())
    finally:
        logger.info("Cleaning up...")
        if proc:
            graceful_shutdown(proc, timeout=60)
        if output_thread and output_thread.is_alive():
            output_thread.join(timeout=10)
        logger.info("LightScope Monitor stopped")

if __name__ == "__main__":
    main()

