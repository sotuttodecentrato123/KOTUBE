$ErrorActionPreference = "SilentlyContinue"
$port = 48217

function Get-ListenerPids {
    $conns = Get-NetTCPConnection -LocalPort $port -State Listen -ErrorAction SilentlyContinue
    if ($conns) {
        return @($conns | Select-Object -ExpandProperty OwningProcess -Unique)
    }
    $trovati = @()
    foreach ($linea in (netstat -ano | Select-String ":$port\s" | Select-String "LISTENING")) {
        $trovati += [int](($linea.Line -split "\s+")[-1])
    }
    return @($trovati | Select-Object -Unique)
}

for ($giro = 0; $giro -lt 5; $giro++) {
    $processi = Get-ListenerPids
    if (-not $processi) { break }
    $fermatoQualcosa = $false
    foreach ($procId in $processi) {
        if ($procId -le 0) { continue }
        $proc = Get-CimInstance Win32_Process -Filter "ProcessId=$procId"
        $exe = $proc.ExecutablePath
        $cmd = $proc.CommandLine
        $nostro = ($exe -and $exe -like "*KOTUBE*") -or ($cmd -and $cmd -like "*KOTUBE*")
        if ($nostro) {
            & taskkill.exe /PID $procId /T /F 2>$null | Out-Null
            $fermatoQualcosa = $true
        }
    }
    if (-not $fermatoQualcosa) { break }
    Start-Sleep -Milliseconds 700
}