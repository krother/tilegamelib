
class FruitMultiplets:
    """Sets of fruits that vanish"""
    def __init__(self):
        self.multiplets = []

    def add_multiplet(self, multiplet):
        """Adds a list of positions to the multiplets"""
        if len(multiplet) >= 4:
            self.multiplets.append(multiplet)

    def get_positions(self):
        """Returns a flattened list containing all positions"""
        result = set()
        for multi in self.multiplets:
            for pos in multi:
                result.add(pos)
        return result

    def __len__(self):
        return len(self.multiplets)


class MultipletCounter:

    def __init__(self):
        self.bonus_exponent = 0

    def count(self, multiplets):
        if len(multiplets) > 0:
            self.bonus_exponent += 1
            return None
        else:
            category = self.get_category(multiplets)
            self.bonus_exponent = 0
            return category

    def get_category(self, multiplets):
        """
        Sophisticated method by Borris M. for
        determining the kind of fruit vanish reaction
        previous - number of previous rounds of vanishing
        """
        n_vanish = self.bonus_exponent + 1
        if n_vanish <= 3:
            if len(multiplets) == 1 and len(multiplets[0]) <= 6:
                return 'vanish%i' % len(multiplets[0])
            if len(multiplets) == 2:
                return 'vanish%i_double' % (n_vanish)
            elif len(multiplets) == 3:
                return 'vanish%i_triple' % (n_vanish)
        return 'vanish_mega'
