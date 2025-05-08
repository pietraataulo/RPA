$exclude = @("venv", "GroceryOrder.zip")
$files = Get-ChildItem -Path . -Exclude $exclude
Compress-Archive -Path $files -DestinationPath "GroceryOrder.zip" -Force