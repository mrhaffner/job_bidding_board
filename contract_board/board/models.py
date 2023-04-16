from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone


USER_CHOICES = [
    ('CONTRACTOR', 'Contractor'),
    ('CONTRACTEE', 'Contractee'),
]


class User(AbstractUser):
    """A user of the contract board is a contractor or a contractee."""
    type = models.CharField(max_length=10, choices=USER_CHOICES)
    agency_name = models.CharField(max_length=200)


class Contract(models.Model):
    """
    A contract object with a title, agency name, contact information,
    bidding end date, and job description. Includes methods to
    calculate lowest bid and number of bids.
    """
    contract_title = models.CharField(max_length=200, unique=True)
    bidding_end_date = models.DateField()
    job_description = models.TextField()
    contractee = models.ForeignKey(User, on_delete=models.CASCADE)
    date_placed = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(null=True)

    @property
    def lowest_bid(self):
        """
        Returns the lowest bid amount for the contract object.
        """
        bids = Bid.objects.filter(contract__pk=self.pk)
        lowest_bid = float('inf')
        for bid in bids:
            lowest_bid = min(bid.amount, lowest_bid)
        return lowest_bid if lowest_bid < float('inf') else 0

    @property
    def number_bids(self):
        """
        Returns the number of bids for the contract object.
        """
        bids = Bid.objects.filter(contract__pk=self.pk)
        return len(bids)

    @property
    def bids(self):
        return Bid.objects.filter(contract__pk=self.pk)
    
    @property
    def expired(self):
        """
        Returns True if the bidding end date has passed, False otherwise.
        """
        return timezone.now().date() > self.bidding_end_date
    
    class Meta:
        ordering = ['-date_placed']


class Bid(models.Model):
    """
    A bid object with a contractor name, bid amount,
    contact information, date placed, and foreign key
    to a Contract object.
    """
    amount = models.FloatField(validators=[MinValueValidator(0.01)])
    date_placed = models.DateField(auto_now_add=True)
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
    contractor = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-amount']