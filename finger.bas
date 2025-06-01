' A simple finger client for a Raspberry Pi Pico 2w
' running Webmite. Tested on V6.00.02RC25.
DIM buff%(4096/8)
DIM STRING address$
DIM INTEGER atPos
DIM STRING user$, host$
CONST CRLF$ = CHR$(13) + CHR$(10)

    PRINT "Enter the address to finger"
    PRINT "(example: jcs@plan.cat or plan.cat)"

DO
    INPUT "Address: ", address$

    IF address$ = "" THEN
        PRINT "Error: Address cannot be blank."
        CONTINUE DO
    ENDIF

    atPos = INSTR(address$, "@")

    IF atPos = 0 THEN
        user$ = ""
        host$ = address$
    ELSE
        IF INSTR(atPos + 1, address$, "@") > 0 THEN
            PRINT "Error: Address can contain only one '@'."
            CONTINUE DO
        ENDIF

        user$ = LEFT$(address$, atPos - 1)
        host$ = MID$(address$, atPos + 1)
    ENDIF

    IF host$ = "" THEN
        PRINT "Error: Host is missing."
        CONTINUE DO
    ENDIF

    EXIT DO

LOOP

CONST Query = user$ + CRLF$

WEB OPEN TCP CLIENT host$, 79
WEB TCP CLIENT REQUEST Query, buff%()
WEB CLOSE TCP CLIENT
LONGSTRING PRINT buff%()
