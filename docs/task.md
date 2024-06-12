# Nagy nyelvi modell alapú chatbot Teamshez a szakmai gyakorlatok támogatására

A mérnökképzés egyik sarkalatos és fontos pontja a BME-n a szakmai gyakorlat megszerzése.
Ennek szervezését törvényi előírások, egyetemi szabályzatok részletesen kezelik.
Ennek ellenére gyakran érzik magukat annyira elveszettnek a hallgatók, hogy a szakmai gyakorlat szervezőjéhez, Blázovics Lászlóhoz fordulnak kérdéseikkel, gyakran Microsoft Teams üzenetek formájában.
Ő természetesen tudja, minek hol érdemes utánanézni, és lelkiismeretesen válaszol.
Azonban ez sok más hasznos tevékenységtől veszi el az idejét.

A téma célja, hogy a hallgató

* megismerkedjen a nagy nyelvi modellek alapjaival (LLM)
* megismerje ezek finomhangolási módszereit (PEFT/LoRA)
* képes legyen egy elérhető modell finomhangolására a szakmai gyakorlathoz elérhető információk segítségével
   * Ehhez megismerhet magas szintű keretrendszereket is (mint pl. a Ludwig)
* teszt interfészt készítsen Gradio használatával
* egy olyan Teams alkalmazást készítsen, amely a fenti modellre támaszkodva releváns módon válaszol a szakmai gyakorlattal kapcsolatos kérdésekre
* RAG architektúra segítségével képes legyen élő adatokkal dolgozni (pl. szerződött vállalatok frissülő listája itt)
    * (Ehhez ki lehet próbálni magas szintű kódkönyvtárakat is, mint pl. az embedchain, vagy még komplexebbet, mint pl. a langchain)
* tehermentesítse Lacit
