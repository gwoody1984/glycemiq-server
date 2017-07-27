from thespian.actors import ActorSystem


class _ActorSystemManager:
    def __init__(self):
        self.actor_system = None

    def get_actor_system(self):
        if self.actor_system is None:
            self.actor_system = ActorSystem('multiprocTCPBase')

        return self.actor_system


actorSystemManager = _ActorSystemManager()
