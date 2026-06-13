from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.core.text import LabelBase

from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout

from kivy.graphics import Color, Line, Ellipse

from datetime import datetime

import os
import math
import psutil
import subprocess



# ================= FONT =================

if os.path.exists("fonts/BebasNeue-Regular.ttf"):

    LabelBase.register(
        name="Fliqlo",
        fn_regular="fonts/BebasNeue-Regular.ttf"
    )

    FONT="Fliqlo"

else:

    FONT="Roboto"



# ================= STATE =================

MODE="clock"
LAST_TOOL=None

THEME="dark"
ZEN=False

running=False



# TIMER

timer_stage="hours"
timer_input=""

timer_h=0
timer_m=0
timer_s=0

timer_time=0

timer_ready=False



# STOPWATCH

stopwatch_time=0



# POMO

pomo_stage="focus"

pomo_input=""

pomo_focus=0
pomo_break=0

pomo_time=0

pomo_phase="FOCUS"

pomo_ready=False





class FocusDeck(FloatLayout):


    def __init__(self,**kw):

        super().__init__(**kw)


        Window.fullscreen="auto"
        self.popup=None



        self.mode_label=Label(

            text="",

            font_name=FONT,

            size_hint=(1,None),

            height=80,

            pos_hint={
                "center_x":.5,
                "center_y":.72
            }

        )




        self.clock=Label(

            text="",

            font_name=FONT,

            size_hint=(1,1),

            pos_hint={
                "center_x":.5,
                "center_y":.45
            }

        )




        self.date=Label(

            size_hint=(None,None),

            size=(200,50),

            pos_hint={
                "x":.025,
                "top":.97
            }

        )




        self.title=Label(

            text="FOCUSDECK",

            bold=True,

            size_hint=(None,None),

            size=(300,50),

            pos_hint={
                "center_x":.5,
                "top":.97
            }

        )





        self.battery=Label(

            size_hint=(None,None),

            size=(200,50),

            pos_hint={
                "right":.975,
                "top":.97
            }

        )

        # ====== NOTIFICATION DOT ======
        with self.battery.canvas.after:
            self.notification_color = Color(1, 0, 0, 1) 
            self.notification_dot = Ellipse(size=(10, 10))
            
        # Bind pos, size, AND texture_size so the dot moves if the text gets wider!
        self.battery.bind(pos=self.update_dot, size=self.update_dot, texture_size=self.update_dot)
        # ==============================


        self.media=Label(

            font_name=FONT,

            size_hint=(1,None),

            height=60,

            pos_hint={
                "center_x":.5,
                "y":.08
            }

        )





        # HELP BUTTON


        self.help_icon=Button(

            text="?",

            font_name=FONT,

            background_color=(0,0,0,0),

            size_hint=(None,None),

            size=(70,70),

            pos_hint={
                "right":.98,
                "y":.02
            }

        )


        self.help_icon.bind(
            on_press=self.show_help
        )





        for x in [

            self.mode_label,
            self.clock,
            self.date,
            self.title,
            self.battery,
            self.media,
            self.help_icon

        ]:

            self.add_widget(x)





        self.bind(size=self.resize)



        Window.bind(
            on_key_down=self.keys
        )



        Clock.schedule_interval(
            self.update,
            .01
        )



    # ====== NOTIFICATION UPDATE ======
    def update_dot(self, *args):
        base = min(Window.width, Window.height)
        dot_size = base * .012
        self.notification_dot.size = (dot_size, dot_size)
        
        # Calculate exactly where the text ends inside the label
        text_width = self.battery.texture_size[0]
        text_right_edge = self.battery.center_x + (text_width / 2)
        
        # Positioned perfectly to the right of the "%" text, hovering slightly up
        self.notification_dot.pos = (
            text_right_edge + (base * .006), 
            self.battery.center_y + (base * .005)
        )
    # =================================


    def resize(self,*a):


        base=min(
            Window.width,
            Window.height
        )


        self.clock.font_size=base*.38

        self.mode_label.font_size=base*.08

        self.date.font_size=base*.03

        self.title.font_size=base*.035

        self.battery.font_size=base*.03

        self.media.font_size=base*.04

        self.help_icon.font_size=base*.05









    def fmt(self,t):


        t=max(0,t)


        h=int(t//3600)

        m=int(t%3600//60)

        s=int(t%60)



        return f"{h:02}:{m:02}:{s:02}"







    def battery_status(self):


        try:

            b=psutil.sensors_battery()


            if b:

                return str(
                    int(b.percent)
                )+"%"


            return "AC"


        except:

            return ""








    def media_status(self):


        if ZEN:

            self.media.opacity=0

            return



        try:


            title=subprocess.check_output(

                [
                    "playerctl",
                    "metadata",
                    "title"
                ],

                stderr=subprocess.DEVNULL

            ).decode().strip()



            self.media.text=title

            self.media.opacity=1




        except:


            self.media.opacity=0
    # ================= ANALOG =================


    def analog(self):

        self.canvas.after.clear()

        now=datetime.now()


        cx=self.width/2
        cy=self.height/2


        r=min(
            self.width,
            self.height
        )*.32



        col=(.85,.85,.85,1)


        if THEME=="light":

            col=(0,0,0,1)



        with self.canvas.after:


            Color(*col)


            Line(
                circle=(cx,cy,r),
                width=3
            )


            for i in range(12):

                a=math.radians(i*30)


                Line(

                    points=[

                    cx+math.sin(a)*r*.85,
                    cy+math.cos(a)*r*.85,

                    cx+math.sin(a)*r,
                    cy+math.cos(a)*r

                    ],

                    width=3
                )



            hands=[


            (
            (now.hour%12+
            now.minute/60)*30,
            .45,
            6
            ),


            (
            now.minute*6,
            .7,
            4
            ),


            (
            now.second*6,
            .85,
            2
            )

            ]



            for angle,length,width in hands:


                a=math.radians(angle)


                Line(

                    points=[

                    cx,
                    cy,

                    cx+math.sin(a)*r*length,

                    cy+math.cos(a)*r*length

                    ],

                    width=width
                )









    # ================= HELP =================


    def show_help(self,*args):


        if ZEN:

            return



        content=Label(

            text=(

            "FOCUSDECK\n\n"

            "CLOCKS\n"
            "C  - CLOCK\n"
            "A  - ANALOG CLOCK\n\n"

            "TOOLS\n"
            "T  - TIMER\n"
            "S  - STOPWATCH\n"
            "P  - POMODORO\n\n"

            "CONTROL\n"
            "SPACE - START / PAUSE\n"
            "R  - RESET\n\n"

            "DISPLAY\n"
            "D - DARK MODE\n"
            "L - LIGHT MODE\n"
            "Z - ZEN MODE\n"
            "RED DOT - NOTIFICATION\n\n"

            "SWITCH\n"
            "C/A KEEPS SESSION\n"
            "T/S/P RESETS SESSION\n\n"

            "ESC - EXIT"

            ),

            font_name="Roboto",

            font_size=28

        )



        self.popup=Popup(

            title="",

            content=content,

            size_hint=(.45,.7),

            auto_dismiss=True

        )


        self.popup.open()







    # ================= RESET =================


    def reset_sessions(self):


        global running

        global timer_stage,timer_input
        global timer_h,timer_m,timer_s
        global timer_time
        global timer_ready

        global stopwatch_time

        global pomo_stage,pomo_input
        global pomo_time
        global pomo_ready



        running=False



        timer_stage="hours"
        timer_input=""


        timer_h=0
        timer_m=0
        timer_s=0


        timer_time=0

        timer_ready=False



        stopwatch_time=0



        pomo_stage="focus"

        pomo_input=""

        pomo_time=0

        pomo_ready=False








    # ================= UPDATE =================


    def update(self,dt):


        global timer_time
        global stopwatch_time

        global pomo_time
        global pomo_phase

        global running



        if MODE!="analog":

            self.canvas.after.clear()



        now=datetime.now()


        self.date.text=now.strftime("%b %d")


        self.battery.text=self.battery_status()


        self.media_status()





        if MODE=="clock":


            self.mode_label.text=""


            self.clock.opacity=1


            self.clock.text=now.strftime(
                "%H:%M:%S"
            )





        elif MODE=="analog":


            self.mode_label.text=""

            self.clock.opacity=0

            self.analog()







        elif MODE=="timer":


            self.clock.opacity=1



            if timer_ready:


                self.mode_label.text="TIMER"



                if running:


                    timer_time-=dt



                    if timer_time<=0:

                        timer_time=0

                        running=False



                self.clock.text=self.fmt(
                    timer_time
                )




            else:


                self.mode_label.text="SET "+timer_stage.upper()


                self.clock.text=(

                    timer_input

                    if timer_input

                    else "00"

                )









        elif MODE=="stopwatch":


            self.clock.opacity=1

            self.mode_label.text="STOPWATCH"



            if running:


                stopwatch_time+=dt



            m=int(stopwatch_time//60)

            s=int(stopwatch_time%60)

            ms=int(stopwatch_time%1*100)



            self.clock.text=(

                f"{m:02}:{s:02}.{ms:02}"

            )









        elif MODE=="pomodoro":


            self.clock.opacity=1



            if pomo_ready:


                self.mode_label.text="POMODORO"



                if running:


                    pomo_time-=dt



                    if pomo_time<=0:


                        if pomo_phase=="FOCUS":


                            pomo_phase="BREAK"

                            pomo_time=pomo_break



                        else:


                            pomo_phase="FOCUS"

                            pomo_time=pomo_focus




                self.clock.text=self.fmt(
                    pomo_time
                )





            else:


                if pomo_stage=="focus":

                    self.mode_label.text="FOCUS MINUTES"


                else:

                    self.mode_label.text="BREAK MINUTES"



                self.clock.text=(

                    pomo_input

                    if pomo_input

                    else "00"

                )







        self.theme()









    # ================= THEME =================


    def theme(self):


        if THEME=="dark":

            Window.clearcolor=(0,0,0,1)

            fg=(.82,.82,.82,1)


        else:

            Window.clearcolor=(1,1,1,1)

            fg=(0,0,0,1)




        for x in self.children:


            if hasattr(x,"color"):

                x.color=fg






        show=0 if ZEN else 1


        self.title.opacity=show

        self.date.opacity=show

        self.battery.opacity=show

        self.media.opacity=show

        self.mode_label.opacity=show

        self.help_icon.opacity=show







    # ================= KEYS =================


    def keys(self,w,key,s,c,m):


        global MODE,LAST_TOOL
        global THEME,ZEN,running


        global timer_stage,timer_input
        global timer_h,timer_m,timer_s
        global timer_time,timer_ready


        global pomo_stage,pomo_input
        global pomo_focus,pomo_break
        global pomo_time,pomo_phase,pomo_ready




        c=str(c or "").lower()




        if key==27:


            if self.popup:


                self.popup.dismiss()

                self.popup=None


            else:


                App.get_running_app().stop()






        elif c in ["t","s","p"]:



            if LAST_TOOL and LAST_TOOL!=c:

                self.reset_sessions()



            LAST_TOOL=c



            if c=="t":

                MODE="timer"


            elif c=="s":

                MODE="stopwatch"


            elif c=="p":

                MODE="pomodoro"






        elif c=="a":

            MODE="analog"

            self.clock.opacity=0






        elif c=="c":

            MODE="clock"






        elif key==32:

            running=not running






        elif c=="d":

            THEME="dark"





        elif c=="l":

            THEME="light"





        elif c=="z":

            ZEN=not ZEN





        elif c=="r":

            self.reset_sessions()







        elif key==8:


            if MODE=="timer":

                timer_input=timer_input[:-1]


            elif MODE=="pomodoro":

                pomo_input=pomo_input[:-1]








        elif c.isdigit():



            if MODE=="timer":

                timer_input+=c


            elif MODE=="pomodoro":

                pomo_input+=c









        elif key in [13,271]:




            if MODE=="timer":


                value=int(timer_input or 0)



                if timer_stage=="hours":

                    timer_h=value
                    timer_stage="minutes"



                elif timer_stage=="minutes":

                    timer_m=value
                    timer_stage="seconds"



                else:


                    timer_s=value


                    timer_time=(

                    timer_h*3600+

                    timer_m*60+

                    timer_s

                    )


                    timer_ready=True

                    running=True



                timer_input=""








            elif MODE=="pomodoro":


                value=int(
                    pomo_input or 0
                )*60



                if pomo_stage=="focus":

                    pomo_focus=value

                    pomo_stage="break"



                else:


                    pomo_break=value

                    pomo_time=pomo_focus

                    pomo_phase="FOCUS"

                    pomo_ready=True

                    running=True



                pomo_input=""









class FocusDeckApp(App):


    def build(self):

        self.title="FocusDeck"

        return FocusDeck()




FocusDeckApp().run()