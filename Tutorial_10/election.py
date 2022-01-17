class Vote:
    """A single vote object.
    
    Data attributes:
    - preference_list: a list of the preferred parties for this voter,
      in descending order of preference.
    """
    def __init__(self, preference_list) -> None:
        self.preference_list = preference_list
    def __str__(self) -> str:
        if not self.preference_list:
            return 'Blank'
        return ' > '.join(self.preference_list)
    def __repr__(self) -> str:
        return f'Vote({self.preference_list})'
    def first_preference(self):
        return None if not self.preference_list else self.preference_list[0]
    def preference(self, names):
        """Return the item in names that occurs first in the preference list,
        or None if no item in names appears.
        """
        for name in self.preference_list:
            if name in names:
                return name
        return None

class Election:
    """A basic election class.
    
    Data attributes:
    - parties: a list of party names
    - blank: a list of blank votes
    - piles: a dictionary with party names for keys
      and lists of votes (allocated to the parties) for values
    - dead: a list of votes that no longer interfere on the outcome of the Election
    """
    
    def __init__(self, parties):
        self.parties = parties
        self.blank = []
        self.piles = {name:[] for name in self.parties}
        self.dead = []

    def add_vote(self, vote):
        """Append the vote to the corresponding pile."""
        if vote.first_preference() == None:
            self.blank.append(vote)
        else:
            self.piles[vote.first_preference()].append(vote)

    def status(self) -> dict:
        """Return the current status of the election:
        a dictionary mapping each of the party names in the piles
        to the number of votes in their pile.
        """
        return {name:len(value) for (name,value) in self.piles.items()}

    def add_votes_from_file(self, filename):
        """
        Convert each line of the file into a Vote,
        and append each of the votes to the correct pile.
        """
        with open(filename, 'r') as file:
            for line in file:
                self.add_vote(Vote(line.split()))

    def first_past_the_post_winner(self):
        """Return the winner of this election under
        the first-past-the-post system, or None if
        the election is tied.
        """
        winner = None
        maxVote = -1
        status = self.status()
        print(status)
        for key, votes in status.items():
            if votes > maxVote: 
                winner, maxVote = key, votes
            elif votes == maxVote: winner = None
        return winner

    def weighted_status(self):
        """Returns a dictionary with keys being the parties
        and values being the number of points (counted using
        the weighted scheme) that the party got.
        """
        weights = [5,4,3,2,1]
        points = {name: 0 for name in self.parties}
        for votes in self.piles.values():
            for vote in votes:
                for i in range(len(vote.preference_list)):
                    points[vote.preference_list[i]] += weights[i]
        return points

    def weighted_winner(self):
        """
        Return the winner of this election under
        the weighted voting scheme.
        """
        result = self.weighted_status()
        curMax = -1
        winner = '' 
        for name, votes in result.items():
            if votes == curMax:
                winner = min(winner, name)
            elif votes > curMax:
                curMax, winner = votes, name
        return winner

    def eliminate(self, party):
        """Remove the given party from piles, and redistribute its 
        votes among the parties not yet eliminated, according to 
        their preferences.  If all preferences have been eliminated, 
        then add the vote to the dead list.
        """
        votes = self.piles[party]
        del self.piles[party]
        for vote in votes:
            preference = vote.preference(self.piles.keys())
            if preference == None:
                self.dead.append(vote)
            else:
                self.piles[preference].append(vote)

    def round_loser(self):
        """Return the name of the party to be eliminated from the next round."""
        status = self.status()
        cur_min = -1
        loser = ""
        quantity_primary_votes = {name: 0 for name in self.piles.keys()}
        for name, votes in self.piles.items():
            for vote in votes:
                if vote.preference_list and vote.preference_list[0] == name:
                    quantity_primary_votes[name] += 1

        for name, votes in status.items():
            if votes == cur_min:
                if quantity_primary_votes[name] < quantity_primary_votes[loser]:
                    loser = name
                if quantity_primary_votes[name] == quantity_primary_votes[loser] and loser > name:                  loser = name
            if cur_min == -1 or votes < cur_min:
                cur_min = votes
                loser = name 
        return loser

    def preferential_winner(self):
        """Run a preferential election based on the current piles of votes,
        and return the winning party.
        """
        while len(self.piles.keys()) > 1:
            self.eliminate(self.round_loser())

        for key in self.piles.keys():
            return key

    def two_round_winner(self):
        """Run a two round winner election"""
        status = self.status()
        weight = self.weighted_status()
        data_candidates = []
        for name in self.piles.keys():
            data_candidates.append((status[name], weight[name], name))
        ordered_cadidates = sorted(data_candidates, reverse=True)
        # for candidate in ordered_cadidates:
        #     print(candidate)
        second_turn = [ordered_cadidates[0], ordered_cadidates[1]]
        preference = {second_turn[0][2]: 0, second_turn[1][2]: 0}
        for value in self.piles.values():
            for vote in value:
                for name in vote.preference_list:
                    if name in preference.keys():
                        preference[name] += 1
                        break
        if preference[ordered_cadidates[0][2]] > preference[ordered_cadidates[1][2]]:
            return ordered_cadidates[0][2]
        elif preference[ordered_cadidates[0][2]] < preference[ordered_cadidates[1][2]]:
            return ordered_cadidates[1][2]
        else:
            return max(ordered_cadidates[0][2], ordered_cadidates[1][2])
