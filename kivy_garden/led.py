from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.properties import ListProperty, OptionProperty, BooleanProperty, NumericProperty, StringProperty

class Led(Image):
    # led's state
    state = OptionProperty("off", options=["on", "off"])
    # led_type : what changes when state changes (color, source or both)
    led_type = OptionProperty('color',options=['color','source','both'])
    # color_on : color when state is on
    color_on = ListProperty([0.22,0.79,1,1])
    # color_off : color when state is off
    color_off = ListProperty([0.05,0.175,0.225,1])
    # source_on : image source when state is on
    source_on = StringProperty('')
    # source_off : image source when state is off
    source_off = StringProperty('')
    # auto_off : switch auto to off state when True
    auto_off=BooleanProperty(False)
    # auto_off_delay : delay before switching off
    auto_off_delay=NumericProperty(0.2)
    
    def led(self,**kwargs):
        super().led(**kwargs)
        # force setting according to off state
        self.on_state(None,'off')
        
    def toggle_state(self):
        """toggle_state : change state"""
        if self.state == 'on':
            self.state = 'off'
        else:
            self.state = 'on'
    
    def on_state(self,instance,state):
        if state=='on':
            if self.led_type == 'color' or self.led_type == 'both':
                self.color=self.color_on
            if self.led_type == 'source' or self.led_type == 'both':
                self.source=self.source_on
            if self.auto_off:
                Clock.schedule_once(lambda dt: self.set_off(),self.auto_off_delay)
        else: # state==off
            if self.led_type == 'source' or self.led_type == 'both':
                self.source=self.source_off
            if self.led_type == 'color' or self.led_type == 'both':
                self.color=self.color_off
            
    def set_off(self):
        self.state='off'
    
    def on_source_on(self,instance,src):
        if self.state == 'on' and (self.led_type == 'source' or self.led_type == 'both'):
            self.source=self.source_on
            
    def on_source_off(self,instance,src):
        if self.state == 'off' and (self.led_type == 'source' or self.led_type == 'both'):
            self.source=self.source_off
            
    def on_color_on(self,instance,clr):
        if self.state == 'on' and (self.led_type == 'color' or self.led_type == 'both'):
            self.color=self.color_on
            
    def on_color_off(self,instance,clr):
        if self.state == 'off' and (self.led_type == 'color' or self.led_type == 'both'):
            self.color=self.color_off
            
if __name__ == '__main__':
    from kivy.app import App
    from kivy.clock import Clock
    from kivy.lang.builder import Builder
    from kivy.uix.boxlayout import BoxLayout
    kvstr="""

BoxLayout:
    orientation: 'vertical'
    padding: 20
    BoxLayout:
        orientation: 'horizontal'
        BoxLayout:
            orientation: 'vertical'
            Led:
                id: led_typecolor
                source: 'shapes/basic_disc.png'
                color_off: [1,0,0,1]
                color_on: [0,1,0,1]"""
        
    
    class LedApp(App):
        def build(self):
            Clock.schedule_interval(lambda dt: self.toggle_led(),3)
            w=Builder.load_string(kvstr)
            return w
            
        def toggle_led(self):
            for k in self.root.ids:
                if "led_" in k:
                    self.root.ids[k].toggle_state()
           
    LedApp().run()