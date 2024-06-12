# 3. hét

Hasznos repo lehet: https://github.com/oroszgy/awesome-hungarian-nlp

## Puli GPT-3SX
Kipróbálható: https://juniper.nytud.hu/demo/puli

![](pics/puli_test.png)

egyszerű utasításra, kérdésre se ad megfelelő választ

![img.png](pics/puli_test2.png)

szövegek folytatására alkalmas, de arra se igazán megbízhatóan alkalmazható

few-shot inference:

![img.png](pics/puli_test3.png)

Utóbbi kettő az oldal példa promptjai közül vannak, de ezek se megbízhatóak

## Puli GPTrio

https://huggingface.co/NYTK/PULI-GPTrio

Ez már magyar és angol szövegen is volt tanítva, az eredményei is jobbak. Megpróbálja a feladatot elvégezni, nem feltételen jó válaszokat ad azonban.

Kipróbálható: https://juniper.nytud.hu/demo/gptrio

![img.png](pics/puli_gptrio_test.png)

![img.png](pics/puli_gptrio_test2.png)

 A húslevesrecept egész jó, pár paraméterállítás után:
![img.png](pics/puli_gptrio_parameters.png)

Helyi futtatás esetén ilyen errort kapok:
![](pics/local_run_error.png)

Google colab esetén hasonló hiba:
![](pics/colab_run_error.png)

## Magyar sentence transformer

https://huggingface.co/NYTK/sentence-transformers-experimental-hubert-hungarian

## Fine-tuned huBERT

https://huggingface.co/mcsabai/huBert-fine-tuned-hungarian-squadv2

![img.png](pics/hubert_test.png)

A modell megfelelő kontextus esetén helyesen válaszol a kérdésekre, hasznos lehet nekünk.

Több kérdést egyszerre nem tud megválaszolni, kisebb magabiztosággal válaszol az egyikre:

Több:
![](pics/hubert_local_test.png)

Egy:
![](pics/hubert_local_test2.png)

## CUDA problémák
Feltelepítettem a CUDA-t, de a laborban a `torch.cuda.is_available()` függvény `False`-t ad vissza. A `nvidia-smi` parancs viszont megfelelően működik, a `nvcc --version` parancs pedig azt írja, hogy a CUDA 12.2 van telepítve.

![CUDA installed](pics/cuda_installed.png)

sikerült megoldani, hogy lássa, de most futtatás közben a következő hibaüzenetet kapom:

![CUDA error](pics/cuda_error.png)

## Szakmai Gyakorlat források

A resources.md-ben találhatóak