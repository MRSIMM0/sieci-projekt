# Zdalne wyłączanie systemów

## Opis protokołu

Serwer z klientem porozumiewają się ze sobą za pomocą protokołu TCP/IP. Serwer i klient wymieniają między sobą komunikaty. Serwer wysyła do klienta polecenie ‘shutdown’ gdy ma nastąpić wyłączenie systemu. Klient wysyła cyklicznie do serwera informacje o stanie systemu (nazwa, użycie procesora, itd). Informacje te przekazywane są w formacie JSON.

## Instalacja

Wymagany jest **python 3.11**. Aby zainstalować wymagane biblioteki należy uruchomić komendę w folderze glównym:

```bash
pip install -r requirements.txt
```

Aby uruchomić serwer lub klient należy wykonać komendę:

```bash
python main.py
```

w folderze server lub klient.

Po uruchomieniu serwera i klienta na liście pojawi się rekord, alby zobaczyć szczegóły należy na niego kliknąć.

Aby wyłączyć dany system należy kliknąć na rekord aby wyświetlić szczegóły a następnie shutdown.

