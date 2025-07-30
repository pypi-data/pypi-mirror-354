import sys
import time
import threading
import signal
import logging
import traceback
import atexit # <-- NEW IMPORT
from AppKit import (
    NSApplication, NSApp, NSWindow, NSTextField, NSRect, NSColor,
    NSWindowStyleMaskBorderless, NSBackingStoreBuffered,
    NSWindowCollectionBehaviorCanJoinAllSpaces,
    NSWindowCollectionBehaviorFullScreenAuxiliary, NSScreenSaverWindowLevel,
    NSFont, NSTextAlignmentCenter, NSView, NSScreen,
    NSDefaultRunLoopMode, NSAnyEventMask
)
from Foundation import NSObject, NSDate
import objc

class CaptionWindowController(NSObject):
    def __init__(self):
        super(CaptionWindowController, self).init()
        self.is_running = False
        self.window = None

    def setupWindow(self):
        self.is_running = True
        # ... (The rest of the setupWindow method is IDENTICAL)
        main_screen_rect = NSScreen.mainScreen().frame()
        screen_w = main_screen_rect.size.width
        win_w = 800
        win_h = 100
        win_x = (screen_w - win_w) / 2
        win_y = 150
        window_frame = NSRect((win_x, win_y), (win_w, win_h))

        self.window = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
            window_frame, NSWindowStyleMaskBorderless, NSBackingStoreBuffered, False)
        # ... (All window and text field setup is the same)
        self.window.setOpaque_(False)
        self.window.setBackgroundColor_(NSColor.clearColor())
        self.window.setHasShadow_(False)
        self.window.setCollectionBehavior_(
            NSWindowCollectionBehaviorCanJoinAllSpaces |
            NSWindowCollectionBehaviorFullScreenAuxiliary)
        self.window.setLevel_(NSScreenSaverWindowLevel)
        self.content_view = NSView.alloc().initWithFrame_(self.window.frame())
        self.content_view.setWantsLayer_(True)
        self.content_view.layer().setBackgroundColor_(NSColor.colorWithCalibratedWhite_alpha_(0.0, 0.5).CGColor())
        self.content_view.layer().setCornerRadius_(10)
        self.text_field = NSTextField.alloc().initWithFrame_(self.content_view.bounds())
        self.text_field.setStringValue_("Starting Overlay...")
        self.text_field.setBezeled_(False)
        self.text_field.setDrawsBackground_(False)
        self.text_field.setEditable_(False)
        self.text_field.setSelectable_(False)
        self.text_field.setTextColor_(NSColor.whiteColor())
        self.text_field.setFont_(NSFont.boldSystemFontOfSize_(24))
        self.text_field.setAlignment_(NSTextAlignmentCenter)
        self.content_view.addSubview_(self.text_field)
        self.window.setContentView_(self.content_view)
        self.window.makeKeyAndOrderFront_(None)

        self.captions = ["This overlay can now handle crashes.", "Press Ctrl+C in the terminal to quit.", "Errors are logged to crash_log.txt"]
        self.current_caption_index = -1
        self.update_caption_on_main_thread()

    def update_caption(self):
        if self.is_running:
            self.performSelectorOnMainThread_withObject_waitUntilDone_(b'update_caption_on_main_thread', None, False)

    @objc.selector
    def update_caption_on_main_thread(self):
        if not self.is_running: return
        try:
            self.current_caption_index = (self.current_caption_index + 1) % len(self.captions)
            new_text = self.captions[self.current_caption_index]
            self.text_field.setStringValue_(new_text)
        except Exception as e:
            logging.exception("Error during caption update.")
            self.stop() # If an error occurs here, gracefully shut down.
        
        if self.is_running:
            threading.Timer(3.0, self.update_caption).start()

    def stop(self):
        """Gracefully stops the application and immediately hides the window."""
        if self.is_running:
            print("Shutdown requested. Tearing down overlay...")
            self.is_running = False
            if self.window:
                self.window.orderOut_(None)

def run_caption_app():
    # --- 1. SETUP LOGGING ---
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        filename='crash_log.txt',
        filemode='w'
    )
    
    app = NSApplication.sharedApplication()
    controller = CaptionWindowController.alloc().init()

    # --- 2. REGISTER FAILSAFE CLEANUP ---
    # This ensures controller.stop() is called no matter how the script exits.
    atexit.register(controller.stop)

    # Setup signal handler for Ctrl+C
    def sigint_handler(signum, frame):
        logging.info("Ctrl+C detected. Shutting down gracefully...")
        controller.stop()
    signal.signal(signal.SIGINT, sigint_handler)
    
    # --- 3. MAIN SAFETY NET ---
    try:
        controller.setupWindow()
        logging.info("Caption overlay started successfully.")
        print("Caption overlay is running. Press Ctrl+C in this terminal to quit.")

        # Manual Event Loop
        while controller.is_running:
            event = app.nextEventMatchingMask_untilDate_inMode_dequeue_(
                NSAnyEventMask, NSDate.distantPast(), NSDefaultRunLoopMode, True)
            if event:
                app.sendEvent_(event)
            time.sleep(0.01)

        for _ in range(10): # A small, finite number of spins is enough
            event = app.nextEventMatchingMask_untilDate_inMode_dequeue_(
                NSAnyEventMask, NSDate.distantPast(), NSDefaultRunLoopMode, True)
            if not event:
                # No more events to process
                break
            app.sendEvent_(event)

    except Exception as e:
        # Catch any unexpected crash during setup or the event loop
        print("An unhandled error occurred! See crash_log.txt for details.")
        logging.exception("Unhandled exception in main loop caught.")
        # The 'atexit' handler will take care of cleanup.

    finally:
        # The finally block also ensures stop is called, providing an extra
        # layer of safety to prevent zombie windows.
        controller.stop()
        print("Application overlay has terminated.")
        print("Restoring default Ctrl+C behavior.")
        signal.signal(signal.SIGINT, signal.SIG_DFL) # DFL = Default Function
        print("Continuing with other Python tasks...")