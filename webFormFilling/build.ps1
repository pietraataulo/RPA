$exclude = @("venv", "webFormFilling.zip")
$files = Get-ChildItem -Path . -Exclude $exclude
Compress-Archive -Path $files -DestinationPath "webFormFilling.zip" -Force