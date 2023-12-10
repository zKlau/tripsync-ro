# TripSync RO - Weather generator

Generatorul de vreme pentru aplicația TripSync RO. Din motive financiare, pentru a putea obține date oficiale despre vreme pe o perioadă mai mare de 14 zile, mulți furnizori de API cer un abonament. Din acest motiv, am decis să creăm un generator de vreme.

## FAQ

#### Cum generăm temperaturile?

Obținem extremele temperaturilor în timpul unei perioade (lună/săptămână) și generăm un număr aleatoriu în intervalul temperaturii minime și temperaturii maxime.

#### Cum generăm starea vremii?

Avem o tabelă de probabilitate din care stabilim șansa ca un tip de vreme să apară, apoi în funcție de temperatură generăm vremea (dacă este prea cald, nu va ninge).

#### Cum salvăm datele?

Datele sunt salvate într-un fișier de tip JSON.

## Tech Stack

Python 3.12
