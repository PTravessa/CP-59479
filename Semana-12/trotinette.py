from datetime import datetime


class Trotinette:
    def __init__(self, id, cost_per_minute):
        self.id = id
        self.rent_timestamp_start = None
        self.rent_timestamp_end = None
        self.user_id = None
        self.cost_per_minute = cost_per_minute
        self.total_benefit = 0

    def check_in(self, user_id):
        assert not self.in_use(), 'The trotinette is being used.'
        self.user_id = user_id
        self.rent_timestamp_start = datetime.now()

    def check_out(self):
        self.rent_timestamp_end = datetime.now()
        duration = self.rent_timestamp_end - self.rent_timestamp_start
        amount = self.cost_per_minute * int(round(duration.total_seconds()/60))
        self.total_benefit = self.total_benefit + amount
        self.free()

    def in_use(self):
        return self.user_id is not None

    def free(self):
        self.user_id = None

    def __str__(self):
        return str(self.id) + "_Benefit_" + str(self.total_benefit)
