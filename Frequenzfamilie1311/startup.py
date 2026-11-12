from __future__ import annotations

# Runs once when the project loads: input on OSC, window in Perform Mode.
# Delayed so Embody has finished restoring the network before the mode changes.
_START_DELAY_FRAMES = 120


def onStart() -> None:
    run('args[0].module.enterPerformOnOsc()', me, delayFrames=_START_DELAY_FRAMES)


def enterPerformOnOsc() -> None:
    """Select the OSC input mode and switch TouchDesigner into Perform Mode."""
    project = parent.Project
    if project.par.Mode.eval() != 'osc':
        project.par.Mode = 'osc'
    ui.performMode = True
