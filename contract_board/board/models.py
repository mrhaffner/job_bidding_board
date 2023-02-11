from django.db import models

class Contract(models.Model):
    contract_title = models.CharField(max_length=200)
    agency_name = models.CharField(max_length=200)
    contact_information = models.CharField(max_length=500)
    bidding_end_date = models.DateField()
    job_description = models.TextField()
    lowest_bid = models.FloatField(default=0)
    number_bids = models.IntegerField(default=0)

    def __str__(self):
        return self.contract_title

class Bid(models.Model):
    contractor_name = models.CharField(max_length=200)
    amount = models.FloatField()
    contact_information = models.CharField(max_length=500)
    date_placed = models.DateTimeField(auto_now_add=True)
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)

    def __str__(self):
        return self.contractor_name