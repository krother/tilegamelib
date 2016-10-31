
VANISH_CATEGORIES = {
    (1, 1, 4): 'quadruple',
    (1, 1, 5): 'quintuple',
    (1, 1, 6): 'sextuple',
    (1, 1, 7): 'septuple',
    (1, 2, 4): 'double_quadruple',
    (1, 2, 5): 'double_quintuple',
    (1, 2, 6): 'double_sextuple',
    (2, 1, 4): '2nd_quadruple',
    (2, 1, 5): '2nd_quintuple',
    (2, 1, 6): '2nd_sextuple',
    (3, 1, 4): '3rd_quadruple',
    (3, 1, 5): '3rd_quintuple',
}


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
        self.n_vanish = 0
        self._score = 0
        self._last_multi = None

    def count(self, multiplets):
        if len(multiplets) > 0:
            self.n_vanish += 1
            self._score += len(multiplets) * sum([len(m) for m in multiplets.multiplets]) ** self.n_vanish * 10
            self._last_multi = multiplets

    def pull_score(self):
        score = self._score
        self._score = 0
        return score

    def reset(self):
        self._last_multi = None
        self.n_vanish = 0

    def get_category(self):
        """
        Sophisticated method by Borris M. for
        determining the kind of fruit vanish reaction
        """
        if self._last_multi:
            multiplets = self._last_multi.multiplets
            vanish_type = (self.n_vanish, len(multiplets), len(multiplets[0]))
            category = VANISH_CATEGORIES.get(vanish_type, 'mega_vanish')
            print(category, vanish_type)
            return category
