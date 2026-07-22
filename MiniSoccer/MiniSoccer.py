# MiniSoccer launcher.
# The game itself is precompiled to minisoccer.mpy (and the grayscale library to
# thumbyGrayscale.mpy) so the Thumby doesn't have to compile 80+ KB of source at
# launch -- that avoids the on-device MemoryError.  This tiny file is all the
# Thumby menu runs.
#
# Everything is wrapped so a failure shows the actual error on screen instead of
# a silent black screen (and prints the traceback to the console/serial).

import gc
import sys

sys.path.insert(0, "/Games/MiniSoccer")
gc.collect()


def _report(e):
    gc.collect()                      # make room in case this was a MemoryError
    try:
        sys.print_exception(e)        # goes to the emulator console / serial
    except Exception:
        pass
    try:
        from thumbyGrayscale import display
        try:
            display.disableGrayscale()
        except Exception:
            pass
        name = type(e).__name__
        msg = str(e)
        display.fill(0)
        try:
            from minisoccer import draw_text
        except Exception:
            display.drawText("ERR " + name[:8], 0, 0, 1)
            display.show()
            return
        draw_text(display, "ERROR", 2, 1, 1)
        draw_text(display, name[:16], 2, 9, 1)
        y = 17
        while msg and y < 36:
            draw_text(display, msg[:17], 2, y, 1)
            msg = msg[17:]
            y += 7
        display.show()
    except Exception:
        pass


try:
    import minisoccer
    minisoccer.main()
except Exception as e:
    _report(e)
    raise
