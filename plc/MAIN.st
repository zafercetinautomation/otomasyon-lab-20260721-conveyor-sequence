(**
    Konveyör Sıralı Çalışma
    Eğitim ve simülasyon amaçlı TwinCAT 3 Structured Text örneği.

    Önemli: Giriş ve çıkışlar semboliktir. Gerçek donanım eşlemesi,
    emniyet analizi ve saha doğrulaması bu örneğin kapsamı dışındadır.
*)
PROGRAM MAIN
VAR
    // Sembolik girişler
    bStart         : BOOL;
    bStop          : BOOL;
    bProductSensor : BOOL;
    bResetCount    : BOOL;

    // Sembolik çıkışlar ve izleme değerleri
    bMotor          : BOOL;
    bRunning        : BOOL;
    bBatchComplete  : BOOL;
    nProductCount   : UINT := 0;
    nBatchTarget    : UINT := 10;

    // Sensör TRUE durumunda kalırsa aynı ürünü tekrar saymamak için
    fbProductEdge : R_TRIG;
END_VAR

fbProductEdge(CLK := bProductSensor);

// Durdurma komutu başlatma komutundan önceliklidir.
IF bStop THEN
    bRunning := FALSE;
ELSIF bStart AND NOT bBatchComplete THEN
    bRunning := TRUE;
END_IF

// Sayaç yalnızca konveyör duruyken sıfırlanabilir.
IF bResetCount AND NOT bRunning THEN
    nProductCount := 0;
    bBatchComplete := FALSE;
END_IF

// Ürün sadece konveyör çalışırken ve sensörün yükselen kenarında sayılır.
IF bRunning AND fbProductEdge.Q THEN
    IF nProductCount < UINT#65535 THEN
        nProductCount := nProductCount + 1;
    END_IF

    // Hedef 0 yapılırsa yanlışlıkla anında tamamlanmayı önle.
    IF (nBatchTarget > 0) AND (nProductCount >= nBatchTarget) THEN
        bBatchComplete := TRUE;
        bRunning := FALSE;
    END_IF
END_IF

bMotor := bRunning;

END_PROGRAM
