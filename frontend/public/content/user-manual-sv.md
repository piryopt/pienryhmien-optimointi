# Användarguide

1. Skapa en enkät
2. Skapa en flerstegsundersökning
3. Hantera en enkät
4. Behandla svar
5. Besvara en enkät
6. Besvara en flerstegsundersökning

Jakajas funktioner visas på startsidan enligt följande:

<img src="images/front_page.png" alt="Startsida" class="md-image" />

## 1. Skapa en enkät

Att skapa en enkät börjar med att klicka på knappen **”Skapa ny enkät”** på startsidan. Applikationen öppnar ett formulär som fylls i enligt följande:

### 1.1 Enkätens namn

- Ge enkäten ett tydligt och beskrivande namn. Namnet måste vara minst 5 tecken långt.
- Namnet måste vara unikt, eftersom Jakaja inte kan ha flera enkäter med samma namn aktiva samtidigt.

### 1.2 Svarsperiod

- Ange start- och sluttid för enkäten. Klicka på fältet och välj ett datum från kalendern eller ange det i formatet dd.mm.yyyy. Ange tiden i formatet hh:mm.
- **Obs:** Enkätens sluttid kan inte ligga i det förflutna.
- Applikationen stänger automatiskt enkäten vid den angivna sluttiden. Vid behov kan enkäten öppnas igen senare (se avsnitt 3.3).

<img src="images/date_of_closing.png" alt="Slutdatum" class="md-image" />

### 1.3 Enkätbeskrivning

- Beskrivningen är valfri. Du kan skriva en kort beskrivning av enkäten eller ge ytterligare instruktioner till respondenterna.

<img src="images/description.png" alt="Enkätbeskrivning" class="md-image" />

### 1.4 Krävs rangordning av alla grupper?

- Välj **”Ja”** om respondenterna måste rangordna alla tillgängliga alternativ.
- Välj **”Nej”** om respondenterna endast behöver rangordna vissa alternativ. Ett nytt fält **”Minsta antal prioriterade grupper”** visas, där du kan ange minimivärdet som ett heltal.

<img src="images/number_of_prioritized_groups.png" alt="Minsta antal prioriterade grupper" class="md-image" />

- Att begränsa antalet rangordnade alternativ rekommenderas när det finns många alternativ (20+).
  - **OBS:** För en lyckad gruppindelning är det viktigt att samla in tillräckligt med preferensdata. Sätt inte minimivärdet för lågt. Det rekommenderas att kräva rangordning av minst 3–5 alternativ beroende på det totala antalet alternativ.

### 1.5 Är nekade val tillåtna?

- Välj **”Ja”** om respondenterna får neka vissa alternativ. Ett nytt fält **”Antal tillåtna nekade grupper”** visas, där du kan ange antalet nekanden som ett heltal.
- Att neka ett alternativ kräver en motivering på minst 10 tecken, som visas i sammanställningen av svaren.

<img src="images/allow_denied_choices.png" alt="Nekade val" class="md-image" />

### 1.6 Prioriterade grupper

- Alternativ kan läggas till manuellt eller importeras från en CSV-fil.
- Prioriterade grupper är de alternativ som respondenterna kan rangordna och som de tilldelas till efter att enkäten stängts.
- Varje alternativ måste innehålla minst:
  - Namn
  - Maximal kapacitet
  - Minsta storlek (ange 0 om minsta storlek inte spelar någon roll)
- Grupper som inte uppnår minsta storlek exkluderas från tilldelningen. För att säkerställa att en grupp skapas oavsett, välj **”Tvinga minsta storlek”**.
- Ytterligare datafält kan läggas till genom att klicka på **”+ Lägg till datafält”**.
  - Om ett fält inte ska vara synligt för respondenterna, lägg till en asterisk (\*) i dess identifierare.
  - Extra fält kan tas bort med hjälp av papperskorgsikonen.

Exempel med postnummer och adress som extra information:

<img src="images/survey_choices.png" alt="Enkätalternativ" class="md-image" />

När en respondent öppnar formuläret visas alternativen enligt följande:

<img src="images/answer_page.png" alt="Svarsida" class="md-image" />

### Importera alternativ från en CSV-fil

- CSV är ett textbaserat filformat där värden separeras med kommatecken.  
  ([Mer information på Wikipedia](https://en.wikipedia.org/wiki/Comma-separated_values))
- Detaljerade instruktioner för hur alternativ importeras från en CSV-fil finns här: [csv-instructions](csv-instructions)

### Skapa enkät

- När alla obligatoriska fält har fyllts i klickar du på **”Skapa enkät”**.
- Om skapandet misslyckas visar applikationen ett felmeddelande som beskriver vad som behöver åtgärdas.
- Enkäten visas på sidan **”Visa tidigare enkäter”** och under **”Aktiva enkäter”** på startsidan.

---

## 2. Skapa en flerstegsundersökning

Att skapa en flerstegsundersökning börjar på samma sätt som en vanlig enkät, men formuläret innehåller ytterligare inställningar:

### 2.1 Är frånvaro tillåten?

- Välj **”Ja”** om respondenterna får markera sig som frånvarande.
  - Frånvaro är då tillåten i alla steg.

### 2.2 Begränsa deltagandeantal

- Välj **”Ja”** för att begränsa hur många gånger en respondent kan delta i en specifik grupp.
  - Till exempel: om en respondent tilldelas en grupp med deltagandebegränsning 1 i ett tidigare steg, kommer hen inte att tilldelas samma grupp i senare steg.
- Deltagandebegränsningar anges per grupp i kolumnen **”Deltagandeantal\*”**.

<img src="images/participation_limit.png" alt="Deltagandebegränsning" class="md-image" />

- Gruppnamnen måste vara identiska i alla steg för att deltagandebegränsningarna ska fungera korrekt.

### 2.3 Steghantering

#### 2.3.1 Lägga till ett steg

- Lägg till ett steg genom att klicka på **”Lägg till steg”**. En ny tabell visas för att definiera alternativen.

<img src="images/stage.png" alt="Steg" class="md-image" />

#### 2.3.2 Stegidentifierare

- Varje steg måste ha en unik identifierare (t.ex. datum eller veckonummer).
- Respondenterna navigerar mellan stegen med hjälp av dessa identifierare, så de bör tydligt beskriva steget.

#### 2.3.3 Lägga till alternativ till ett steg

- Alternativ kan läggas till manuellt eller importeras från en CSV-fil, precis som i en vanlig enkät.

#### 2.3.4 Kopiera ett steg

- Klicka på **”Kopiera steg”** för att duplicera ett steg och all dess data.

#### 2.3.5 Ta bort ett steg

- Klicka på **”Ta bort steg”** för att ta bort ett steg.

---

## 3. Hantera en enkät

Alla enkäter listas på sidan **”Visa tidigare enkäter”**.

<img src="images/survey_management.png" alt="Enkätadministration" class="md-image" />

### 3.1 Skicka enkäten till respondenter

- Klicka på **”Kopiera enkäten länk till urklipp”** eller kopiera URL:en från webbläsarens adressfält.

### 3.2 Stänga en enkät

- Öppna **”Visa resultat”** och klicka på **”Stäng enkät”**.

### 3.3 Återöppna en stängd enkät

- Klicka på **”Öppna enkät igen”** och bekräfta.

### 3.4 Ge administrativa rättigheter

- På redigeringssidan anger du en annan lärares e-postadress och klickar på **”Lägg till lärare”**.

<img src="images/admin.png" alt="Administratörsrättigheter" class="md-image" />

### 3.5 Redigera en enkät

- Du kan redigera namn, beskrivning och svarsperiod.
- Gruppstorlekar kan endast redigeras om det finns fler respondenter än tillgängliga platser.

### 3.6 Ta bort en enkät

- Borttagna enkäter flyttas till papperskorgen och tas bort permanent efter en vecka.

### 3.7 Återställa en enkät

- Borttagna enkäter kan återställas från papperskorgen.

### 3.8 Kopiera en enkät

- Klicka på **”Kopiera enkät”** för att skapa en ny enkät baserad på en befintlig.

---

## 4. Behandla svar

### 4.1 Visa svar

- Klicka på **”Visa resultat”** på enkäten.

### 4.2 Gruppindelning

- Stäng enkäten och klicka sedan på **”Fördela grupper”**.

### 4.3 Fler svar än platser

- Redigera gruppstorlekar vid behov.
- Om det behövs skapas en grupp **”Tom”** för respondenter som inte tilldelats någon grupp.

### 4.4 Behandla resultat

- Klicka på **”Spara resultat”** för att spara tilldelningen.
- Sparade enkäter kan inte återöppnas.
- Resultat kan exporteras till Excel.

---

## 5. Besvara en enkät

<img src="images/answer.png" alt="Besvara enkät" class="md-image" />

### 5.1 Rangordna alternativ

- Dra alternativen till den gröna rutan och ordna dem enligt preferens.

### 5.2 Neka alternativ

- Om tillåtet, dra alternativen till den röda rutan och ange en motivering på minst 10 tecken.

---

## 6. Besvara en flerstegsundersökning

<img src="images/multistage_answer.png" alt="Besvara flerstegsundersökning" class="md-image" />

### 6.1 Steg

- Navigera mellan stegen med hjälp av stegidentifierarna.
- Besvara varje steg som en vanlig enkät.

### 6.2 Frånvaro

- Om tillåtet, klicka på **”Jag är frånvarande”** för att markera frånvaro.

<img src="images/absence.png" alt="Frånvaro" class="md-image" />
