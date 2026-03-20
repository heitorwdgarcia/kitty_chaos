from core.world import World

world = World()

def __getattr__(name):
    return getattr(world, name)

def __setattr__(name, value):
    return setattr(world, name, value)