rule eicar_av_test {
    meta:
        description = "EICAR test file detection"
        author = "Your Name"
        severity = "critical"
        reference = "https://www.eicar.org/"
    strings:
        $eicar = "X5O!P%@AP[4\\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*"
    condition:
        $eicar
}
