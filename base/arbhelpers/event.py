class Event:
    def __init__(self, home, away, sport, id_, book):
        self.id = id_
        self.sport = sport
        self.home = home
        self.away = away
        self.start_time = None
        self.betradar_id = None
        self.book = book
        self.text = home + ' vs ' + away

    def print(self):
        print(
            f"Home: {self.home}, Away: {self.away} - ID: {self.id} StartTime: {self.start_time}, "
            f"Book: {self.book}")

    def to_dict(self):
        return {
            "home": self.home,
            "away": self.away,
            "sport": self.sport,
            "start_time": self.start_time,
            "book": self.book,
            "betradar_id": self.betradar_id,
            "text": self.text,
            "_id": self.id
        }
