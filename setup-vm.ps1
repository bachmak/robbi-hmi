$ip = (Get-NetIPAddress -AddressFamily IPv4 |
    Where-Object {
        $_.IPAddress -notlike "169.254.*" -and
        $_.IPAddress -ne "127.0.0.1" -and
        $_.IPAddress -notlike "192.168.*"
    } |
    Select-Object -First 1 -ExpandProperty IPAddress)

Write-Host "OPC UA URL: opc.tcp://${ip}:4840"

netsh interface portproxy add v4tov4 `
    listenaddress=$ip listenport=4840 `
    connectaddress=VM_IP connectport=4840

netsh advfirewall firewall add rule `
    name="PortProxy 4840" dir=in action=allow `
    protocol=TCP localport=4840

sc start iphlpsvc
