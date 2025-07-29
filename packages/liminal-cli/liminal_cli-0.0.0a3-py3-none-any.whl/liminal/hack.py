"""
this seems to be the only way to run a command from python and have atuin record it

subprocess.run(['bash', '-ic', 'mycommand; exit']) doesnt work
	# resp = subprocess.run(['bash', '-ic', f'logger "liminal installed {datetime_utcnow()} {uuid4()}"'])
	resp = subprocess.run(['bash', '-ic', f'eval "$(atuin init bash)"; echo pleaseeee; true; exit 0'], cwd=Path(__file__).parent.parent, env=None)
"""
import os
import pty
import subprocess
import time

from liminal.standalone_install_wrapper import LOGGER



def run_in_pty_shell_minimal(shell_executable, command_to_execute_in_shell) -> bool:
    """
    Minimal version: Runs a command in a new shell instance spawned within a PTY.
    Sends only the target command and relies on PTY closure/shell behavior for exit.
    No explicit debug mode here for brevity.
    """


    # Command to send, newline terminated for execution
    command_with_newline = f"{command_to_execute_in_shell}\n"

    LOGGER.info(f"{shell_executable} -l -c '{command_to_execute_in_shell}'")

    manager_fd, subsidiary_fd = pty.openpty()
    process = None

    try:
        # Start the shell, request interactive mode
        process = subprocess.Popen(
            [shell_executable, "-i"],
            stdin=subsidiary_fd,
            stdout=subsidiary_fd,
            stderr=subsidiary_fd,
            env=os.environ.copy(),
            start_new_session=True, # Good for PTYs to detach from controlling terminal
        )
        os.close(subsidiary_fd) # subsidiary FD is now managed by the child process

        # Brief pause for shell initialization (e.g., sourcing .bashrc)
        # This is a common heuristic. If too short, rc files might not be fully processed.
        # If too long, it adds unnecessary delay. Adjust if needed.
        time.sleep(0.3) # Reduced from 0.5, test what works

        # Write the command to the master end of the PTY
        os.write(manager_fd, command_with_newline.encode())

        # After sending the command, we want the shell to process it and then exit.
        # Closing the manager_fd will send EOF to the shell's stdin,
        # which typically causes an interactive shell to exit.
        # We'll do this after a short delay to allow command processing.
        time.sleep(0.2) # Allow command to be processed before closing master
        os.close(manager_fd)
        manager_fd = -1 # Mark as closed

        # Wait for the process to complete. Set a timeout.
        process.wait(timeout=5) # Adjust timeout as necessary

        if process.returncode > 0:
            # A non-zero return code from the shell might be okay if the command itself
            # had an error but Atuin still logged it. Or it could mean the shell
            # exited abnormally. For a minimal version, we'll just note it.
            LOGGER.warning(f"Info: Shell in PTY (minimal) exited with code {process.returncode}.")

        return True # Assume command execution was attempted

    except subprocess.TimeoutExpired:
        LOGGER.error(f"Error: Shell process in PTY (minimal) timed out.")
        if process:
            process.kill() # Ensure termination
            process.wait() # Wait for kill to complete
        return False
    except Exception as e:
        LOGGER.exception(f"Error running command in PTY shell (minimal): {e}")
        if process and process.poll() is None: # If process is still running
            process.kill()
            process.wait()
        return False
    finally:
        if manager_fd != -1 : # If not already closed (e.g. due to an earlier error)
             try:
                os.close(manager_fd)
             except OSError:
                pass # Ignore if already closed or invalid
        if process and process.poll() is None:
            # This block should ideally not be reached if wait() succeeded or timed out correctly
            LOGGER.warning("Final check (minimal): PTY process did not exit cleanly, attempting kill.")
            process.kill()
            process.wait()
            

if __name__ == '__main__':
    import uuid 
    # run_in_pty_shell('/bin/bash', f'logger "ok {uuid.uuid4()}"')
    run_in_pty_shell_minimal('/bin/bash', f'logger "ok {uuid.uuid4()}"')
