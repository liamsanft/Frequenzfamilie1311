from __future__ import annotations

# Runs once when the project loads: manual control, window in Perform Mode.
# Delayed so Embody has finished restoring the network before the mode changes.
_START_DELAY_FRAMES = 120


def onStart() -> None:
    run('args[0].module.enterPerformManual()', me, delayFrames=_START_DELAY_FRAMES)


def enterPerformManual() -> None:
    """Select the manual control mode and switch TouchDesigner into Perform Mode."""
    project = parent.Project
    if project.par.Mode.eval() != 'manual':
        project.par.Mode = 'manual'
    ui.performMode = True
