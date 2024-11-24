wallet=200000
profit=1.15
annee=5
mois=annee*12
for i in range(1, mois):
    wallet = wallet*profit

print(round(wallet))