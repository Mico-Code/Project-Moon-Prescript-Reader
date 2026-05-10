import tkinter as tk
import random
import threading
import time
import sys
import os
from PIL import Image, ImageTk, ImageEnhance  # type: ignore

#"Prescripts"
PRESCRIPTS = [
    "Prepare to act and watch the last person to talk to you die. Afterward, discard this prescript...",
    "Retrieve the package from your Neighbors House.",
    "Observe. Do not engage unless necessary.",
    "Someone requires your presence at the Corridor.",
    "Give her a second chance.",
    "Stand by. Await further instruction.",
    "Neutralise witnesses. Leave no trace.",
    "Be the lover boy again.",
    "Deliver the message. Verbatim.",
    "Crash out. Rage. Let Loose.",
    "Locate Her. Ensure her safety.",
    "Do not go to sleep until you memorized all the numbers of pi.",
    "When everyone is asking something of you, light a candle and watch it burn for 5 minutes.",
    "Burn the evidence. All of it.",
    "Love Bomb Someone.",
    "You are authorized to use lethal force.",
    "The operation begins at midnight be there or be square.",
    "After it is too late to prepare, take a step to the left and go to a concert with the person whose name you have already forgotten.",
    "Complete the assignment. Then disappear.",
    "Eliminate the Capo of the Thumb. He has become a liability.",
    "Talk to her again.",
    "Avoid talking when asked by someone. Do not explain why, just look at them and say nothing. Do this for 5 minutes.",
    "Go to the library and scream the moment you enter. If asked why, just scream.",
    "You Must Gangnam Like I Have.",
    "Let's Larp."
    "Collect my prescripts twin",
    "Perma Ban Widowmaker From Overwatch",
    "Spoil the ending of an anime for the next person you talk to",
    "Tell someone that you told one lie on april",
    "Go to the store and only buy a toaster and a tub plug, when asked why tell them 'I miss her' and leave without another word",
    "Piss on kids.",
    "Jerk off in a public bathroom and then leave without washing your hands.",
    "Go to a restaurant and order the most expensive thing on the menu, when it arrives say 'This is not what I ordered' and then leave without paying.",
    "Go to a movie theater and yell 'This is the worst movie I've ever seen' during the quietest part of the film.",
    "Go to a park and start doing jumping jacks in the middle of a group of people having a picnic.",
    "Go to a dog park with a leash around your next and ask random people if they're your master, if they say yes start wagging your imaginary tail and barking, if they say no start crying and say 'I just want to be loved'.",
    "Bleed on the floor of a grocery store and then walk around barefoot for a while before leaving.",
    "Pretend that you're a furry and have anal butt plug problems in the middle of a crowded street and ask people for help, if they offer to help say 'I'm proud of you Son' and then run away without another word.",
    "Ask someone if they want to see a magic trick, if they say yes shoot the person next to them and say 'Tada!, he doen't exist anymore'.",
    "Adopt a cat and name it after the last person you talked to, then post pictures of the cat on social media for a month without explaining why.",
    "Go to a busy intersection and start doing the macarena in the middle of the crosswalk while cars are waiting for you to cross.",
    "Go to a fast food restaurant and order a burger with no bun, then eat it with your hands and say 'This is how I like it' before leaving without paying.",
    "Happy April Fools Day! You have been pranked by the Index.",
]

#Color Pallette
BG         = "#090d12"
SCREEN_BG  = "#060b14"
SCREEN_FG  = "#7ab8e8"
GOLD       = "#4aa8e8"
GOLD_DIM   = "#1a3a52"
SHELL      = "#0f1a24"
BUTTON_BG  = "#0d1520"
BUTTON_ACT = "#0f2a40"
RED_LED    = "#ff3c3c"
RED_OFF    = "#3a0000"
GREEN_LED  = "#00aaff"
GREEN_OFF  = "#002233"

SCREEN_W = 320
SCREEN_H = 420

#  Beep 
def _beep_thread(freq=880, dur=0.12, reps=2):
    try:
        import winsound
        for _ in range(reps):
            winsound.Beep(freq, int(dur * 1000))
    except Exception:
        try:
            for _ in range(reps):
                sys.stdout.write("\a")
                sys.stdout.flush()
                time.sleep(dur + 0.05)
        except Exception:
            pass

def beep(freq=880, dur=0.12, reps=2):
    threading.Thread(target=_beep_thread, args=(freq, dur, reps), daemon=True).start()

# Logo
_LOGO_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "index_logo.png")

def _make_logo_image(size=80, brightness=1.0):
    try:
        img = Image.open(_LOGO_PATH).convert("RGBA")
        img = img.resize((size, size), Image.LANCZOS)
        img = ImageEnhance.Brightness(img).enhance(brightness)
        return ImageTk.PhotoImage(img)
    except Exception:
        return None

# Main App 
class IndexBeeper:
    BOOT_LINES = [
        "INDEX DEVICE v4.07",
        "HERMES LINK......",
        "AUTHENTICATING...",
        "PROXY CONFIRMED  ",
        "AWAITING PRESCRIPT",
    ]
    COUNTDOWN_SEC = 60

    def __init__(self, root):
        self.root = root
        self.root.title("Index Beeper")
        self.root.resizable(False, False)
        self.root.configure(bg=BG)

        self._countdown   = 0
        self._timer_job   = None
        self._current_msg = ""
        self._boot_done   = False
        self._booting     = False
        self._led_on      = False
        self._led_job     = None
        self._logo_photo  = None
        self._logo_brightness = 0.08

        self._build_ui()
        self.root.after(200, self._start_boot)

    def _build_ui(self):
        shell = tk.Frame(self.root, bg=SHELL, bd=0,highlightbackground=GOLD_DIM, highlightthickness=2,relief="flat")
        shell.pack(padx=18, pady=18, ipadx=14, ipady=18)

        sym_frame = tk.Frame(shell, bg=SHELL)
        sym_frame.pack(pady=(10, 4))
        self.sym_label = tk.Label(sym_frame, bg=SHELL, bd=0)
        self.sym_label.pack()
        self._update_logo(self._logo_brightness)

        self.index_label = tk.Label(shell, text="I N D E X", bg=SHELL,
                                    fg=GOLD_DIM, font=("Courier", 9, "bold"))
        self.index_label.pack()

        led_row = tk.Frame(shell, bg=SHELL)
        led_row.pack(pady=(6, 2))
        self.led_canvas = tk.Canvas(led_row, width=20, height=20,
                                    bg=SHELL, highlightthickness=0)
        self.led_canvas.pack(side="left", padx=6)
        self._led_item = self.led_canvas.create_oval(3, 3, 17, 17,fill=RED_OFF, outline=GOLD_DIM)
        tk.Label(led_row, text="PRESCRIPT", bg=SHELL, fg=GOLD_DIM,font=("Courier", 8)).pack(side="left")

        screen_border = tk.Frame(shell, bg=GOLD_DIM, bd=2)
        screen_border.pack(pady=8)
        self.screen = tk.Canvas(screen_border, width=SCREEN_W, height=SCREEN_H,
                                bg=SCREEN_BG, highlightthickness=0)
        self.screen.pack()

        for y in range(0, SCREEN_H, 4):
            self.screen.create_line(0, y, SCREEN_W, y, fill="#080f1a", width=1)

        self.screen_label = self.screen.create_text(
            SCREEN_W // 2, SCREEN_H // 2 - 30,
            text="", fill=SCREEN_FG, font=("Courier", 11, "bold"),
            width=SCREEN_W - 24, justify="center", tags="msg"
        )
        self.cd_text = self.screen.create_text(
            SCREEN_W // 2, SCREEN_H - 44,
            text="", fill=GOLD, font=("Courier", 20, "bold"), tags="cd"
        )
        self.status_text = self.screen.create_text(
            SCREEN_W // 2, SCREEN_H - 16,
            text="", fill=GOLD_DIM, font=("Courier", 8), tags="status"
        )

        btn_row = tk.Frame(shell, bg=SHELL)
        btn_row.pack(pady=(4, 2))

        self.receive_btn = tk.Button(
            btn_row, text="RECEIVE", width=10,
            bg=BUTTON_BG, fg=GOLD, activebackground=BUTTON_ACT,
            activeforeground=GOLD, font=("Courier", 9, "bold"),
            relief="flat", bd=0, cursor="hand2",
            highlightbackground=GOLD_DIM, highlightthickness=1,
            command=self._receive_prescript, state="disabled"
        )
        self.receive_btn.pack(side="left", padx=8)

        self.finish_btn = tk.Button(
            btn_row, text="COMPLETE", width=10,
            bg=BUTTON_BG, fg=RED_LED, activebackground="#1a0000",
            activeforeground=RED_LED, font=("Courier", 9, "bold"),
            relief="flat", bd=0, cursor="hand2",
            highlightbackground=GOLD_DIM, highlightthickness=1,
            command=self._finish_prescript, state="disabled"
        )
        self.finish_btn.pack(side="left", padx=8)

        tk.Label(shell, text="SN:IDX-0047-RIEN", bg=SHELL, fg="#1a2a3a",font=("Courier", 7)).pack(pady=(8, 0))

    def _start_boot(self):
        self._booting = True
        beep(440, 0.08, 1)
        self._boot_step(0, "")

    def _boot_step(self, idx, accumulated):
        if idx < len(self.BOOT_LINES):
            line = self.BOOT_LINES[idx]
            accumulated = (accumulated + "\n" + line).strip()
            self.screen.itemconfig(self.screen_label, text=accumulated)
            progress = (idx + 1) / len(self.BOOT_LINES)
            self._update_logo(0.08 + 0.92 * progress)
            self.index_label.config(fg=self._lerp_color(GOLD_DIM, GOLD, progress))
            beep(440 + idx * 80, 0.06, 1)
            self.root.after(520, lambda: self._boot_step(idx + 1, accumulated))
        else:
            self.root.after(400, self._boot_complete)

    def _boot_complete(self):
        self._boot_done = True
        self._booting   = False
        self._update_logo(1.0)
        self.index_label.config(fg=GOLD)
        self.screen.itemconfig(self.screen_label, text="STANDING BY\n\nAWAITING\nPRESCRIPT")
        self.screen.itemconfig(self.status_text, text="[ PRESS RECEIVE ]")
        beep(880, 0.15, 2)
        self._start_led_pulse(GREEN_LED, GREEN_OFF)
        self.receive_btn.config(state="normal")

    def _start_led_pulse(self, on_color, off_color, fast=False):
        self._stop_led()
        delay = 400 if fast else 900

        def pulse():
            self._led_on = not self._led_on
            self.led_canvas.itemconfig(self._led_item,fill=on_color if self._led_on else off_color)
            self._led_job = self.root.after(delay, pulse)

        self._led_job = self.root.after(delay, pulse)

    def _stop_led(self):
        if self._led_job:
            self.root.after_cancel(self._led_job)
            self._led_job = None

    def _set_led(self, color):
        self._stop_led()
        self.led_canvas.itemconfig(self._led_item, fill=color)

    def _receive_prescript(self):
        if not self._boot_done:
            return
        self._stop_timer()
        msg = random.choice(PRESCRIPTS)
        self._current_msg = msg
        self._set_led(RED_LED)
        beep(660, 0.07, 3)
        self.screen.itemconfig(self.screen_label, text="INCOMING\nPRESCRIPT...")
        self.screen.itemconfig(self.cd_text, text="")
        self.screen.itemconfig(self.status_text, text="")
        self.root.after(700, lambda: self._reveal_prescript(msg))

    def _reveal_prescript(self, msg):
        self.screen.itemconfig(self.screen_label, text=msg)
        self._countdown = self.COUNTDOWN_SEC
        self.screen.itemconfig(self.cd_text, text=self._fmt_time(self._countdown))
        self.screen.itemconfig(self.status_text, text="[ TIME REMAINING ]")
        self._start_led_pulse(RED_LED, RED_OFF, fast=True)
        self.receive_btn.config(state="normal")
        self.finish_btn.config(state="normal")
        self._tick()

    def _tick(self):
        if self._countdown <= 0:
            self._on_timeout()
            return
        self._countdown -= 1
        self.screen.itemconfig(self.cd_text, text=self._fmt_time(self._countdown))
        if self._countdown <= 10:
            self.screen.itemconfig(self.cd_text, fill=RED_LED)
            if self._countdown % 2 == 0:
                beep(1200, 0.04, 1)
        else:
            self.screen.itemconfig(self.cd_text, fill=GOLD)
        self._timer_job = self.root.after(1000, self._tick)

    def _stop_timer(self):
        if self._timer_job:
            self.root.after_cancel(self._timer_job)
            self._timer_job = None

    def _on_timeout(self):
        self._stop_led()
        self._set_led(RED_OFF)
        beep(220, 0.3, 3)
        self.screen.itemconfig(self.screen_label, text="PRESCRIPT\nEXPIRED\n\nFAILURE\nNOTED.")
        self.screen.itemconfig(self.cd_text, text="00:00")
        self.screen.itemconfig(self.status_text, text="[ INDEX IS WATCHING ]")
        self.finish_btn.config(state="disabled")
        self._start_led_pulse(RED_LED, RED_OFF, fast=True)

    def _finish_prescript(self):
        self._stop_timer()
        self._stop_led()
        self._set_led(GREEN_LED)
        beep(880, 0.1, 1)
        self.root.after(80, lambda: beep(1100, 0.15, 1))
        self.screen.itemconfig(self.screen_label, text="PRESCRIPT\nCOMPLETE\n\nHERMES\nACKNOWLEDGES.")
        self.screen.itemconfig(self.cd_text, text="")
        self.screen.itemconfig(self.status_text, text="[ STANDING BY ]")
        self.finish_btn.config(state="disabled")
        self._start_led_pulse(GREEN_LED, GREEN_OFF)

    def _update_logo(self, brightness):
        photo = _make_logo_image(size=80, brightness=brightness)
        if photo:
            self._logo_photo = photo
            self.sym_label.config(image=photo)
        self._logo_brightness = brightness

    @staticmethod
    def _fmt_time(secs):
        return f"{secs // 60:02d}:{secs % 60:02d}"

    @staticmethod
    def _lerp_color(c1, c2, t):
        def parse(c):
            c = c.lstrip("#")
            return tuple(int(c[i:i+2], 16) for i in (0, 2, 4))
        r1, g1, b1 = parse(c1)
        r2, g2, b2 = parse(c2)
        r = int(r1 + (r2 - r1) * t)
        g = int(g1 + (g2 - g1) * t)
        b = int(b1 + (b2 - b1) * t)
        return f"#{r:02x}{g:02x}{b:02x}"

if __name__ == "__main__":
    root = tk.Tk()
    app = IndexBeeper(root)
    root.mainloop()