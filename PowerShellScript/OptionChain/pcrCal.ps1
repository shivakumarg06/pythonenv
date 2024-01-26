# Sample CSV file path (replace with your actual file path)
$csvFilePath = ".\PowerShellScript\OptionChain\option-chain-ED-NIFTY-25-Jan-2024.csv"

# Import CSV data
$optionChainData = Import-Csv $csvFilePath

# Extract relevant columns for open interest
$putOpenInterest = $optionChainData | Where-Object { $_.OptionType -eq "put" } | Measure-Object OpenInterest -Sum | Select-Object -ExpandProperty Sum
$callOpenInterest = $optionChainData | Where-Object { $_.OptionType -eq "call" } | Measure-Object OpenInterest -Sum | Select-Object -ExpandProperty Sum

# Calculate PCR
$pcr = $putOpenInterest / $callOpenInterest

# Output PCR
Write-Host "Put-Call Ratio: $pcr"

# Assuming you have columns like 'StrikePrice' and 'Close' for support and resistance calculation
$supportLevel = $optionChainData | Sort-Object Close | Select-Object -First 1
$resistanceLevel = $optionChainData | Sort-Object Close -Descending | Select-Object -First 1

# Output support and resistance levels
Write-Host "Support Level: $($supportLevel.StrikePrice)"
Write-Host "Resistance Level: $($resistanceLevel.StrikePrice)"


#########################################################################################################
#########################################################################################################
#########################################################################################################
#########################################################################################################
