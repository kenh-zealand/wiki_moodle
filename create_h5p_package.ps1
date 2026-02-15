# PowerShell script to create H5P package

$h5pFolder = "StaffHandbook_H5P"

# Create temporary folder
New-Item -ItemType Directory -Force -Path $h5pFolder | Out-Null

# Copy files to temp folder
Copy-Item "h5p.json" $h5pFolder
Copy-Item -Recurse "content" $h5pFolder
Copy-Item -Recurse "H5P.StaffHandbook-1.0" $h5pFolder

Write-Host "✓ Files copied to temp folder"

# Create ZIP file (H5P package)
$zipPath = "StaffHandbook.h5p"
if (Test-Path $zipPath) {
    Remove-Item $zipPath -Force
}

Compress-Archive -Path "$h5pFolder\*" -DestinationPath $zipPath -CompressionLevel Optimal

Write-Host "✓ H5P package created: $zipPath"

# Clean up temp folder
Remove-Item -Recurse -Force $h5pFolder

Write-Host "✓ Cleanup complete"

# Show file size
$fileSize = (Get-Item $zipPath).Length / 1KB
Write-Host ""
Write-Host "H5P Package Ready!"
Write-Host "File: $zipPath"
Write-Host "Size: $([math]::Round($fileSize, 2)) KB"
