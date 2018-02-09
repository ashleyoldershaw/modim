from interaction_manager import InteractionManager


im = InteractionManager()

im.setProfile(['*', '*', 'es', '*'])
im.setPath('../../demo/eurobotics/')
im.execute('animal')


#im.setPath('../../demo/facultywelcomedaynew/')
#im.execute('welcome')
