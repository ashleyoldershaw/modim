import time
from ws_client import begin, end, display_text, display_image, ask

begin()
display_image("dolphin")
display_text("Ecco la nuova interfaccia MODIM")
time.sleep(5)
display_text("Ti piace?")
a = ask("['Si', 'No']")
print "Hai risposto: ",a
if a=='Si':
    display_text("Bene. Mi fa piacere.")
else:
    display_text("Ooops. Mi dispiace.")
time.sleep(3)
display_text("Arrivederci")
end()

