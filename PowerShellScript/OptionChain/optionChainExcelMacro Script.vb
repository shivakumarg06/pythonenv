Let cookies=()=>

in     cookies 

========================= 

Let
Source = Json.Document(Web.Contents("https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY", [Headers=[#"Accept-Encoding"="gzip, deflate", #"Accept-Language"="en-US,en", #"User-Agent"="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 OPR/68.0.3618.206", Cookie="8A87B46ABA4CAFF3B69F913708597828~xM8YKIspOw4k2OTekhqVI8Ft8AHi/RYKbvLqfKirkbafd1XOqJELenPBKr4Y+FAgbqei34v6NKmWyp1RWvhDhh2jrLXAela7ZdmyrHShEPCaVopVDul8R91B2SbFshwrUsS7yKn5+cmpmaF25zGeiAjHTfTMnii7F2E1slCnkEo="]])),
records = Source[records],
data = records[data], 
#"Converted To Table" = Table.FromList(data, Splitter.SplitByNothing(), null, null, ExtraValues.Error),    
#"Expanded Column1" = Table.ExpandRecordColumn(#"Converted To Table", "Column1", {"strikePrice", "expiryDate", "CE", "PE"}, {"strikePrice", "expiryDate", "CE", "PE"})
in
#"Expanded Column1" 

========================= =If(P4>=1,"Buy",If(P4=0,"-",If(P4<=-1,"Sell"))) ========================= Sub time() Sheets("Nifty1").Range("j3").Copy Sheets("Nifty1").Range("m3") Sheets("Nifty1").Range("m3:p3").Copy Sheets("Nifty1").Range("m4").PasteSpecial xlPasteValues Set a = Sheets("Nifty1").Range("m4:p4") Set B = Sheets("Nifty1").Range("m400000:p400000").End(xlUp).Offset(1, 0) a.Copy B End Sub ========================== Sub runtimer() Application.OnTime Now + TimeSerial(0, 5, 0), "runtimer" time End Sub ========================== Private Sub Workbook_BeforeClose(Cancel As Boolean) ActiveWorkbook.Save End Sub Private Sub Workbook_Open() End Sub ==========================


