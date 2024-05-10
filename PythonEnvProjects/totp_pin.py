import pyotp as tp

totp_key = "HPAPMMM4LHEF3RPIW3MSOQALJQEZSM43"
k = tp.TOTP(totp_key).now()
print(k)
