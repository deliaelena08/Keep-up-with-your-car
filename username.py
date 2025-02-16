
username_helper1= """
MDTextField:
    hint_text:"Introduceti numele utilizatorului"
    helper_text_mode:"on_focus"
    pos_hint:{'x':0.27,'y':0.5}
    size_hint_x:None
    width:500
"""
BoxLayout:
            size_hint: (1,1)
            padding: [100, 70, 100, 70]
            cols:2
            spacing:"5dp"
Label:
                text:"Nume de utilizator"
                color:0,0,0,1
                font_size:"16dp"
            TextInput:
                multiline: False
