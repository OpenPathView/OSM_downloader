from . import wrapper
import os

# os.chdir(os.path.dirname(os.path.abspath(__file__)))

#MainWindow of any use ???? (four interogation point because I think it's useless ^^)
class MainWindow():
    """
    define an autonome leaflet window
    """

    def __init__(self):
        """
        init stuff
        """
        self.leafletWrapper = wrapper.Wrapper()
        self.leafletWrapper.start()

    def join(self):
        """
        wait for the subprocess to end (not needed went intergrated in other app)
        """
        self.leafletWrapper.join()
