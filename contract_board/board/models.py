from django.db import models


class Contract(models.Model):
    contract_title = models.CharField(max_length=200)  # length
    agency_name = models.CharField(max_length=200)  # length
    contact_information = models.CharField(max_length=500)  # length
    bidding_end_date = models.DateField()
    job_description = models.TextField()

    @property
    def lowest_bid(self):
        bids = Bid.objects.filter(contract__pk=self.pk)
        lowest_bid = float('inf')
        for bid in bids:
            lowest_bid = min(bid.amount, lowest_bid)
        return lowest_bid if lowest_bid < float('inf') else 0

    @property
    def number_bids(self):
        bids = Bid.objects.filter(contract__pk=self.pk)
        return len(bids)


class Bid(models.Model):
    contractor_name = models.CharField(max_length=200)  # length
    amount = models.FloatField()  # decimal places
    contact_information = models.CharField(max_length=500)  # length
    date_placed = models.DateField(auto_now_add=True)
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)