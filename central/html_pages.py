import language

# load stylesheet
style=None
with open('style.css','r') as f:
    style=f.read()

# load language
lang=language.load_language('es')

# html index page
html_head="""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            {0}
        </style>
        <title>Alarm System</title>
    </head>
    """.format(style)

def html_index(alarm_state,alarm_running,devices=None):
    img="/disarmed.png" if alarm_running else "/armed.png"
    if alarm_state and alarm_running:
        state=lang['breached_state']
        img="/disarmed.png"
    else:
        img="/armed.png" if alarm_state else "/disarmed.png"
        state=lang['armed_state'] if alarm_state else lang['disarmed_state']
    html=html_head+"""
        <body>
            <a href="/"><img src="/reload.png" alt="Reload page" class="right"></a>
            <img src={0} alt="Image" class="center" width="350" height="350" >
            <h1 class="center" style="font-size:42px;">{1}</h1>
            <div class="control-btn">
                <a href="/start"><img src="/start.png" alt="Start Alarm" width="175" height="175"></a>
            </div>
            <div class="control-btn">
                <a href="/stop"><img src="/stop.png" alt="Stop Alarm" width="175" height="175"></a>
            </div>
        """.format(img,state)
    html_table="""
            <table>
            """
    for device in devices:
        sensor_state_img="/stop.png" if devices[device]['state'] else "/start.png"
        html_table+="""
                <tr>
                    <th style="text-align:left; font-size: 30px;">{0}: {1}</th>
                    <th><img src={2} alt="Sensor state" width="50" height="50"></th>
                </tr>        
                """.format(devices[device]['location'],devices[device]['type'],sensor_state_img)
    html_table+="""
            </table>
        </body>
    </html>"""
    
    return html+html_table
