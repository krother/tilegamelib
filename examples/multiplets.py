
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
        self._score = 0
        self._last_multi = None

    def count(self, multiplets):
        if len(multiplets) > 0:
            self.bonus_exponent += 1
            self._last_multi = multiplets
            return None
        else:
            category = self.get_category(multiplets)
            return category

    def pull_score(self):
        score = self._score
        self._score = 0
        return score

    def reset(self):
        self._last_multi = None
        self.bonus_exponent = 0

    def get_category(self):
        """
        Sophisticated method by Borris M. for
        determining the kind of fruit vanish reaction
        """
        if not self._last_multi:
            return
        else:
            n_vanish = self.bonus_exponent + 1
            multiplets = self._last_multi.multiplets
            self._score = len(multiplets) * sum([len(m) for m in multiplets]) ** self.bonus_exponent * 10
            if n_vanish <= 3:
                if len(multiplets) == 1 and len(multiplets[0]) <= 6:
                    category = 'vanish%i' % len(multiplets[0])
                if len(multiplets) == 2:
                    category = 'vanish%i_double' % (n_vanish)
                elif len(multiplets) == 3:
                    category = 'vanish%i_triple' % (n_vanish)
                print(category)
                return category
            category = 'vanish_mega'
            print(category)
            return category
