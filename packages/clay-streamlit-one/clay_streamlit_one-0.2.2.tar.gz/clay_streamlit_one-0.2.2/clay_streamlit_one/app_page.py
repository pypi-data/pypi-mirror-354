import os
import streamlit as st
import time

class AppPage():
    def __init__(self, name, main_fun=None, sidebar_fun=None):
        # print(f"AppPage.__init__ called for page '{name}'")
        self.name = name
        
        self.main_fun = main_fun
        self.sidebar_fun = sidebar_fun
        
    def run(self):
        print(f"AppPage.run called for page '{self.name}'")

        if self.main_fun is None:
            st.header(f"I'm page '{self.name}'")
        else:
            self.main_fun()

    # this is called by ClayStreamlitApp.run_page
    def set_sidebar(self):
        if self.sidebar_fun is not None:
            # st.divider()
            st.write(f":rainbow[*menus for {self.name}*]", unsafe_allow_html=True)
            self.sidebar_fun()


    def _force_quit(self):
        pid = os.getpid()
        st.error(f"**The app was terminated on page {self.name}**")
        time.sleep(0.1)
        os.kill(pid, 9)  # Forcefully stops the server        
        
