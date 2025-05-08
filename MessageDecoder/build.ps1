$exclude = @("venv", "message_decoder.zip")
$files = Get-ChildItem -Path . -Exclude $exclude
Compress-Archive -Path $files -DestinationPath "message_decoder.zip" -Force