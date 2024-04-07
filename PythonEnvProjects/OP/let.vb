let 

    p2 = Excel.CurrentWorkbook(){[Name="NIFTY_P"]}[Content],
    up = p2[SymbolPrice]{0},

    p3= Excel.CurrentWorkbook(){[Name="Table4"]}[Content],
    exp= p3[Expiry]{0},

    p4 = Excel.CurrentWorkbook(){[Name="Table4"]}[Content],
    st=p3[No. of Strikes]{0},

    Source = Excel.CurrentWorkbook(){[Name="Table1"]}[Content],
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"strikePrice", Int64.Type}, {"expiryDate", type datetime}, {"PE.openInterest", type number}, {"PE.changeinOpenInterest", Int64.Type}, {"PE.impliedVolatility", type number}, {"PE.lastPrice", type number}, {"PE.change", type number},{"CE.openInterest", type number}, {"CE.changeinOpenInterest", Int64.Type}, {"CE.impliedVolatility", type number}, {"CE.lastPrice", type number}, {"CE.change", type number}}),
    #"Removed Columns" = Table.RemoveColumns(#"Changed Type",{"CE.pChange", "CE.totalBuyQuantity", "CE.totalSellQuantity", "CE.bidQty", "CE.bidprice", "CE.askQty", "CE.askPrice", "CE.underlyingValue", "timestamp", "underlying_value", "CE.totalTradedVolume", "CE.pchangeinOpenInterest", "PE.pChange", "PE.totalBuyQuantity", "PE.totalSellQuantity", "PE.bidQty", "PE.bidprice", "PE.askQty", "PE.askPrice", "PE.underlyingValue", "CE.strikePrice", "CE.expiryDate", "CE.underlying", "CE.identifier", "PE.pchangeinOpenInterest", "PE.totalTradedVolume", "PE.strikePrice", "PE.expiryDate", "PE.underlying", "PE.identifier"}),
    #"Added Custom" = Table.AddColumn(#"Removed Columns", "Custom", each up-[strikePrice]),
    #"Filtered Rows" = Table.SelectRows(#"Added Custom", each [Custom] >= -(st*50) and [Custom] <= (st*50)),
    #"Filtered Rows1" = Table.SelectRows(#"Filtered Rows", each ([Expiry] = Date.From(exp)))

in 
    #"Filtered Rows1"