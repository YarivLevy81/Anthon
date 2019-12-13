UNDEFINED_VARIABLE = -1


class Snapshot:

    def __init__(self):
        self.timestamp = UNDEFINED_VARIABLE
        self.translation = Snapshot.Translation()
        self.rotation = Snapshot.Rotation()
        self.color_image = None
        self.depth_image = None
        self.feelings = Snapshot.UserFeelings()

    def __repr__(self):
        out_string = "<<< Snapshot >>>\n"
        out_string += f'timestamp   = {self.timestamp}\n'
        out_string += f'translation = {(self.translation.x, self.translation.y, self.translation.z)}\n'
        out_string += f'rotation    = {(self.rotation.x, self.rotation.y, self.rotation.z, self.rotation.w)}\n'
        out_string += 'color_image=' + repr(self.color_image) + "\n"
        out_string += 'depth_image=' + repr(self.depth_image) + "\n"
        out_string += f'feeling= {self.feelings.hunger, self.feelings.thirst, self.feelings.exhaustion, self.feelings.happiness}\n'
        out_string += "<<< Snapshot >>>\n"

        return out_string

    class Translation:
        def __init__(self):
            self.x = UNDEFINED_VARIABLE
            self.y = UNDEFINED_VARIABLE
            self.z = UNDEFINED_VARIABLE

    class Rotation:
        def __init__(self):
            self.x = UNDEFINED_VARIABLE
            self.y = UNDEFINED_VARIABLE
            self.z = UNDEFINED_VARIABLE
            self.w = UNDEFINED_VARIABLE

    class UserFeelings:
        def __init(self):
            self.hunger = UNDEFINED_VARIABLE
            self.thirst = UNDEFINED_VARIABLE
            self.exhaustion = UNDEFINED_VARIABLE
            self.happiness = UNDEFINED_VARIABLE
