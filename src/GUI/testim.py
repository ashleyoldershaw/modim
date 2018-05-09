from interaction_manager import InteractionManager


im = InteractionManager(None, None)

im.setProfile(['*', '*', 'es', '*'])
im.setPath('../../demo/eurobotics/')
im.init()
im.execute('welcome')
im.execute('animal')


#im.setPath('../../demo/facultywelcomedaynew/')
#im.execute('welcome')
