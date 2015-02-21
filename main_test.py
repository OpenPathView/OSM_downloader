
from pyleaflet import Wrapper
from pyleaflet import event
leafletWrapper = Wrapper()
leafletWrapper.start()
while 1:
    e = leafletWrapper.waitEvent()
    print(e)
    if e.eventId==event.QUIT:
        exit()
