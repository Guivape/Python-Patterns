import sys

class Process:
    """
    Replaces the third-party 'state_machine' decorator approach
    with a dictionary-based state engine.
    Each event references a dict mapping valid (current_state -> next_state).
    We add simple before/after hooks as first-class functions
    for dynamic method assignment.
    """

    # List of possible states
    CREATED = "created"
    WAITING = "waiting"
    RUNNING = "running"
    TERMINATED = "terminated"
    BLOCKED = "blocked"
    SWAPPED_OUT_WAITING = "swapped_out_waiting"
    SWAPPED_OUT_BLOCKED = "swapped_out_blocked"

    # Dict of valid transitions { event: {current_state: next_state} }
    _transitions = {
        "wait": {
            CREATED: WAITING,
            RUNNING: WAITING,
            BLOCKED: WAITING,
            SWAPPED_OUT_WAITING: WAITING
        },
        "run": {
            WAITING: RUNNING
        },
        "terminate": {
            RUNNING: TERMINATED
        },
        "block": {
            RUNNING: BLOCKED,
            SWAPPED_OUT_BLOCKED: BLOCKED
        },
        "swap_wait": {
            WAITING: SWAPPED_OUT_WAITING
        },
        "swap_block": {
            BLOCKED: SWAPPED_OUT_BLOCKED
        }
    }

    # Optional hooks
    _before_hooks = {
        "terminate": lambda self: print(f"{self.name} terminated (before hook)")
    }
    _after_hooks = {
        "wait": lambda self: print(f"{self.name} entered waiting mode (after hook)"),
        "run": lambda self: print(f"{self.name} is running (after hook)"),
        "block": lambda self: print(f"{self.name} is blocked (after hook)"),
        "swap_wait": lambda self: print(f"{self.name} is swapped out and waiting (after hook)"),
        "swap_block": lambda self: print(f"{self.name} is swapped out and blocked (after hook)")
    }

    def __init__(self, name):
        self.name = name
        self.current_state = Process.CREATED

    def do_event(self, event_name):
        # optional 'before' hook
        if event_name in self._before_hooks:
            self._before_hooks[event_name](self)

        valid_map = self._transitions.get(event_name, {})
        next_state = valid_map.get(self.current_state)
        if next_state is None:
            print(f"Error: {self.name} cannot do '{event_name}' from {self.current_state}")
            return

        self.current_state = next_state

        # optional 'after' hook
        if event_name in self._after_hooks:
            self._after_hooks[event_name](self)

def transition(proc, event_name):
    proc.do_event(event_name)

def state_info(proc):
    print(f"state of {proc.name}: {proc.current_state}")

def main():
    p1 = Process("process1")
    p2 = Process("process2")

    for p in (p1, p2):
        state_info(p)
    print()

    transition(p1, "wait")
    transition(p2, "terminate")
    for p in (p1, p2):
        state_info(p)
    print()

    transition(p1, "run")
    transition(p2, "wait")
    for p in (p1, p2):
        state_info(p)
    print()

    transition(p2, "run")
    for p in (p1, p2):
        state_info(p)
    print()

    for p in (p1, p2):
        transition(p, "block")
    for p in (p1, p2):
        state_info(p)
    print()

    for p in (p1, p2):
        transition(p, "terminate")
    for p in (p1, p2):
        state_info(p)

if __name__ == "__main__":
    sys.exit(main())
